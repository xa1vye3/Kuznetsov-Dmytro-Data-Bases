import time


class View:
    def show_menu(self):
        while True:
            print("Menu:")
            print("1. Display table names")
            print("2. Display column names of a table")
            print("3. Add data to a table")
            print("4. Update data in a table")
            print("5. Delete data from a table")
            print("6. Generate data for a table")
            print("7. Search data")
            print("8. Exit")

            choice = input("Make a choice: ")

            if choice in ('1', '2', '3', '4', '5', '6', '7', '8'):
                return choice
            else:
                print("Please enter a valid option number (1 to 8)")
                time.sleep(2)

    def show_message(self, message):
        print(message)
        time.sleep(2)

    def ask_continue(self):
        agree = input("Continue making changes? (y/n) ")
        return agree

    def show_tables(self, tables):
        print("Table names:")
        for table in tables:
            print(table)
        time.sleep(2)

    def ask_table(self):
        table_name = input("Enter the table name: ")
        return table_name

    def show_columns(self, columns):
        print("Column names:")
        for column in columns:
            print(column)
        time.sleep(2)

    def insert(self):
        while True:
            try:
                table = input("Enter the table name: ")
                columns = input("Enter column names (space-separated): ").split()
                val = input("Enter corresponding values (space-separated): ").split()

                if len(columns) != len(val):
                    raise ValueError("The number of columns must match the number of values.")

                return table, columns, val
            except ValueError as e:
                print(f"Error: {e}")

    def update(self):
        while True:
            try:
                table = input("Enter the table name: ")
                column = input("Enter the name of the column to update: ")
                id = int(input("Enter the ID of the row to update: "))
                new_value = input("Enter the new value: ")
                return table, column, id, new_value
            except ValueError as e:
                print(f"Error: {e}")

    def delete(self):
        while True:
            try:
                table = input("Enter the table name: ")
                id = int(input("Enter the ID of the row to delete: "))
                return table, id
            except ValueError as e:
                print(f"Error: {e}")

    def generate_data_input(self):
        while True:
            try:
                table_name = input("Enter the table name: ")
                num_rows = int(input("Enter the number of rows to generate: "))
                return table_name, num_rows
            except ValueError as e:
                print(f"Error: {e}")

    def search_data_input(self):
        while True:
            try:
                print("\nEnter search parameters:")

                price_min = input("Minimum price: ")
                price_max = input("Maximum price: ")
                name = input("Name (LIKE pattern): ")
                email = input("Email (LIKE pattern): ")
                title = input("Title (LIKE pattern): ")

                filter_conditions = {
                    'price_min': int(price_min) if price_min else None,
                    'price_max': int(price_max) if price_max else None,
                    'name': name if name else None,
                    'email': email if email else None,
                    'title': title if title else None,
                    'group_by': ['t1.user_id', 't2.rental_id']
                }
                return filter_conditions
            except ValueError as e:
                print(f"Error: {e}")
