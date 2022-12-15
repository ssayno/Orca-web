import os.path

import pandas as pd
import sqlite3


def extract_and_storage(file_path):
    data = pd.read_excel(file_path, sheet_name='扣费汇总')
    packageNumbers = data['运单号']
    current_path = os.path.dirname(__file__)
    db_file = os.path.join(current_path, os.pardir, 'static', 'Data', 'orca.db')
    with sqlite3.connect(db_file) as connect:
        cursor = connect.cursor()
        create_table_sql = '''\
        create table if not exists packageNumbers(
        id text primary key
        )
        '''
        try:
            cursor.execute(create_table_sql)
            connect.commit()
        except Exception as e:
            print(e)
            connect.rollback()
        for packageNumber in packageNumbers:
            try:
                cursor.execute(
                    'insert into packageNumbers values(?)', (packageNumber,)
                )
                connect.commit()
            except Exception as e:
                print(e)
                connect.rollback()

        try:
            cursor.execute(
                'select count(id) from packageNumbers'
            )
            connect.commit()
        except Exception as e:
            print(e)
            connect.rollback()

        packages = cursor.fetchone()
        if packages is not None:
            packages = packages[0]
        else:
            packages = 0
        cursor.close()
    return packages
