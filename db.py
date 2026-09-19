import sqlite3
from utils.logger import logger


class Users:
    def __init__(self):
        self.db_path = 'db/users.db'


    def get_connection(self):
        return sqlite3.connect(self.db_path)


    def init_db(self):
        try:
            logger.info('DB | init_db')


            with self.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS Users (
                        user_id INTEGER PRIMARY KEY,
                        name TEXT,
                        nickname TEXT,
                        count INTEGER DEFAULT 0
                    )
                    '''
                )

                conn.commit()


        except Exception as e:
            logger.error(f'DB | error during db initialization: {e}')


    def add_user(self, user_id, name, nickname):
        try:
            logger.info('DB | add_user')

            with self.get_connection() as conn:
                cursor = conn.cursor()


                cursor.execute('SELECT user_id FROM Users WHERE user_id = ?', (user_id,))
                user = cursor.fetchone()


                if user is None:
                    cursor.execute(
                        '''INSERT INTO Users (user_id, name, nickname)
                           VALUES (?, ?, ?)''',
                        (user_id, name, nickname,)
                    )

                conn.commit()



        except Exception as e:
            logger.error(f'DB | error when adding a user: {e}')



    def update_count(self, user_id):
        try:
            logger.info('DB | update_count')
            with self.get_connection() as conn:
                cursor = conn.cursor()


                cursor.execute('Update Users SET count = count + 1 WHERE user_id = ?', (user_id, ))


                conn.commit()


        except Exception as e:
            logger.error(f'DB | error when update count: {e}')