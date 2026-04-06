import psycopg2
import csv
import os

# 🔗 Database connection
conn = psycopg2.connect(
    host="localhost",
    database="suppliers",
    user="postgres",
    password="@Klaus"
)
cur = conn.cursor()


# 📁 Get current directory
BASE_DIR = os.getcwd()


# 📌 Show files in current folder
def show_files():
    print("\n📁 Files in current directory:")
    for file in os.listdir(BASE_DIR):
        print("-", file)


# 📌 Insert from CSV (improved)
def insert_from_csv(filename):
    filepath = os.path.join(BASE_DIR, filename)

    if not os.path.exists(filepath):
        print("❌ File not found!")
        show_files()
        return

    try:
        with open(filepath, "r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                cur.execute(
                    "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                    (row[0], row[1])
                )

        conn.commit()
        print("✅ CSV data inserted successfully.")

    except Exception as e:
        print("❌ Error:", e)


# 📌 Insert manually
def insert_manual():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()

    if not name or not phone:
        print("❌ Name and phone cannot be empty!")
        return

    try:
        cur.execute(
            "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
            (name, phone)
        )
        conn.commit()
        print("✅ Contact added.")

    except Exception as e:
        print("❌ Error:", e)


# 📌 Update contact
def update_contact():
    print("1 - Update name")
    print("2 - Update phone")
    choice = input("Choose: ").strip()

    try:
        if choice == "1":
            phone = input("Enter phone: ")
            new_name = input("New name: ")

            cur.execute(
                "UPDATE phonebook SET first_name = %s WHERE phone = %s",
                (new_name, phone)
            )

        elif choice == "2":
            name = input("Enter name: ")
            new_phone = input("New phone: ")

            cur.execute(
                "UPDATE phonebook SET phone = %s WHERE first_name = %s",
                (new_phone, name)
            )

        else:
            print("❌ Invalid option")
            return

        conn.commit()
        print("✅ Updated successfully.")

    except Exception as e:
        print("❌ Error:", e)


# 📌 Query contacts
def query_contacts():
    print("1 - Search by name")
    print("2 - Search by phone prefix")
    choice = input("Choose: ").strip()

    try:
        if choice == "1":
            name = input("Enter name: ")
            cur.execute(
                "SELECT * FROM phonebook WHERE first_name ILIKE %s",
                ("%" + name + "%",)
            )

        elif choice == "2":
            prefix = input("Enter prefix: ")
            cur.execute(
                "SELECT * FROM phonebook WHERE phone LIKE %s",
                (prefix + "%",)
            )

        else:
            print("❌ Invalid option")
            return

        rows = cur.fetchall()

        if rows:
            print("\n📋 Results:")
            for row in rows:
                print(row)
        else:
            print("❗ No results found.")

    except Exception as e:
        print("❌ Error:", e)


# 📌 Delete contact
def delete_contact():
    print("1 - Delete by name")
    print("2 - Delete by phone")
    choice = input("Choose: ").strip()

    try:
        if choice == "1":
            name = input("Enter name: ")
            cur.execute(
                "DELETE FROM phonebook WHERE first_name = %s",
                (name,)
            )

        elif choice == "2":
            phone = input("Enter phone: ")
            cur.execute(
                "DELETE FROM phonebook WHERE phone = %s",
                (phone,)
            )

        else:
            print("❌ Invalid option")
            return

        conn.commit()
        print("✅ Deleted successfully.")

    except Exception as e:
        print("❌ Error:", e)


# 📌 Main menu
def menu():
    print("📂 Working directory:", BASE_DIR)

    while True:
        print("\n--- PHONEBOOK ---")
        print("1. Insert from CSV")
        print("2. Insert manually")
        print("3. Update contact")
        print("4. Search contacts")
        print("5. Delete contact")
        print("6. Show files in folder")
        print("0. Exit")

        choice = input("Select option: ").strip()

        if not choice:
            print("❗ Enter a number!")
            continue

        if choice == "1":
            filename = input("Enter CSV filename: ")
            insert_from_csv(filename)

        elif choice == "2":
            insert_manual()

        elif choice == "3":
            update_contact()

        elif choice == "4":
            query_contacts()

        elif choice == "5":
            delete_contact()

        elif choice == "6":
            show_files()

        elif choice == "0":
            break

        else:
            print("❌ Invalid choice!")


# 🚀 Run
menu()

# 🔚 Close connection
cur.close()
conn.close()