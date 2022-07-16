import os, json, csv
import httplib2, psycopg2
import pandas as pd
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import records


def get_service_simple():
    return build('sheets', 'v4', developerKey=records.api_key)


def get_service_sacc():
    cred_json = os.path.dirname(__file__) + "/records/task-for-numbers-90c076f1fd41.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    cred_service = ServiceAccountCredentials.from_json_keyfile_name(cred_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=cred_service)


service = get_service_sacc()
sheet = service.spreadsheets()


sheet_id = "1uDGhTSWObNi5tP86U5eNvGv6kZ1kVl7DNXGCj_0as9E"

resp = sheet.values().batchGet(spreadsheetId=sheet_id, ranges="Лист1!A1:E51", majorDimension='ROWS').execute()

df = pd.DataFrame(resp)

with open('records/data.json', 'r+') as f_empty:
    pass

with open('records/data.json', 'w', encoding='utf-8') as f:
    for row in df.iterrows():
        row[1].to_json(f, orient='records')
        f.write("\n")
        f.close()
with open('records/data.json', 'r+') as fl:
    j = json.load(fl)
    data = j[1]['values'][1:51]

    with open('records/data_csv.csv', 'r+') as csv_clearn:
        pass
        csv_clearn.close()

    headerList = ["number", "order_number", "price_usd", "delivery_date", "price_rub"]
    with open('records/data_csv.csv', 'w', newline='') as csv_file:
        csvwriter = csv.writer(csv_file, delimiter=';')
        csvwriter.writerow(headerList)
        csvwriter.writerows(data)
        csv_file.close()


#   Функция соединения к базе данных PorstgreSQL
def conn_db():
    connect = psycopg2.connect(database="postgres",
                                host="127.0.0.1",
                                port="5432",
                                user="postgres",
                                password="admin")
    return connect


#   Функция удаления таблицы
def clear_table():
    connect = conn_db()
    cursor = connect.cursor()
    cursor.execute('''DROP TABLE test_1;''')
    connect.commit()
    cursor.close()
    connect.close()
    return print('Table cleared!')


#   Функция создания новой таблицы
def create_table():
    connect = conn_db()
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE test_1 (number TEXT NOT NULL,
                                            order_number TEXT NOT NULL,
                                            price_usd TEXT NOT NULL,
                                            delivery_date TEXT NOT NULL,
                                            price_rub TEXT NOT NULL);''')

    with open('records/data_csv.csv', 'r') as f_csv:
        next(f_csv)
        cursor.copy_from(f_csv, 'test_1', sep=';', columns=["number", "order_number",
                                                            "price_usd", "delivery_date", "price_rub"])
        f_csv.close()
    connect.commit()
    cursor.close()
    connect.close()
    return print('Table created and data written from csv file!')


if __name__ == '__main__':
    conn_db()
    clear_table()
    create_table()
