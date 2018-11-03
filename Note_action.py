from user_action import UserDb
from datetime import datetime
import base64 as base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class NoteDb(UserDb):
    def __init__(self):
        super().__init__()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS noteTbl(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            title VARCHAR(255),
                                            topic VARCHAR (255),
                                            content VARCHAR (255),
                                            created_at VARCHAR(255),
                                            modified_at VARCHAR(255),
                                            created_by INT(11),
                                            FOREIGN KEY (created_by) REFERENCES userTbl(id))""")

    def create_note(self, title, topic, content, user_password, user_id):

        content_to_store = self.encrypt_content(content, user_password)
        created_at = datetime.now().strftime('%Y-%M-%d %I:%M %p')
        modified_at = datetime.now().strftime('%Y-%M-%d %I:%M %p')
        created_by = user_id

        self.cur.execute("""INSERT INTO noteTbl(title, topic, content, created_at, modified_at, created_by) VALUES
        (?, ?, ?, ?, ?, ?)""", (title, topic, content_to_store, created_at, modified_at, created_by))

        self.con.commit()

    def update_note(self, column_name, value, note_id, user_password=None):

        name_of_table_column = column_name
        inserted_value = value
        modified_at = datetime.now().strftime('%Y-%M-%d %I:%M %p')
        if name_of_table_column == 'content':
            encrypted_value = self.encrypt_content(inserted_value, user_password)

            self.cur.execute("""UPDATE noteTbl SET {} = ?, modified_at = ? WHERE id = ?""".format(name_of_table_column),
                             (encrypted_value, modified_at, note_id))
            self.con.commit()

        else:
            self.cur.execute("""UPDATE noteTbl SET {} = ?, modified_at = ? WHERE id = ?""".format(name_of_table_column),
                             (inserted_value, modified_at, note_id))
            self.con.commit()

    def remove_note(self, note_id):

        self.cur.execute("""DELETE FROM noteTbl where id = ?""", (note_id,))
        self.con.commit()

    def get_user_notes(self, table_column, value):

        self.cur.execute("""SELECT id, title, topic, content, created_at, modified_at FROM noteTbl 
        WHERE {} = ?""".format(table_column), (value,))
        result = self.cur.fetchall()
        return result

    def find_note(self, value, user_id):

        self.cur.execute("""SELECT id, title, topic, content, created_at, modified_at FROM noteTbl
        WHERE (title LIKE '{}%' OR topic LIKE '{}%') AND created_by = ?""".format(value, value),
                         (user_id,))
        result = self.cur.fetchall()
        return result

    def count_notes(self, user_id):

        self.cur.execute("""SELECT COUNT(id) FROM noteTbl WHERE created_by = ?""", (user_id,))
        result = self.cur.fetchone()
        return result

    @staticmethod
    def encrypt_content(text, user_password):

        # We Generate key for our encryption
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(user_password.encode("utf-8"))
        generated_key = base64.urlsafe_b64encode(digest.finalize())

        password_key = generated_key  # We encrypt the text with our generated key from users password
        key = Fernet(password_key)
        encoding = "utf-8"
        text_to_encrypt = text.encode(encoding)
        encrypted_text = key.encrypt(text_to_encrypt)

        return encrypted_text

    @staticmethod
    def decrypt_content(text, user_password):

        # Get the required key from users password
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(user_password.encode("utf-8"))
        generated_key = base64.urlsafe_b64encode(digest.finalize())

        password_key = generated_key  # We decrypt the text with required key from users password
        key = Fernet(password_key)
        encoding = "utf-8"  # to turn string to bytes for Debugging
        # decoded_text = key.decrypt(text.encode(encoding))
        decoded_text = key.decrypt(text)
        plain_text = decoded_text.decode("utf-8")

        return plain_text

x = NoteDb()
for row in x.find_note('Facebook',2):
    print(row)
