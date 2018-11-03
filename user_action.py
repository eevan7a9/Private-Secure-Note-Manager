from sqlite3 import connect
from datetime import datetime
from passlib.hash import pbkdf2_sha256


class UserDb:

    def __init__(self):
        self.con = connect("storage_note.db")
        self.cur = self.con.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS userTbl(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    username VARCHAR(255),
                                    password VARCHAR (255),
                                    created_at VARCHAR(255))""")
        self.con.commit()

    def insert_user(self, user_name, user_password):

        hashed_password = self.hash_password(user_password)
        created_at = datetime.now().strftime('%Y-%M-%d %I:%M %p')

        self.cur.execute("""INSERT INTO userTbl(username, password, created_at)VALUES (?,?,?)""",
                         (user_name, hashed_password, created_at))
        self.con.commit()

    def check_username(self, username):

        self.cur.execute("""SELECT * FROM userTbl WHERE username = ?""")
        query_result = self.cur.fetchone()
        for user in query_result:
            result = user

            return result

    def update_password(self, user_id, new_password):
        hashed_password = self.hash_password(new_password)

        self.cur.execute("""UPDATE userTbl set password = ? WHERE id = ?""", (hashed_password, user_id))
        self.con.commit()

    def get_password(self, user_name):
        input_name = user_name
        self.cur.execute("""SELECT password FROM userTbl WHERE username=?""", (input_name, ))
        result = self.cur.fetchone()
        return result

    def get_user_info(self,info, user_name):
        input_name = user_name
        self.cur.execute("""SELECT {} From main.userTbl WHERE username = ?""".format(info),(input_name,))
        result = self.cur.fetchone()
        return result

    def verify_password(self, user_name, user_password):
        input_password = user_password
        for row in self.get_password(user_name):
            database_password = row

            result = pbkdf2_sha256.verify(input_password, database_password)
            return result

    @staticmethod
    def hash_password(user_password):
        hashed_password = pbkdf2_sha256.hash(user_password)
        return hashed_password

# x = UserDb()
# input = "user3"
# x.check_username()

