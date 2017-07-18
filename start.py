import csv
import datetime
import db_creation
import create_report


def return_days_number_to_add(day_number, currency):
    global days_to_add
    days_to_add = 0
    if currency in ('AED', 'SAR'):
        week_range_list = range(1, 5) + [7]
        week_end_day = 7
        if day_number not in week_range_list:
            days_to_add = week_end_day - day_number
    else:
        week_range_list = range(1, 6)
        week_end_day = 8
        if day_number not in week_range_list:
            days_to_add = week_end_day - day_number
    return days_to_add


def settle_trade(settle_date, price, units, agreed_fx, currency):
    amount_in_usd = int(float(price)*int(units)*float(agreed_fx))
    settlement_date_in_format = datetime.datetime.strptime(settle_date, '%d-%m-%Y').date()
    week_number = settlement_date_in_format.isoweekday()
    days_to_add = return_days_number_to_add(week_number, currency)
    next_settle_date = settlement_date_in_format + datetime.timedelta(days=days_to_add)
    final_settle_date = next_settle_date.strftime('%d-%m-%Y')
    return amount_in_usd, final_settle_date


# Create a connection
conn = db_creation.Connection()

# Delete the table if exists
conn.delete_table()

# Create the table if exists
conn.create_table()

# Open the file
file_name = "sample.csv"
file_obj = open(file_name)

# Reading the content of file
read_content = csv.reader(file_obj)

# Skip the header row
next(read_content, None)

for content in read_content:
    agreed_fx = content[2]
    settlement_date = content[5]
    units = content[6]
    price = content[7]
    currency = content[3]
    entity = content[0]
    instruction = content[1]
    out_values = settle_trade(settlement_date, price, units, agreed_fx, currency)
    # Inserting the final settlement data
    conn.insert_data(entity, instruction, out_values[0], out_values[1])

# Show the report now
report_obj = create_report.ReportCreation()

# Report 1 - Amount in USD settled incoming everyday
report_obj.return_incoming_data()

# Report 2 - Amount in USD settled outgoing everyday
report_obj.return_outgoing_data()

# Report 3 - Ranking based on entities on outgoing & incoming amount
report_obj.return_entity_ranking()

# Close the database connection
conn.close_connection()
