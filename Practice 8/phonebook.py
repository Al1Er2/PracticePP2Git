import os
from connect import get_connection

def run_search():
    pattern = input("Enter search term: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
            for row in cur.fetchall():
                print(row)

def run_upsert():
    fname = input("First Name: ")
    lname = input("Last Name: ")
    phone = input("Phone: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_contact(%s, %s, %s)", (fname, lname, phone))
        conn.commit()
    print("Upsert successful.")

def run_bulk_insert():
    # Example lists (In a real app, these would come from a file or multi-input)
    names = ['John', 'Jane', 'BadNum']
    surnames = ['Doe', 'Smith', 'Error']
    phones = ['1234567', '9876543', '123'] # '123' is too short, will fail
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            # We pass an empty array for the INOUT parameter
            cur.execute("CALL bulk_insert_contacts(%s, %s, %s, %s)", (names, surnames, phones, []))
            failed = cur.fetchone()[0]
            print(f"Bulk insert finished. Failed items: {failed}")
        conn.commit()

def run_pagination():
    limit = int(input("How many records per page? "))
    offset = int(input("How many records to skip (offset)? "))
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
            for row in cur.fetchall():
                print(row)

def run_delete():
    target = input("Enter name or phone to delete: ")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact_proc(%s)", (target,))
        conn.commit()
    print("Delete procedure called.")

if name == "__main__":
    # Simple menu to test the new procedures
    print("1. Search | 2. Upsert | 3. Bulk Insert | 4. Paginate | 5. Delete")
    choice = input("Select: ")
    if choice == '1': run_search()
    elif choice == '2': run_upsert()
    elif choice == '3': run_bulk_insert()
    elif choice == '4': run_pagination()
    elif choice == '5': run_delete()
