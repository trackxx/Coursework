import sqlite3


# The class that maintains the connection to the local database
class Database():

    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()
        # Check if user profile table exists. If not, create it.
        try:
            self.cursor.execute('''SELECT * FROM profile''')
        except sqlite3.OperationalError:
            self.cursor.execute('''CREATE TABLE profile(ID INTEGER PRIMARY KEY, USERNAME VARCHAR(16), PASSWORD VARCHAR(16), COURSE VARCHAR(32))''')
            self.conn.commit()

    # Adds an entry to the 'details' table of the database
    def addEntry(self, username, password, course):
        self.cursor.execute('''INSERT INTO profile VALUES (NULL, "{}", "{}", "{}")'''.format(username.lower(), password, course))
        self.conn.commit()

    # Returns true if a row with 'username' in the USERNAME column exists. False otherwise.
    def getUsername(self, username):
        for row in self.cursor.execute('''SELECT USERNAME FROM profile WHERE USERNAME="{}"'''.format(username.lower())):
            return True
        return False

    # Returns true if a user with the specified username and password exists.
    def getUser(self, username, password):
        for row in self.cursor.execute('''SELECT USERNAME FROM profile WHERE USERNAME="{}" AND PASSWORD="{}"'''.format(username.lower(), password)):
            return True
        return False

    # Actually returns the data of a particular user
    def getUserData(self, username):
        return self.cursor.execute('''SELECT USERNAME, COURSE FROM profile WHERE USERNAME="{}"'''.format(username.lower()))