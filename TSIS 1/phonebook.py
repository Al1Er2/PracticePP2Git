# phonebook.py
import psycopg2
import csv
import json
import sys
import os

DB_CONFIG = {
    "dbname": "phonebook_db",
    "user": "postgres",
    "password": "@Klaus",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def execute_sql_file(filename):
    """Utility to run schema.sql and procedures.sql"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, filename)
    if not os.path.exists(full_path):
        print(f"Skipping {filename}: not found.")
        return
    
    conn = get_db_connection()
    cur = conn.cursor()
    with open(full_path, 'r', encoding='utf-8') as f:
        cur.execute(f.read())
    conn.commit()
    cur.close()
    conn.close()

# ----------------- 3.3 IMPORT / EXPORT -----------------

def import_csv(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, filename)

    if not os.path.exists(full_path):
        print(f"Error: The file '{filename}' was not found.")
        return

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        with open(full_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 1. Ensure group exists
                group_name = row.get('group', 'Other')
                cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT DO NOTHING RETURNING id;", (group_name,))
                cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
                group_id = cur.fetchone()[0]

                # 2. Insert Contact
                cur.execute("""
                    INSERT INTO contacts (first_name, last_name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """, (row['first_name'], row.get('last_name'), row.get('email'), row.get('birthday') or None, group_id))
                contact_id = cur.fetchone()[0]

                # 3. Insert Phone
                if row.get('phone_number'):
                    phone_type = row.get('phone_type', 'mobile')
                    cur.execute("""
                        INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)
                    """, (contact_id, row['phone_number'], phone_type))
                    
        conn.commit()
        print("CSV imported successfully!")
    except Exception as e:
        print(f"Error reading CSV: {e}")
    finally:
        cur.close()
        conn.close()

def export_json(filename="contacts.json"):
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = """
    SELECT c.first_name, c.last_name, c.email, c.birthday::TEXT, g.name as group,
           COALESCE(json_agg(json_build_object('phone', p.phone, 'type', p.type)) FILTER (WHERE p.phone IS NOT NULL), '[]') as phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    GROUP BY c.id, g.name;
    """
    cur.execute(query)
    columns = [desc[0] for desc in cur.description]
    data = [dict(zip(columns, row)) for row in cur.fetchall()]
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
    print(f"Exported to {filename} successfully.")
    cur.close()
    conn.close()

def import_json(filename="contacts.json"):
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return

    conn = get_db_connection()
    cur = conn.cursor()
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for item in data:
        # Check for duplicates by first_name
        cur.execute("SELECT id FROM contacts WHERE first_name = %s", (item['first_name'],))
        existing = cur.fetchone()
        
        if existing:
            choice = input(f"Duplicate found for '{item['first_name']}'. [O]verwrite or [S]kip? ").strip().lower()
            if choice == 's':
                continue
            elif choice == 'o':
                # Overwrite: delete existing and proceed to re-insert
                cur.execute("DELETE FROM contacts WHERE id = %s", (existing[0],))
        
        # Insert Group
        group_name = item.get('group', 'Other')
        if group_name:
            cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT DO NOTHING", (group_name,))
            cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            group_id = cur.fetchone()[0]
        else:
            group_id = None
            
        # Insert Contact
        cur.execute("""
            INSERT INTO contacts (first_name, last_name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        """, (item['first_name'], item.get('last_name'), item.get('email'), item.get('birthday') or None, group_id))
        contact_id = cur.fetchone()[0]
        
        # Insert Phones
        for phone_obj in item.get('phones', []):
            cur.execute("""
                INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)
            """, (contact_id, phone_obj['phone'], phone_obj['type']))
            
    conn.commit()
    print("JSON imported successfully.")
    cur.close()
    conn.close()

# ----------------- 3.2 & 3.4 CONSOLE SEARCH / FILTER / PROCS -----------------

def execute_search_function():
    term = input("Search term (Name, Email, or Phone): ")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (term,))
    results = cur.fetchall()
    if results:
        print("\nResults:")
        for r in results: print(r)
    else:
        print("No matches found.")
    cur.close()
    conn.close()

def filter_and_sort():
    print("\n1. Filter by Group\n2. Search by Email\n3. Sort All Contacts")
    choice = input("Select an option: ")
    conn = get_db_connection()
    cur = conn.cursor()
    
    if choice == '1':
        grp = input("Enter Group Name (e.g., Family, Work): ")
        cur.execute("""
            SELECT c.first_name, c.last_name, g.name 
            FROM contacts c JOIN groups g ON c.group_id = g.id 
            WHERE g.name ILIKE %s
        """, (grp,))
    elif choice == '2':
        email_frag = input("Enter email snippet (e.g. 'gmail'): ")
        cur.execute("SELECT first_name, last_name, email FROM contacts WHERE email ILIKE %s", (f'%{email_frag}%',))
    elif choice == '3':
        print("Sort by: [1] Name  [2] Birthday  [3] Date Added")
        sort_choice = input("Choice: ")
        order_col = "first_name"
        if sort_choice == '2': order_col = "birthday"
        elif sort_choice == '3': order_col = "created_at"
        cur.execute(f"SELECT first_name, last_name, birthday, created_at FROM contacts ORDER BY {order_col} ASC")
    else:
        print("Invalid choice.")
        return

    for row in cur.fetchall(): print(row)
    cur.close()
    conn.close()

def paginated_navigation():
    limit = 3
    offset = 0
    conn = get_db_connection()
    cur = conn.cursor()
    
    while True:
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
        rows = cur.fetchall()
        print(f"\n--- Page {(offset//limit)+1} ---")
        if not rows:
            print("No more records.")
        else:
            for r in rows: print(r)
            
        action = input("\n[N]ext page | [P]revious page | [Q]uit : ").lower()
        if action == 'n':
            if len(rows) == limit: offset += limit
        elif action == 'p':
            if offset >= limit: offset -= limit
        elif action == 'q':
            break
            
    cur.close()
    conn.close()

def proc_add_phone():
    name = input("Contact First Name: ")
    phone = input("Phone Number: ")
    ptype = input("Type (home/work/mobile): ")
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        conn.commit()
        print("Phone added via stored procedure.")
    except Exception as e:
        print(f"Error: {e}")
    cur.close()
    conn.close()

def proc_move_group():
    name = input("Contact First Name: ")
    grp = input("New Group Name: ")
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, grp))
        conn.commit()
        print("Moved to group via stored procedure.")
    except Exception as e:
        print(f"Error: {e}")
    cur.close()
    conn.close()

# ----------------- MAIN LOOP -----------------

def main():
    # Setup initial schemas and functions if needed
    execute_sql_file("schema.sql")
    execute_sql_file("procedures.sql")
    
    while True:
        print("\n--- PhoneBook TSIS 1 ---")
        print("1. Import CSV")
        print("2. Export JSON")
        print("3. Import JSON")
        print("4. Global Search (Uses PL/pgSQL Function)")
        print("5. Filter & Sort Contacts")
        print("6. Paginated Navigation")
        print("7. Add Phone to Contact (PL/pgSQL Proc)")
        print("8. Move Contact to Group (PL/pgSQL Proc)")
        print("9. Exit")
        choice = input("Select: ")
        
        if choice == '1': import_csv('contacts.csv')
        elif choice == '2': export_json()
        elif choice == '3': import_json()
        elif choice == '4': execute_search_function()
        elif choice == '5': filter_and_sort()
        elif choice == '6': paginated_navigation()
        elif choice == '7': proc_add_phone()
        elif choice == '8': proc_move_group()
        elif choice == '9': break

if __name__ == "__main__":
    main()