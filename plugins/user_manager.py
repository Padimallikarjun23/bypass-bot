# plugins/user_manager.py
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from datetime import datetime
from config import DATA_DIR, ADMIN_ID

class UserManager:
    def __init__(self):
        self.data_file = os.path.join(DATA_DIR, "user_data.json")
        self.user_data = self._load_data()
        
        # Set admin ID if not set
        if not self.user_data.get("admin_id"):
            self.user_data["admin_id"] = ADMIN_ID
            self._save_data()

    def _load_data(self):
        """Load user data with backward compatibility"""
        os.makedirs(DATA_DIR, exist_ok=True)
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
                        # Ensure all required fields exist (backward compatibility)
                        if "total_users" not in data:
                            data["total_users"] = []
                        if "banned_users" not in data:
                            data["banned_users"] = []
                        if "premium_users" not in data:
                            data["premium_users"] = []
                        if "premium_expiry" not in data:
                            data["premium_expiry"] = {}
                        if "daily_usage" not in data:
                            data["daily_usage"] = {}
                        return data
                    else:
                        print("user_data.json is empty, creating default data")
            except (json.JSONDecodeError, Exception) as e:
                print(f"Error loading user data: {e}, creating default data")
        
        # Return default data if file doesn't exist or is corrupted
        default_data = {
            "premium_users": [],
            "premium_expiry": {},
            "daily_usage": {},
            "admin_id": ADMIN_ID,
            "total_users": [],
            "banned_users": []
        }
        
        self._save_data_direct(default_data)
        return default_data

    def _save_data(self):
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(self.data_file, "w") as f:
                json.dump(self.user_data, f, indent=2)
        except Exception as e:
            print(f"Error saving user data: {e}")

    def _save_data_direct(self, data):
        """Save data directly without using self.user_data"""
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(self.data_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving user data: {e}")

    def add_user(self, user_id):
        """Add user to total users list"""
        uid = str(user_id)
        if uid not in self.user_data["total_users"]:
            self.user_data["total_users"].append(uid)
            self._save_data()
            return True
        return False

    def is_premium(self, user_id):
        """Check if user is premium with backward compatibility"""
        uid = str(user_id)
        return uid in self.user_data.get("premium_users", [])

    def is_admin(self, user_id):
        return str(user_id) == str(self.user_data.get("admin_id"))

    def is_banned(self, user_id):
        return str(user_id) in self.user_data.get("banned_users", [])

    def ban_user(self, user_id):
        uid = str(user_id)
        if uid not in self.user_data.get("banned_users", []):
            if "banned_users" not in self.user_data:
                self.user_data["banned_users"] = []
            self.user_data["banned_users"].append(uid)
            self._save_data()
            return True
        return False

    def unban_user(self, user_id):
        uid = str(user_id)
        if uid in self.user_data.get("banned_users", []):
            self.user_data["banned_users"].remove(uid)
            self._save_data()
            return True
        return False

    def add_premium_user(self, user_id, days=30):
        """Add premium user with enhanced validation"""
        try:
            # Clean and validate user ID
            uid = str(user_id).strip()
            if not uid or not uid.isdigit():
                print(f"[ERROR] Invalid user ID format: {uid}")
                return False
                
            # Ensure all required data structures exist
            self.user_data.setdefault("premium_users", [])
            self.user_data.setdefault("premium_expiry", {})
            self.user_data.setdefault("total_users", [])
            
            # Convert all IDs to strings for consistency
            self.user_data["premium_users"] = [str(u) for u in self.user_data["premium_users"]]
            self.user_data["total_users"] = [str(u) for u in self.user_data["total_users"]]
            
            # Add to total users if not present
            if uid not in self.user_data["total_users"]:
                self.user_data["total_users"].append(uid)
            
            now = datetime.now().timestamp()
            if uid in self.user_data["premium_users"]:
                # Extend existing premium
                current_expiry = float(self.user_data["premium_expiry"].get(uid, now))
                if current_expiry < now:
                    current_expiry = now
                new_expiry = current_expiry + (days * 24 * 3600)
                self.user_data["premium_expiry"][uid] = new_expiry
                print(f"[DEBUG] Extended premium for user {uid} until {datetime.fromtimestamp(new_expiry)}")
            else:
                # Add new premium user
                self.user_data["premium_users"].append(uid)
                expiry = now + (days * 24 * 3600)
                self.user_data["premium_expiry"][uid] = expiry
                print(f"[DEBUG] Added new premium user {uid} until {datetime.fromtimestamp(expiry)}")
            
            # Save changes immediately
            self._save_data()
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to add premium user {user_id}: {str(e)}")
            return False

    def remove_premium_user(self, user_id):
        """Remove premium user with enhanced validation and error handling"""
        try:
            # Convert to string and clean any whitespace
            uid = str(user_id).strip()
            
            print(f"[DEBUG] Attempting to remove premium for user: '{uid}'")
            print(f"[DEBUG] Data type of user_id: {type(user_id)}")
            
            # Validate user_id format
            if not uid or not uid.isdigit():
                print(f"[DEBUG] Invalid user ID format: {uid}")
                return False
                
            # Load fresh data to avoid cached issues
            self.user_data = self._load_data()
            
            # Ensure premium_users list exists
            if "premium_users" not in self.user_data:
                self.user_data["premium_users"] = []
            
            # Convert all user IDs to strings for comparison
            premium_users = [str(u) for u in self.user_data["premium_users"]]
            print(f"[DEBUG] Current premium users (after conversion): {premium_users}")
            
            if uid not in premium_users:
                print(f"[DEBUG] User {uid} not found in premium users list")
                print(f"[DEBUG] Premium users count: {len(premium_users)}")
                return False
            
            # Remove from premium users (use original list)
            self.user_data["premium_users"].remove(uid)
            
            # Remove from premium expiry if exists
            if "premium_expiry" in self.user_data and uid in self.user_data["premium_expiry"]:
                print(f"[DEBUG] Removing user {uid} from premium_expiry")
                self.user_data["premium_expiry"].pop(uid)
            
            # Save changes immediately
            self._save_data()
            print(f"[DEBUG] Successfully removed premium for user {uid}")
            print(f"[DEBUG] Updated premium users: {self.user_data['premium_users']}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to remove premium user {uid}: {str(e)}")
            return False

    def check_premium_expiry(self):
        now = datetime.now().timestamp()
        expired = []
        
        # Ensure premium_expiry exists
        if "premium_expiry" not in self.user_data:
            self.user_data["premium_expiry"] = {}
            return expired
        
        for uid, exp in list(self.user_data["premium_expiry"].items()):
            if now > exp:
                expired.append(uid)
                self.remove_premium_user(uid)
                print(f"[DEBUG] Expired premium for user {uid}")
        
        return expired

    def get_daily_usage(self, user_id):
        uid = str(user_id)
        today = datetime.now().strftime("%Y-%m-%d")
        
        if uid not in self.user_data["daily_usage"]:
            self.user_data["daily_usage"][uid] = {}
        
        # Clean old usage data (keep only today)
        self.user_data["daily_usage"][uid] = {
            k: v for k, v in self.user_data["daily_usage"][uid].items() if k == today
        }
        self._save_data()
        return self.user_data["daily_usage"][uid].get(today, 0)

    def increment_usage(self, user_id):
        uid = str(user_id)
        today = datetime.now().strftime("%Y-%m-%d")
        
        if uid not in self.user_data["daily_usage"]:
            self.user_data["daily_usage"][uid] = {}
        
        current_usage = self.user_data["daily_usage"][uid].get(today, 0)
        self.user_data["daily_usage"][uid][today] = current_usage + 1
        self._save_data()
        return self.user_data["daily_usage"][uid][today]

    def get_stats(self):
        return {
            "total_users": len(self.user_data.get("total_users", [])),
            "premium_users": len(self.user_data.get("premium_users", [])),
            "banned_users": len(self.user_data.get("banned_users", [])),
        }

    def get_premium_expiry(self, user_id):
        uid = str(user_id)
        if "premium_expiry" not in self.user_data:
            return None
        
        expiry_timestamp = self.user_data["premium_expiry"].get(uid)
        if expiry_timestamp:
            return datetime.fromtimestamp(expiry_timestamp)
        return None

    def migrate_old_data(self):
        """Migrate from old data structure to new structure"""
        print("[DEBUG] Checking for data migration...")
        
        # Check if migration is needed
        if "total_users" not in self.user_data:
            self.user_data["total_users"] = []
            
            # Migrate from premium_users if they exist
            if "premium_users" in self.user_data:
                for uid in self.user_data["premium_users"]:
                    if uid not in self.user_data["total_users"]:
                        self.user_data["total_users"].append(uid)
            
            # Migrate from daily_usage if it exists
            if "daily_usage" in self.user_data:
                for uid in self.user_data["daily_usage"].keys():
                    if uid not in self.user_data["total_users"]:
                        self.user_data["total_users"].append(uid)
            
            self._save_data()
            print("[DEBUG] Data migration completed")

# Create global instance
user_manager = UserManager()

# Run migration on startup
user_manager.migrate_old_data()
