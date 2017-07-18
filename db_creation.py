import sqlite3


TABLE_NAME = 'data'
DATABASE_FILE_NAME = 'data.db'


class Connection:

    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_FILE_NAME)
        self.cursor = self.conn.cursor()

    def delete_table(self):
        delete_table_query = "DROP table IF EXISTS %s" % TABLE_NAME
        self.cursor.execute(delete_table_query)

    def create_table(self):
        create_table_query = '''CREATE TABLE IF NOT EXISTS %s
             (entity text, instruction text, amount int, settleDate text)''' % TABLE_NAME
        self.cursor.execute(create_table_query)

    def insert_data(self, entity, instr, amount, settlement_date):
        sql_insert_query = "INSERT INTO %s VALUES ('%s', '%s', '%s', '%s')" \
                    % (TABLE_NAME, entity, instr, amount, settlement_date)
        self.cursor.execute(sql_insert_query)
        self.commit_action()

    def commit_action(self):
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
