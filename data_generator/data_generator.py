import yaml
from faker import Faker
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def get_users():
    fake = Faker('ko_KR')
    users = []

    cust_ids = [i for i in range(0, 5982)]
    for cust_id in cust_ids:
        simple_profile = {'userid': cust_id}
        simple_profile.update(fake.simple_profile())
        users.append(simple_profile)

    return users

def get_orders(data_path):
    df_train = pd.read_csv(data_path+"\\train_transactions.csv")
    df_test = pd.read_csv(data_path+"\\test_transactions.csv")
    df = pd.concat([df_train, df_test]).reset_index(drop=True)
    df = df.reset_index(drop=False)
    df = df.rename(columns={"index": "transactionid"})
    return df

class DatabaseConnect:
    def __init__(self, db_conn):
        self.host = db_conn['host']
        self.username = db_conn['username']
        self.password = db_conn['pw']
        self.database = db_conn['database']
        self.port = db_conn['port']
        self.url = "postgresql://{}:{}@{}:{}/{}".format(self.username, self.password, self.host, self.port, self.database)
        self.engine = create_engine(self.url)
        self.conn = psycopg2.connect(self.url)
        
    def __enter__(self):
        if self.conn is not None:
            self.cursor = self.conn.cursor()
            return self
        else:
            raise IOError("Cannot access DB File")
            
    def __exit__(self, e_type, e_value, tb):
        self.cursor.close()
        self.conn.close()
        print("Closing Database")
        
    def create(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        print("Create Complete!")
        
    def insert(self, users, df):
        user_placeholder = ', '.join(["%s" for _ in range(len(users[0]))])
        insert_sql = f"INSERT INTO store.customers VALUES ({user_placeholder});"
        for cust_id, user in enumerate(users):
            self.cursor.execute(insert_sql, list(user.values()))
            self.conn.commit()
        df.to_sql('orders', self.engine, schema='store', index=False, if_exists='replace')
        print("Insert Complete!")

if __name__ == "__main__":

    with open('data_generator.yaml') as f:
        db_conn = yaml.load(f, Loader=yaml.FullLoader)
    
    users = get_users()
    orders = get_orders(db_conn['data_path'])

    with DatabaseConnect(db_conn) as db:

        db.create(open("create.sql", "r").read())
        db.insert(users, orders)