import db_creation


class ReportCreation:

    def __init__(self):
        pass

    def return_incoming_data(self):
        conn_obj = db_creation.Connection()
        sql_query = "Select sum(amount), settleDate from data where instruction = 'S' group by settleDate"
        cursor = conn_obj.conn.cursor()
        result = cursor.execute(sql_query)
        print "---------------- Incoming Amount settled -------------"
        for i in result.fetchall():
            print "Amount %s - Settle Date %s" % (i[0], i[1])

    def return_outgoing_data(self):
        conn_obj = db_creation.Connection()
        sql_query = "Select sum(amount), settleDate from data where instruction = 'B' group by settleDate"
        cursor = conn_obj.conn.cursor()
        result = cursor.execute(sql_query)
        print "\n"
        print "---------------- Outgoing Amount settled -------------"
        for i in result.fetchall():
            print "Amount %s - Settlement Date %s" % (i[0], i[1])

    def return_incoming_ranking(self, date=None):
        conn_obj = db_creation.Connection()
        sql_income_query = "Select sum(amount) as amount, entity  from data where "
        if date is not None:
            sql_income_query += "settleDate = '%s' and " % date
        sql_income_query += "instruction = 'S' group by entity order by amount desc"
        cursor = conn_obj.conn.cursor()
        result = cursor.execute(sql_income_query)
        count = 1
        print "\n"
        print "----------- Ranking for Incoming Amount --------------"
        for i in result.fetchall():
            print "Rank %s - Entity %s" % (count, i[1])
            count += 1
        print "------------------------------------------------------"

    def return_outgoing_ranking(self, date=None):
        conn_obj = db_creation.Connection()
        sql_outgoing_query = "Select sum(amount) as amount, entity from data where "
        if date is not None:
            sql_outgoing_query += "settleDate = '%s' and " % date
        sql_outgoing_query += "instruction = 'B' group by entity order by amount desc"
        cursor = conn_obj.conn.cursor()
        result = cursor.execute(sql_outgoing_query)
        count = 1
        print "\n"
        print "----------- Ranking for Outgoing Amount --------------"
        for i in result.fetchall():
            print "Rank %s - Entity %s" % (count, i[1])
            count += 1
        print "------------------------------------------------------"

    def return_entity_ranking(self, date=None):
        self.return_incoming_ranking(date)
        self.return_outgoing_ranking(date)
