import os
import hashlib
from dao import DAO

class UserExistsError(RuntimeError):
    def __init__(self, username) -> None:
        super().__init__(f"User exists: {username}")

class User:
    def __init__(self, username: str, key: str, salt: str) -> None:
        self.username = username
        self.key = key
        self.salt = salt

    def make_key(self, password):
        return hashlib.pbkdf2_hmac('sha256',
                                   password.encode('utf-8'),
                                   self.salt,
                                   100000)

class UserDAO(DAO):
    def _data(self, user: User):
        return (user.username, user.key, user.salt)

    def new(self, username: str, password: str):
        if self.__user_exists(username):
            raise UserExistsError(username)
        salt = os.urandom(32)
        usr = User(username, "", salt)
        key = usr.make_key(password)
        usr.key = key
        return usr

    def get_user(self, username):
        sql = f'''SELECT * FROM {self._get_table_name()}
                  WHERE (username=:username)'''
        res = self.cursor.execute(sql, (username,)).fetchone()
        if not res:
            return None
        key = res[1]
        salt = res[2]
        return User(username, key, salt)

    def get_user_by_id(self, rowid):
        sql = f'''SELECT * FROM {self._get_table_name()}
                    WHERE (rowid=:rowid)'''
        res = self.cursor.execute(sql, (rowid,)).fetchone()
        username = res[0]
        key = res[1]
        salt = res[2]
        return User(username, key, salt)

    def get_user_id(self, username):
        sql = f'''SELECT rowid FROM {self._get_table_name()}
                  WHERE username = :username'''
        res = self.cursor.execute(sql, (username,)).fetchone()
        return res[0]

    def fetch_all(self):
        entries = super().fetch_all()
        return list(map(lambda x: User(x[1], x[2], x[3]), entries))

    def create_table(self):
        sql = f'''CREATE TABLE IF NOT EXISTS {self._get_table_name()}
                        (username text unique, key text, salt text)'''
        self.cursor.execute(sql)

    def _store_sql(self):
        return f'''INSERT INTO {self._get_table_name()}
                        VALUES (:username, :key, :salt)'''

    def _get_table_name(self):
        return 'users'

    def __user_exists(self, username):
        sql = f'''SELECT EXISTS(SELECT 1 FROM {self._get_table_name()}
                    WHERE username=:username)'''
        res = self.cursor.execute(sql, (username,))
        return res.fetchone()[0] == 1
