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
export_file = "./result.csv"


def mysql_read():
    try:
        # DB Connection
        conn = pymysql.connect(host=host, user=username, passwd=password, db=database, use_unicode=True, charset='utf8')
        cursor = conn.cursor()

    except Exception:
        logging.exception("failed conn")
        sys.exit(1)
    
    # SQL문 실행 및 Fetch
    sql = "SELECT * FROM tbl_member_detail"
    cursor.execute(sql)
    
    # 데이타 Fetch, 컬럼명 find
    rows = cursor.fetchall()
    field_names = [i[0] for i in cursor.description]

    # tuple to list
    list = []
    for row in rows:
        list.append(row)
    
    print(list)

    # list to DataFrame
    df = pd.DataFrame(list, columns=field_names)
    print(df)

    # to csv
    df.to_csv(export_file, index = False)

    conn.close()


def csv_read():
    print("csv")


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