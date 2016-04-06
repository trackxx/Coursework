import sqlite3


class Database():

    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute('''SELECT * FROM details''')
        except sqlite3.OperationalError:
            self.cursor.execute('''CREATE TABLE details(ID INTEGER PRIMARY KEY, USERNAME VARCHAR(16), PASSWORD VARCHAR(16), COURSE VARCHAR(32))''')
            self.conn.commit()

    def addEntry(self, username, password, course):
        self.cursor.execute('''INSERT INTO details VALUES (NULL, "{}", "{}", "{}")'''.format(username.lower(), password, course))
        self.conn.commit()

    def getUsername(self, username):
        for row in self.cursor.execute('''SELECT USERNAME FROM details WHERE USERNAME="{}"'''.format(username.lower())):
            return True
        return False

    def getUser(self, username, password):
        for row in self.cursor.execute('''SELECT USERNAME FROM details WHERE USERNAME="{}" AND PASSWORD="{}"'''.format(username.lower(), password)):
            return True
        return False