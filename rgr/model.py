import psycopg2
import time

class Model:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='booking_online',
            user='postgres',
            password='38743874',
            host='localhost',
            port=5432
        )

    def get_all_tables(self):
        c = self.conn.cursor()
        c.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        return c.fetchall()

    def get_all_columns(self, table_name):
        c = self.conn.cursor()
        c.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s", (table_name,))
        return c.fetchall()

    def add_data(self, table_name, columns, val):
        c = self.conn.cursor()
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(val))

        identifier_column = f'{table_name[:-1]}_id' if table_name.endswith('s') else f'{table_name}_id'
        c.execute(f'SELECT "{identifier_column}" FROM "public"."{table_name}"')
        existing_identifiers = [item[0] for item in c.fetchall()]

        if int(val[columns.index(identifier_column)]) in existing_identifiers:
            return 2

        external_keys = [col for col in columns if col.endswith('_id') and col != identifier_column]
        for key_column in external_keys:
            referenced_table = key_column[:-3] + 's'
            c.execute(f'SELECT "{key_column}" FROM "public"."{referenced_table}"')
            if int(val[columns.index(key_column)]) not in [item[0] for item in c.fetchall()]:
                return 3

        c.execute(f'INSERT INTO "public"."{table_name}" ({columns_str}) VALUES ({placeholders})', val)
        self.conn.commit()
        return 1

    def update_data(self, table_name, column, id, new_value):
        c = self.conn.cursor()
        identifier_column = f'{table_name[:-1]}_id' if table_name.endswith('s') else f'{table_name}_id'

        if column.endswith('_id') and column != identifier_column:
            referenced_table = column[:-3] + 's'
            c.execute(f'SELECT "{column}" FROM "public"."{referenced_table}"')
            if int(new_value) not in [item[0] for item in c.fetchall()]:
                return 3

        c.execute(f'UPDATE "public"."{table_name}" SET "{column}" = %s WHERE "{identifier_column}" = %s',
                  (new_value, id))
        self.conn.commit()
        return 1

    def delete_data(self, table_name, id):
        c = self.conn.cursor()
        identifier_column = f'{table_name[:-1]}_id' if table_name.endswith('s') else f'{table_name}_id'

        c.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = "
                  "'BASE TABLE'")
        tables = [item[0] for item in c.fetchall()]

        for current_table in tables:
            if current_table == table_name:
                continue

            c.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s", (current_table,))
            if identifier_column in [col[0] for col in c.fetchall()]:
                c.execute(f'SELECT "{identifier_column}" FROM "public"."{current_table}"')
                if id in [item[0] for item in c.fetchall()]:
                    return 0

        c.execute(f'DELETE FROM "public"."{table_name}" WHERE "{identifier_column}" = %s', (id,))
        self.conn.commit()
        return 1

    def generate_data(self, table_name, count):
        c = self.conn.cursor()
        c.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s", (table_name,))
        columns_info = c.fetchall()

        id_column = f'{table_name[:-1]}_id'

        for i in range(count):
            insert_query = f'INSERT INTO "public"."{table_name}" ('
            select_subquery = ""

            for column_info in columns_info:
                column_name = column_info[0]
                column_type = column_info[1]

                if column_name == id_column:
                    c.execute(f'SELECT max("{id_column}") FROM "public"."{table_name}"')
                    max_id = c.fetchone()[0] or 0
                    select_subquery += f'{max_id + 1},'
                elif column_name == 'role':
                    select_subquery += "(CASE WHEN RANDOM() < 0.5 THEN 'tenant' ELSE 'landlord' END),"
                elif column_name == 'email':
                    select_subquery += f"'user{i}@example.com',"
                elif column_name.endswith('_id'):
                    related_table_name = column_name[:-3].capitalize()
                    c.execute(
                        f'SELECT {related_table_name.lower()}_id FROM "public"."{related_table_name}" ORDER BY RANDOM() LIMIT 1')
                    related_id = c.fetchone()[0]
                    select_subquery += f'{related_id},'
                elif column_type == 'integer':
                    select_subquery += f'trunc(random()*100)::INT,'
                elif column_type == 'character varying':
                    select_subquery += f"'Text {column_name} {i}',"
                elif column_type == 'date':
                    select_subquery += "'2024-01-01',"
                elif column_type == 'timestamp with time zone':
                    select_subquery += "'2024-01-01 00:00:00+03',"
                else:
                    continue

                insert_query += f'"{column_name}",'

            insert_query = insert_query.rstrip(',') + f') VALUES ({select_subquery[:-1]})'
            c.execute(insert_query)

        self.conn.commit()

    def search_data(self, table1, table2, query_type, filter_conditions):
        c = self.conn.cursor()
        params = []

        if query_type == '1':
            query = f"""
                SELECT * 
                FROM "public"."{table1}" t1
                JOIN "public"."{table2}" t2 ON t1.user_id = t2.user_id
                WHERE 1=1
            """
            if 'price_min' in filter_conditions and 'price_max' in filter_conditions:
                query += " AND t2.price BETWEEN %s AND %s"
                params.extend([filter_conditions['price_min'], filter_conditions['price_max']])

            if 'title' in filter_conditions and 'title' in query:
                query += " AND t2.title LIKE %s"
                params.append(f"%{filter_conditions['title']}%")

        elif query_type == '2':
            query = f"""
                SELECT * 
                FROM "public"."{table1}" t1
                JOIN "public"."{table2}" t2 ON t1.rental_id = t2.rental_id
                WHERE 1=1
            """
            if 'price_min' in filter_conditions and 'price_max' in filter_conditions:
                query += " AND t1.price BETWEEN %s AND %s"
                params.extend([filter_conditions['price_min'], filter_conditions['price_max']])

            if 'title' in filter_conditions and 'title' in query:
                query += " AND t1.title LIKE %s"
                params.append(f"%{filter_conditions['title']}%")

        elif query_type == '3':
            query = f"""
                SELECT * 
                FROM "public"."{table1}" t1
                JOIN "public"."{table2}" t2  ON t1.rental_id = t2.rental_id
                WHERE 1=1
            """

            if 'price_min' in filter_conditions and 'price_max' in filter_conditions:
                query += " AND t1.price BETWEEN %s AND %s"
                params.extend([filter_conditions['price_min'], filter_conditions['price_max']])

            if 'title' in filter_conditions and 'title' in query:
                query += " AND t1.title LIKE %s"
                params.append(f"%{filter_conditions['title']}%")

        else:
            raise ValueError("Incorrect query")

        if 'name' in filter_conditions and 'name' in query:
            query += " AND t1.name LIKE %s"
            params.append(f"%{filter_conditions['name']}%")

        if 'email' in filter_conditions and 'email' in query:
            query += " AND t1.email LIKE %s"
            params.append(f"%{filter_conditions['email']}%")

        if 'rating_min' in filter_conditions and 'rating_max' in filter_conditions:
            query += " AND t2.rating BETWEEN %s AND %s"
            params.extend([filter_conditions['rating_min'], filter_conditions['rating_max']])

        if 'group_by' in filter_conditions:
            query += " GROUP BY " + ", ".join(filter_conditions['group_by'])

        start_time = time.time()
        c.execute(query, tuple(params))
        result = c.fetchall()
        end_time = time.time()

        execution_time = (end_time - start_time) * 1000
        print(f"Query executed in: {execution_time:.2f} ms")

        return result
