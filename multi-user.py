def find_milestone_partners(user_points_dict, target_milestone):
    """
    Finds two users whose combined reward points exactly hit a target milestone.
    Uses a Hash Map (dictionary) to do it efficiently in a single pass.
    """
    seen_users = {}  # Keeps track of: {points_needed: username}
    
    for username, points in user_points_dict.items():
        # Calculate exactly how many points we need to hit the milestone
        needed_points = target_milestone - points
        
        # If we already encountered a user with the exact points needed, we found a match!
        if points in seen_users:
            matching_partner = seen_users[points]
            return f"Match Found! {matching_partner} ({user_points_dict[matching_partner]} pts) and {username} ({points} pts) can team up to reach {target_milestone} points!"
        
        # Otherwise, log the needed points and the current user's name
        seen_users[needed_points] = username
        
    return "No two users can exactly hit the milestone together."

# --- Testing the code with multiple users ---
if __name__ == "__main__":
    # A database of users and their current points
    user_database = {
        "Alice": 150,
        "Bob": 420,
        "Charlie": 300,
        "David": 580,
        "Emma": 210
    }
    
    milestone = 720  # The target goal (Bob's 420 + Charlie's 300 = 720)
    
    print(f"Scanning database for a perfect pair to reach {milestone} points...")
    result = find_milestone_partners(user_database, milestone)
    print(result)
