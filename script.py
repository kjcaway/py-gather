"""
    file: script.py
    description: this is script that read data and parse/extract new data
    date: 2023-04-30
    author: x
"""
import sys
import argparse
import logging

import pymysql
import pandas as pd

host = "localhost"
port = 3306
database = "test"
username = "root"
password = "1234"

import_file = "./in.csv"
export_file = "./out.csv"


def mysql_read():
    try:
        # connect db
        conn = pymysql.connect(host=host, user=username, passwd=password, db=database, use_unicode=True, charset='utf8')
        cursor = conn.cursor()

    except Exception:
        logging.exception("failed conn")
        sys.exit(1)
    
    # execute sql
    sql = "SELECT * FROM tbl_member_detail"
    cursor.execute(sql)
    
    # fetch data and extract columns
    rows = cursor.fetchall()
    field_names = [i[0] for i in cursor.description]

    # convert tuple to list
    list = []
    for row in rows:
        list.append(row)
    print(list)

    # list to df
    df = pd.DataFrame(list, columns=field_names)
    print(df)

    # convert df to csv
    df.to_csv(export_file, index = False)

    conn.close()


def csv_read():
    # read csv file
    df = pd.read_csv('./in.csv')
    print(df)


"""
--input / -i arguments
"""
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', nargs=1, help='please typing "mysql" or "csv"', dest='input_type', required=True)

    input_type = parser.parse_args().input_type

    return input_type


if __name__ == '__main__':
    input_type = get_arguments()
    if input_type[0] == 'mysql':
        mysql_read()
    elif input_type[0] == 'csv':
        csv_read()
    else:
        print("please select type use '-i'")
