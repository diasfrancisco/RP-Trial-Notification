import psycopg2

import config


class DatabaseStorage:
    def _get_db_details(self):
        """
        Grabs the details of the database
        """        
        conn = None
        
        try:
            conn = psycopg2.connect(
                host = config.DB_CREDENTIALS['host'],
                database = config.DB_CREDENTIALS['database'],
                port = config.DB_CREDENTIALS['port'],
                user = config.DB_CREDENTIALS['credentials']['username'],
                password = config.DB_CREDENTIALS['credentials']['password']
            )
            
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
                
    def create_table(self):
        conn = None
        
        try:
            conn = psycopg2.connect(
                host = config.DB_CREDENTIALS['host'],
                database = config.DB_CREDENTIALS['database'],
                port = config.DB_CREDENTIALS['port'],
                user = config.DB_CREDENTIALS['credentials']['username'],
                password = config.DB_CREDENTIALS['credentials']['password']
            )
            
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
                cur.close()
            else:
                cur.execute(
                    '''
                    CREATE TABLE rp_trials (
                        id VARCHAR(30),
                        title VARCHAR(1000),
                        authors VARCHAR(500),
                        organization VARCHAR(500),
                        summary VARCHAR(2000),
                        start_date VARCHAR(20),
                        primary_date VARCHAR(20),
                        end_date VARCHAR(20)
                    );
                    '''
                )
                conn.commit()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)
        finally:
            if conn is not None:
                conn.close()
                
    def query_ids(self):
        conn = None
        
        try:
            conn = psycopg2.connect(
                host = config.DB_CREDENTIALS['host'],
                database = config.DB_CREDENTIALS['database'],
                port = config.DB_CREDENTIALS['port'],
                user = config.DB_CREDENTIALS['credentials']['username'],
                password = config.DB_CREDENTIALS['credentials']['password']
            )
            
            cur = conn.cursor()
            cur.execute(
                '''
                SELECT id FROM rp_trials;
                '''
            )
            db_ids = cur.fetchall()
            cur.close()

            return db_ids
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)
        finally:
            if conn is not None:
                conn.close()
    
    def insert_data(self, trial):
        conn = None
        
        try:
            conn = psycopg2.connect(
                host = config.DB_CREDENTIALS['host'],
                database = config.DB_CREDENTIALS['database'],
                port = config.DB_CREDENTIALS['port'],
                user = config.DB_CREDENTIALS['credentials']['username'],
                password = config.DB_CREDENTIALS['credentials']['password']
            )
            
            cur = conn.cursor()
            cur.execute(
                f'''
                INSERT INTO rp_trials(id, title, authors, organization, summary, start_date, primary_date, end_date)
                VALUES ('{trial.id}', '{trial.title}', '{trial.authors}', '{trial.org}', '{trial.summary}', '{trial.start_date}', '{trial.primary_date}', '{trial.end_date}')
                '''
            )
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as err:
            print(err)
        finally:
            if conn is not None:
                conn.close()