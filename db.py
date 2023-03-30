import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
    
    
    
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))
            
    def add_user(self, user_id, referrer_id=None, don_stats=0):
        with self.connection:
            if referrer_id != None:
                self.cursor.execute("INSERT INTO `users` (`user_id`, `referrer_id`, `don_stats`) VALUES (?, ?, ?)", (user_id, referrer_id, 0,))
            else:
                return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
                
    def count_reeferals(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(`id`) as count FROM `users` WHERE `referrer_id` = ?", (user_id,)).fetchone()[0]
            
    def add_check(self, user_id, bill_id):
        with self.connection:
            self.cursor.execute("INSERT INTO `check` (`user_id`, `bill_id`) VALUES (?, ?)", (user_id, bill_id,))
                
    def get_check(self, bill_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `check` WHERE `bill_id` = ?", (bill_id,)).fetchmany(1)
            if not bool(len(result)):
                return False
            return result[0]
            
    def delete_check(self, bill_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `check` WHERE `bill_id` = ?", (bill_id,))

