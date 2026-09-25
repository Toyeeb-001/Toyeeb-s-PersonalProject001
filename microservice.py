import time

class SpotifyLoyaltyEngine:
    def __init__(self):
        # A fast internal data map simulating a database
        self.user_database = {
            "user_01": {"name": "Kofi", "minutes_listened": 1200, "tier": "Free"},
            "user_02": {"name": "Chidi", "minutes_listened": 8500, "tier": "Premium"}
        }

    def process_streaming_payout(self, user_id, new_minutes):
        """
        AI can generate this math instantly, but an engineer must design 
        how it safely interacts with database memory without crashing.
        """
        # Guard Rail: Ensure user exists
        if user_id not in self.user_database:
            return {"status": "ERROR", "message": "User identifier not found in cluster."}
            
        user = self.user_database[user_id]
        
        # Core architectural modification
        user["minutes_listened"] += new_minutes
        
        # Dynamic upgrading business logic
        if user["minutes_listened"] > 5000 and user["tier"] == "Free":
            user["tier"] = "Premium_Eligible"
            note = "System triggered automated tier promotion."
        else:
            note = "Metrics updated successfully."
            
        return {
            "status": "SUCCESS",
            "timestamp": time.time(),
            "data": user,
            "system_note": note
        }

# --- SYSTEM TEST RUN ---
engine = SpotifyLoyaltyEngine()
# Imagine millions of these events hitting your Chromebook server every second:
result = engine.process_streaming_payout("user_01", 4000)
print(f"System State Output: {result}")
