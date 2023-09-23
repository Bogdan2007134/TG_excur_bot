import sqlite3
import pandas as pd
from datetime import datetime, timedelta


class Database:
    def __init__(self, db_file):
        """Подключение к БД"""
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_tables(self):
            from config import STANDARD_PRICE
            """Создание таблиц"""
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS excur_statistic
                                (id INTEGER PRIMARY KEY NOT NULL,
                                excur_date TEXT NOT NULL,
                                price_excur INTEGER NOT NULL)"""
            )

            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS prices
                                (id INTEGER PRIMARY KEY NOT NULL,
                                price INTEGER DEFAULT 0)"""
            )

            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS promo_code
                                (id INTEGER PRIMARY KEY NOT NULL,
                                promo TEXT,
                                discount INTEGER NOT NULL DEFAULT 0,
                                usage INTEGER)"""
            )

            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS users
                                (id INTEGER PRIMARY KEY NOT NULL,
                                user_id INTEGER NOT NULL,
                                ref_id INTEGER,
                                direction TEXT,
                                progress INTEGER NOT NULL DEFAULT 0,
                                active INTEGER NOT NULL DEFAULT 1,
                                condition INTEGER NOT NULL DEFAULT False,
                                payment_status INTEGER NOT NULL DEFAULT False,
                                page INTEGER DEFAULT 0,
                                current_promo TEXT,
                                promocode TEXT,
                                date TEXT)"""
            )

            self.cursor.execute(
                """SELECT id FROM prices WHERE id=1"""
            )
            record_exists = self.cursor.fetchone()

            if not record_exists:
                self.cursor.execute(
                    f"""INSERT INTO prices (price) VALUES ({STANDARD_PRICE})"""
                )

            self.connection.commit()

    def add_user(self, user_id, date, ref_id=None):
        """Регистрация пользователя"""
        with self.connection:
            if ref_id != None:
                return self.cursor.execute(
                    "INSERT INTO users (user_id, ref_id, date) VALUES (?,?,?)",
                    (user_id, ref_id, date),
                )
            else:
                return self.cursor.execute(
                    "INSERT INTO users (user_id, date) VALUES (?,?)", (user_id, date)
                )

    def get_user_count(self):
        """Получение количества пользователей"""

        return self.cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    def user_exists(self, user_id):
        """Проверка зарегистрирован ли пользователь"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM users WHERE user_id = ?", (user_id,)
            ).fetchall()
            return bool(len(result))

    def get_pref(self, user_id):
        """Проверка является ли пользователь админом"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT pref FROM users WHERE user_id = ?", (user_id,)
            ).fetchall()
            for row in result:
                pref = str(row[0])
            return pref

    def set_pref(self, user_id, pref):
        """Назначение пользователя админом"""
        with self.connection:
            return self.cursor.execute(
                "UPDATE users SET pref = ? WHERE user_id = ?",
                (
                    pref,
                    user_id,
                ),
            )

    def get_price(self, id):
        """Получение значения колонны price в таблице prices"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT price FROM prices WHERE id = ?", (id,)
            ).fetchall()
            for row in result:
                price = int(row[0])
            return price

    def add_price(self, id, price):
        """Изменение значения колонны price в таблице prices"""
        self.cursor.execute(
            "UPDATE prices SET price = ? WHERE id = ?",
            (
                price,
                id,
            ),
        )
        return self.connection.commit()

    def add_direction(self, user_id, direction):
        """Изменение значения колонны direction в таблице users"""
        self.cursor.execute(
            "UPDATE users SET direction = ? WHERE user_id = ?",
            (
                direction,
                user_id,
            ),
        )
        return self.connection.commit()

    def get_direction(self, user_id):
        """Проверка оплаченой экскурсии"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT direction FROM users WHERE user_id = ?", (user_id,)
            ).fetchall()
            for row in result:
                direction = str(row[0])
            return direction

    def update_progress(self, user_id):
        """продвижение выбранного прогресса из бд"""
        self.cursor.execute(
            "UPDATE users SET progress = progress + 1 WHERE user_id = ?", (user_id,)
        )
        return self.connection.commit()

    def reset_progress(self, user_id):
        """обнуление выбранного прогресса из бд"""
        self.cursor.execute(
            "UPDATE users SET progress = 0 WHERE user_id = ?", (user_id,)
        )
        return self.connection.commit()

    def select_progress(self, user_id):
        """просмотр выбранного прогресса из бд"""

        return self.cursor.execute(
            "SELECT progress FROM users WHERE user_id = ?", (user_id,)
        ).fetchall()

    def select_direction(self, user_id):
        """Просмотр выбранной экскурсии"""
        self.cursor.execute("SELECT direction FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            direction = result[0]
            return direction
        else:
            return None

    def select_payment_status(self, user_id):
        """просмотр состояния оплаты экскурсии"""
        return self.cursor.execute(
            "SELECT payment_status FROM users WHERE user_id = ?", (user_id,)
        ).fetchall()

    def add_payment_status(self, user_id, payment_status):
        """Изменение значения колонны payment_status в таблице users"""
        self.cursor.execute(
            "UPDATE users SET payment_status = ? WHERE user_id = ?",
            (
                payment_status,
                user_id,
            ),
        )
        return self.connection.commit()

    def select_condition(self, user_id):
        """просмотр состояния экскурсии"""
        return self.cursor.execute(
            "SELECT condition FROM users WHERE user_id = ?", (user_id,)
        ).fetchall()

    def add_condition(self, user_id, condition):
        """Изменение значения колонны condition в таблице users"""
        self.cursor.execute(
            "UPDATE users SET condition = ? WHERE user_id = ?",
            (
                condition,
                user_id,
            ),
        )
        return self.connection.commit()

    def get_users(self):
        """
        Этот запрос выполняет выборку всех записей из таблицы "users" по стобцу "active"
        """
        with self.connection:
            return self.cursor.execute("SELECT user_id, active FROM users").fetchall()

    def set_active(self, user_id, active):
        """
        Этот запрос обновляет значение столбца "active"
        """
        with self.connection:
            return self.cursor.execute(
                "UPDATE users SET active = ? WHERE user_id = ?",
                (
                    active,
                    user_id,
                ),
            )

    def get_users_last_day_count(self):
        """получения количества пришедших пользователей за последний день"""
        query = "SELECT COUNT(*) FROM users WHERE date >= ?"
        yesterday = datetime.now() - timedelta(days=1)
        return self.cursor.execute(
            query, (yesterday.strftime("%Y-%m-%d %H:%M:%S"),)
        ).fetchone()[0]

    def get_users_last_week_count(self):
        """получения количества пришедших пользователей за последнюю неделю"""
        query = "SELECT COUNT(*) FROM users WHERE date >= ?"
        yesterday = datetime.now() - timedelta(days=7)
        return self.cursor.execute(
            query, (yesterday.strftime("%Y-%m-%d %H:%M:%S"),)
        ).fetchone()[0]

    def get_users_last_month_count(self):
        """получения количества пришедших пользователей за последний месяц"""
        query = "SELECT COUNT(*) FROM users WHERE date >= ?"
        yesterday = datetime.now() - timedelta(days=30)
        return self.cursor.execute(
            query, (yesterday.strftime("%Y-%m-%d %H:%M:%S"),)
        ).fetchone()[0]

    def get_users_last_year_count(self):
        """получения количества пришедших пользователей за последний год"""
        query = "SELECT COUNT(*) FROM users WHERE date >= ?"
        yesterday = datetime.now() - timedelta(days=365)
        return self.cursor.execute(
            query, (yesterday.strftime("%Y-%m-%d %H:%M:%S"),)
        ).fetchone()[0]

    def add_excursion(self, excur_date, price_excur):
        """Добавление даты покупки экскурсий"""

        return self.cursor.execute(
            "INSERT INTO excur_statistic (excur_date, price_excur) VALUES (?, ?)",
            (excur_date, price_excur),
        )

    def get_excur_statistic_count(self):
        """Получение количества купленных экскурсий"""

        return self.cursor.execute("SELECT COUNT(*) FROM excur_statistic").fetchone()[0]

    def get_excur_statistic_last_day(self):
        """получения количества пришедших пользователей за последний день"""
        query = "SELECT COUNT(*) FROM excur_statistic WHERE excur_date >= ?"
        yesterday = datetime.now() - timedelta(days=1)
        return self.cursor.execute(
            query, (yesterday.strftime("%Y-%m-%d %H:%M:%S"),)
        ).fetchone()[0]

    def get_excur_statistic_last_week(self):
        """получения количества пришедших пользователей за последнюю неделю"""
        query = "SELECT COUNT(*) FROM excur_statistic WHERE excur_date >= ?"
        yesterday = datetime.now() - timedelta(days=7)
        return self.cursor.execute(
            query, (yesterday.strftime("%Y-%m-%d %H:%M:%S"),)
        ).fetchone()[0]

    def get_excur_statistic_last_month(self):
        """получения количества пришедших пользователей за последний месяц"""
        query = "SELECT COUNT(*) FROM excur_statistic WHERE excur_date >= ?"
        yesterday = datetime.now() - timedelta(days=30)
        return self.cursor.execute(
            query, (yesterday.strftime("%Y-%m-%d %H:%M:%S"),)
        ).fetchone()[0]

    def get_excur_statistic_last_year(self):
        """получения количества пришедших пользователей за последний год"""
        query = "SELECT COUNT(*) FROM excur_statistic WHERE excur_date >= ?"
        yesterday = datetime.now() - timedelta(days=365)
        return self.cursor.execute(
            query, (yesterday.strftime("%Y-%m-%d %H:%M:%S"),)
        ).fetchone()[0]

    def get_page(self, user_id):
        """Получение значения колонны page в таблице users"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT page FROM users WHERE user_id = ?", (user_id,)
            ).fetchall()
            for row in result:
                price = int(row[0])
            return price

    def add_page(self, user_id, page):
        """Сбросить текущую страницу выбранного пользователя в базе данных"""
        self.cursor.execute(
            "UPDATE users SET page = ? WHERE user_id = ?", (page, user_id)
        )
        return self.connection.commit()

    def get_promo_discount_dict(self):
        """Возвращает словарь promo и discount из таблицы"""
        results = self.cursor.execute(
            f"SELECT promo, discount FROM promo_code;"
        ).fetchall()

        df = pd.DataFrame(results, columns=["promo", "discount"])
        dictionary = df.set_index("promo").to_dict()["discount"]
        return dictionary

    def add_to_promocode(self, user_id, promocode):
        """Добавление нового промокода в список промокодов пользователя"""
        with self.connection:
            self.cursor.execute(
                "SELECT promocode FROM users WHERE user_id = ?", (user_id,)
            )
            current_promocode = self.cursor.fetchone()[0]
            if current_promocode is not None:
                updated_promocode = current_promocode + "," + promocode
            else:
                updated_promocode = promocode
            self.cursor.execute(
                "UPDATE users SET promocode = ? WHERE user_id = ?",
                (updated_promocode, user_id),
            )

    def get_promocode_user(self, user_id):
        """Получение списка промокодов пользователя"""
        with self.connection:
            self.cursor.execute(
                "SELECT promocode FROM users WHERE user_id = ?", (user_id,)
            )
            result = self.cursor.fetchone()
            if result and result[0] is not None:
                return result[0].split(",")
            else:
                return []

    def add_current_promo(self, user_id, current_promo):
        """Изменение значения колонны current_promo в таблице users"""
        self.cursor.execute(
            "UPDATE users SET current_promo = ? WHERE user_id = ?",
            (
                current_promo,
                user_id,
            ),
        )
        return self.connection.commit()

    def get_current_promo_user(self, user_id):
        """Проверка промокода"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT current_promo FROM users WHERE user_id = ?", (user_id,)
            ).fetchall()
            for row in result:
                current_promo = str(row[0])
            return current_promo

    def get_total_excur_price(self):
        """Получение суммы всех цен экскурсий"""
        self.cursor.execute("SELECT SUM(price_excur) FROM excur_statistic")
        total_price = self.cursor.fetchone()[0]
        return total_price

    def add_promocode(self, promo, discount, usage):
        """Добавление нового промокода и скидки к нему"""

        return self.cursor.execute(
            "INSERT INTO promo_code (promo, discount, usage) VALUES (?,?,?)",
            (promo, discount, usage),
        )

    def delete_promocode(self, promo):
        """Удаление промокода по его названию"""
        return self.cursor.execute("DELETE FROM promo_code WHERE promo = ?", (promo,))

    def get_usage_by_promo(self, promo):
        """Получение значения usage по названию промокода"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT usage FROM promo_code WHERE promo = ?", (promo,)
            ).fetchall()
            for row in result:
                usage = int(row[0])
            return usage

    def count_referrals(self, user_id):
        """Получение количества рефералов"""
        with self.connection:
            return self.cursor.execute(
                "SELECT COUNT(id) as count FROM users WHERE ref_id = ?", (user_id,)
            ).fetchone()[0]

    def get_ref_id_user(self, user_id):
        """Проверка промокода"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT ref_id FROM users WHERE user_id = ?", (user_id,)
            ).fetchall()
            for row in result:
                ref_id = int(row[0])
            return ref_id

    def update_usage_by_promo(self, promo, new_usage):
        """Изменение значения usage по названию промокода"""
        return self.cursor.execute(
            "UPDATE promo_code SET usage=? WHERE promo=?", (new_usage, promo)
        )

    def close(self):
        """Закрытие подключения к БД"""
        self.connection.close()
