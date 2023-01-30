from .log import LOGGER
import psycopg2 as pg
import pandas as pd

class Database:
    def __init__(
            self, 
            DATABASE_HOST,
            DATABASE_USERNAME,
            DATABASE_PASSWORD,
            DATABASE_NAME,
            DATABASE_PORT
        ):
        self.host = DATABASE_HOST,
        self.username = DATABASE_USERNAME
        self.password = DATABASE_PASSWORD
        self.dbname = DATABASE_NAME,
        self.port = DATABASE_PORT,
        self.conn = None

    def connect(self):
        '''Connect to a Postgres database'''
        if self.conn is None:
            try:
                self.conn = pg.connect(host = self.host[0], user = self.username, password = self.password, dbname = self.dbname[0])
            except Exception as e:
                self.conn.close()
                LOGGER.error(e)                
                raise e
            finally:
                LOGGER.info('Connection opened successfully')
    

    
    def select_id(self, query):
        '''return id after insert data into table currency.forecast'''
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            id = cur.fetchone()[0]
            self.conn.commit() 
            cur.close()            
            return id


    def select_rows_df(self, query):
        try:
            '''return dataframe from table'''
            self.connect()
            df_record = pd.read_sql(query, self.conn)
            LOGGER.info(f'{len(df_record)} returned successfully')
            return df_record
        except Exception as e:
            LOGGER.error(e)                
            raise e


    def select_rows(self, query):
        '''return rows from table without columns name'''
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            records = cur.fetchall()
        cur.close()
        return records


    def insert_rows(self, query):
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()
            cur.close()            
        
            return cur.rowcount

        
    def connection_check(self):
        self.conn.close()
            