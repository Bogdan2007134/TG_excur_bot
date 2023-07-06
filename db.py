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
    #      with self.connection:
    #         result = self.cursor.execute("SELECT signup FROM users WHERE user_id = ?", (user_id,)).fetchall()
    #         for row in result:
    #              signup = str(row[0])
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

    def MINUS(self, user_id):
        self.cursor.execute("UPDATE users SET excur_sub = excur_sub - 1 WHERE user_id = ?", 
                            (user_id))
        return self.connection.commit()
# добавление города в city
    def change_city(self, user_id, city):
        self.cursor.execute("UPDATE users SET city = ? WHERE user_id = ?",
            (city, user_id))
        return self.connection.commit()
    
        """
        тут я хрен знает как у тебя бд устроена но дословно 
        UPDATE users SET city = ? WHERE user_id = ?
        тебе нужно одновить значение города если ID равен пользователю
        я думаю в принципе тут не будет ошибок чтобы обрабатывать
        в try: except:
        
        опять же, сделай как должно быть, я как понял, я с базой данных хуже тебя знаком
        """

# просмотр выбранного города из бд
    def select_city(self, user_id):
        self.cursor.execute("SELECT city FROM users WHERE id = ?", (user_id,))
        return self.cursor.fetchone()
    """
    ну тут я тоже хз как у тебя бд работает, но нам нужно 
    просматривать город который числится у пользователя по ID
    """
    
    
    
# просмотр выбранного прогресса из бд
    def select_progress(self, user_id):
        self.cursor.execute("SELECT column1, column2 FROM table_name WHERE user_id = ?", 
                            (user_id,))
        return self.cursor.fetchall()
    """
    нужно просматривать прогресс который числится у пользователя по ID
    """

# продвижение выбранного прогресса из бд
    def update_progress(self, user_id):
        self.cursor.execute("UPDATE users SET progress = progress + 1 WHERE user_id = ?", 
                            (user_id))
        return self.connection.commit()
    """
    нужно прибавлять к прогрессу + 1 прогресс который числится у пользователя по ID
    """
    
# продвижение выбранного прогресса из бд
    def reset_progress(self, user_id):
        self.cursor.execute("UPDATE users SET progress = 0 WHERE user_id = ?", 
                            (user_id))
        return self.connection.commit()
    """
    нужно обнулять прогресс который числится у пользователя по ID
    """
    
    def select_direction(self, user_id):
        self.cursor.execute("SELECT direction FROM users WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            direction = result[0]
            return direction
        else:
            return None

    
# просмотр выбранного прогресса из бд
    def change_direction(self, user_id, direction):
        query = "UPDATE users SET direction = ? WHERE user_id = ?"
        self.cursor.execute(query, (direction, user_id))
        return self.connection.commit()
    """
    нужно просматривать направление который числится у пользователя по ID
    """
    
# добавление выбранного направления из бд
    def change_direction(self, user_id, direction):
        self.cursor.execute("UPDATE users SET direction = ? WHERE id = ?",
                    (direction, user_id))
        return self.connection.commit()
    """
    нужно добавлять направление который числится у пользователя по ID
    """
    
    
        
# просмотр выбранного прогресса из бд
    def select_interactive_direction(self, user_id): 
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", 
                            (user_id,)) 
        result = self.cursor.fetchall() 
        return result 
    """
    нужно просматривать интерактивное направление который числится у пользователя по ID
    """
    
# выбор выбранного прогресса из бд
    def change_interactiv_direction(self, user_id, interactiv):
        self.cursor.execute("INSERT users", 
                            (user_id, interactiv))
        return self.connection.commit()
    
    def get_selected_progress(self, user_id): 
        self.cursor.execute("SELECT interactiv FROM users WHERE user_id = ?", 
                            (user_id,)) 
        result = self.cursor.fetchone() 
        if result:     
            return result[0] 
        else:     
            return None 
    """
    нужно добавлять интерактивное направление который числится у пользователя по ID
    """
    
    
    
# выход из бд 
    def close(self):
        self.connection.close()