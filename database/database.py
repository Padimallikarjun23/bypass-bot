import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_file="database/users.db"):
        self.db_file = db_file
        self.setup()

    def setup(self):
        """Create necessary tables if they don't exist"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        # Create users table
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (user_id INTEGER PRIMARY KEY,
                     username TEXT,
                     join_date TEXT,
                     is_premium INTEGER DEFAULT 0)''')
        
        # Create stats table
        c.execute('''CREATE TABLE IF NOT EXISTS stats
                    (user_id INTEGER,
                     action TEXT,
                     timestamp TEXT,
                     FOREIGN KEY (user_id) REFERENCES users(user_id))''')
        
        conn.commit()
        conn.close()

    async def add_user(self, user_id: int, username: str = None):
        """Add new user to database"""
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            
            c.execute("INSERT OR IGNORE INTO users (user_id, username, join_date) VALUES (?, ?, ?)",
                     (user_id, username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding user to database: {e}")
            return False

    async def full_userbase(self):
        """Get list of all user IDs"""
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            
            c.execute("SELECT user_id FROM users")
            users = [row[0] for row in c.fetchall()]
            
            conn.close()
            return users
        except Exception as e:
            logger.error(f"Error getting userbase: {e}")
            return []

    async def total_users_count(self):
        """Get total number of users"""
        try:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            
            c.execute("SELECT COUNT(*) FROM users")
            count = c.fetchone()[0]
            
            conn.close()
            return count
        except Exception as e:
            logger.error(f"Error getting user count: {e}")
            return 0

# Initialize database
db = Database()

# Export functions
full_userbase = db.full_userbase
total_users_count = db.total_users_count
add_user = db.add_user
