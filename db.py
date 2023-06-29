import sqlite3

class Database:

#подключение к бд
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        
#регистрация пользовательского id в бд
    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id, excur_sub) VALUES (?,?)", (user_id, 0))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))
    

#проверка и установка этапа регистрации
    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT signup FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE users SET signup = ? WHERE user_id = ?", (signup, user_id,))
    
#установка никнейма
    def get_nickname(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT nickname FROM users WHERE user_id = ?",(user_id,)).fetchall()
            for row in result:
                nickname = str(row[0])
            return nickname
        
    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE users SET nickname = ? WHERE user_id = ?", (nickname, user_id,))
    

    #добавление и вычитание баллов за покупку экскурсии
    def plus(self, user_id, operation, excur_sub):
        self.cursor.execute("INSERT INTO users (user_id, operation, excur_sub) VALUES (?, ?, ?)", 
                            (self.add_user(user_id), operation == '+', excur_sub))
        return self.connection.commit()
    
    def MINUS(self, user_id, operation, excur_sub):
        self.cursor.execute("INSERT INTO users (user_id, operation, excur_sub) VALUES (?, ?, ?)", 
                            (self.add_user(user_id), operation == '-', excur_sub))
        return self.connection.commit()
    
#выход из бд 
    def close(self):
        self.connection.close()