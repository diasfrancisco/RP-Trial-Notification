import psycopg2

import config


class DatabaseStorage:
    def __init__(self):
        self.conn = psycopg2.connect(
                host = config.DB_CREDENTIALS['host'],
                database = config.DB_CREDENTIALS['database'],
                port = config.DB_CREDENTIALS['port'],
                user = config.DB_CREDENTIALS['credentials']['username'],
                password = config.DB_CREDENTIALS['credentials']['password']
            )
    
    def _get_db_details(self):
        """
        Creates a database connection
        """        
        conn = None
        
        try:
            print('Connecting to PostgreSQL database...')
            conn = self.conn
            
            cur = conn.cursor()
            
            print('Postgres Database version: ')
            cur.execute('SELECT version()')
            
            db_version = cur.fetchone()
            print(db_version)
            
            cur.close()
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed')
                
    def create_table(self):
        conn = None
        
        try:
            print('Connecting to PostgreSQL database...')
            conn = self.conn
            
            cur = conn.cursor()
            cur.execute(
                '''
                SELECT EXISTS (
                    SELECT *
                    FROM information_schema.tables
                    WHERE
                        table_schema = 'public' AND
                        table_name = 'rp_trials'
                );
                '''
            )
            does_table_exist = cur.fetchone()
            
            if does_table_exist[0]:
                print('Table exists')
                cur.close()
            else:
                print('Creating table...')
                cur.execute(
                    '''
                    CREATE TABLE rp_trials (
                        id VARCHAR(30),
                        title VARCHAR(255),
                        authors VARCHAR(255),
                        organization VARCHAR(255),
                        summary VARCHAR(1000),
                        start_date DATE,
                        primary_date DATE,
                        end_date DATE
                    );
                    '''
                )
                print('Created table')
                conn.commit()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed')
                
    def query_ids(self):
        pass
    
    def insert_data(self):
        pass
    
    
def test():
    db_test = DatabaseStorage()
    # db_test._get_db_details()
    db_test.create_table()
    
test()