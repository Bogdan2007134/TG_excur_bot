import sqlite3

class Database:

# подключение к бд
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        
# регистрация пользовательского id в бд
    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id, excur_sub) VALUES (?,?)", (user_id, 0))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))
    

# проверка и установка этапа регистрации
    # def get_signup(self, user_id):
    #     with self.connection:
    #         result = self.cursor.execute("SELECT signup FROM users WHERE user_id = ?", (user_id,)).fetchall()
    #         for row in result:
    #             signup = str(row[0])
    #         return signup

    # def set_signup(self, user_id, signup):
    #     with self.connection:
    #         return self.cursor.execute("UPDATE users SET signup = ? WHERE user_id = ?", (signup, user_id,))
    
# установка никнейма
    def get_balance(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT excur_sub FROM users WHERE user_id = ?",(user_id,)).fetchall()
            for row in result:
                excur_sub = str(row[0])
            return excur_sub
         
# добавление и вычитание баллов за покупку экскурсии
    def plus(self, user_id, excur_sub):
        self.cursor.execute("UPDATE users SET excur_sub = excur_sub + ? WHERE user_id = ?", 
                            (excur_sub, user_id))
        return self.connection.commit()

    def MINUS(self, user_id, excur_sub):
        self.cursor.execute("UPDATE users SET excur_sub = excur_sub - ? WHERE user_id = ?", 
                            (excur_sub, user_id))
        return self.connection.commit()


# выход из бд 
    def close(self):
        self.connection.close()