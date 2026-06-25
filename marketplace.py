"""Player-to-player marketplace and trading system with economy."""

import json
import os
from datetime import datetime
from config import *

class TradeOffer:
    """Represents a trade offer between two players."""
    
    def __init__(self, sender, receiver, offering, requesting):
        self.id = datetime.now().timestamp()
        self.sender = sender
        self.receiver = receiver
        self.offering = offering  # List of items
        self.requesting = requesting  # List of items
        self.status = "pending"  # pending, accepted, declined, completed
        self.created_at = datetime.now()
        self.confirmations = {sender: False, receiver: False}
    
    def confirm(self, player):
        """Register confirmation from a player."""
        if player in self.confirmations:
            self.confirmations[player] = True
        
        if all(self.confirmations.values()):
            self.status = "completed"
    
    def to_dict(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "offering": self.offering,
            "requesting": self.requesting,
            "status": self.status,
            "created_at": str(self.created_at)
        }

class PlayerProfile:
    """Represents a player profile with inventory and trading history."""
    
    def __init__(self, player_id, username):
        self.player_id = player_id
        self.username = username
        self.currency = 0
        self.inventory = {
            "cosmetics": [],
            "trails": [],
            "blocks": [],
            "scripts": []
        }
        self.listings = []
        self.completed_trades = []
        self.level_completions = {}
        self.stats = {
            "total_playtime": 0,
            "levels_completed": 0,
            "best_times": {},
            "trades_completed": 0
        }
    
    def add_currency(self, amount, source=""):
        """Add currency to player account."""
        self.currency += amount
        print(f"✓ {self.username} earned {amount} currency ({source})")
    
    def spend_currency(self, amount):
        """Spend currency from player account."""
        if self.currency >= amount:
            self.currency -= amount
            return True
        return False
    
    def add_item(self, category, item_name, rarity="common"):
        """Add item to inventory."""
        if category in self.inventory:
            item = {
                "name": item_name,
                "rarity": rarity,
                "acquired_at": datetime.now().isoformat(),
                "tradeable": True
            }
            self.inventory[category].append(item)
            print(f"✓ {self.username} acquired: {item_name} ({rarity})")
    
    def remove_item(self, category, item_name):
        """Remove item from inventory."""
        if category in self.inventory:
            self.inventory[category] = [i for i in self.inventory[category] 
                                       if i["name"] != item_name]
    
    def to_dict(self):
        return {
            "player_id": self.player_id,
            "username": self.username,
            "currency": self.currency,
            "inventory": self.inventory,
            "listings": self.listings,
            "stats": self.stats
        }

class Marketplace:
    """Central marketplace for player-to-player trading."""
    
    def __init__(self):
        self.active_listings = []
        self.pending_trades = []
        self.completed_trades = []
        self.players = {}
        self.profiles_dir = "saves/profiles"
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure necessary directories exist."""
        os.makedirs(self.profiles_dir, exist_ok=True)
        os.makedirs("saves/market_listings", exist_ok=True)
        os.makedirs("saves/trades", exist_ok=True)
    
    def create_player(self, player_id, username):
        """Create a new player profile."""
        profile = PlayerProfile(player_id, username)
        self.players[player_id] = profile
        self.save_profile(profile)
        return profile
    
    def get_player(self, player_id):
        """Get player profile by ID."""
        if player_id not in self.players:
            self.load_profile(player_id)
        return self.players.get(player_id)
    
    def save_profile(self, profile):
        """Save player profile to file."""
        filepath = os.path.join(self.profiles_dir, f"{profile.player_id}.json")
        with open(filepath, 'w') as f:
            json.dump(profile.to_dict(), f, indent=2)
    
    def load_profile(self, player_id):
        """Load player profile from file."""
        filepath = os.path.join(self.profiles_dir, f"{player_id}.json")
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                profile = PlayerProfile(data["player_id"], data["username"])
                profile.currency = data.get("currency", 0)
                profile.inventory = data.get("inventory", {})
                profile.stats = data.get("stats", {})
                self.players[player_id] = profile
                return profile
        except:
            return None
    
    def create_listing(self, seller_id, items, asking_price):
        """Create a market listing."""
        listing = {
            "id": datetime.now().timestamp(),
            "seller_id": seller_id,
            "items": items,
            "asking_price": asking_price,
            "created_at": datetime.now().isoformat(),
            "active": True
        }
        self.active_listings.append(listing)
        return listing
    
    def purchase_listing(self, buyer_id, listing_id):
        """Purchase a listing from the marketplace."""
        listing = None
        for l in self.active_listings:
            if l["id"] == listing_id:
                listing = l
                break
        
        if not listing:
            return False
        
        buyer = self.get_player(buyer_id)
        seller = self.get_player(listing["seller_id"])
        
        if buyer.spend_currency(listing["asking_price"]):
            # Transfer items
            for item in listing["items"]:
                buyer.add_item(item["category"], item["name"], item.get("rarity"))
            
            # Give currency to seller
            seller.add_currency(listing["asking_price"], "marketplace_sale")
            
            # Mark listing as inactive
            listing["active"] = False
            
            self.save_profile(buyer)
            self.save_profile(seller)
            return True
        
        return False
    
    def propose_trade(self, sender_id, receiver_id, offering, requesting):
        """Propose a trade between two players."""
        trade = TradeOffer(sender_id, receiver_id, offering, requesting)
        self.pending_trades.append(trade)
        return trade
    
    def confirm_trade(self, trade_id, player_id):
        """Confirm a trade by a player."""
        trade = None
        for t in self.pending_trades:
            if t.id == trade_id:
                trade = t
                break
        
        if not trade:
            return False
        
        trade.confirm(player_id)
        
        if trade.status == "completed":
            # Execute trade
            sender = self.get_player(trade.sender)
            receiver = self.get_player(trade.receiver)
            
            # Swap items
            for item in trade.offering:
                receiver.add_item(item["category"], item["name"])
            for item in trade.requesting:
                sender.add_item(item["category"], item["name"])
            
            self.pending_trades.remove(trade)
            self.completed_trades.append(trade)
            
            # Update stats
            sender.stats["trades_completed"] += 1
            receiver.stats["trades_completed"] += 1
            
            self.save_profile(sender)
            self.save_profile(receiver)
        
        return True
    
    def reward_level_completion(self, player_id, level_name, completion_time):
        """Reward player for completing a level."""
        profile = self.get_player(player_id)
        
        base_reward = BASE_LEVEL_REWARD
        difficulty_bonus = DIFFICULTY_MULTIPLIER if completion_time > 60 else 1.0
        time_bonus = max(0, TIME_BONUS - int(completion_time / 10))
        
        total_reward = int(base_reward * difficulty_bonus + time_bonus)
        
        profile.add_currency(total_reward, f"level_completion:{level_name}")
        profile.stats["levels_completed"] += 1
        profile.level_completions[level_name] = {
            "time": completion_time,
            "earned": total_reward,
            "completed_at": datetime.now().isoformat()
        }
        
        self.save_profile(profile)
        return total_reward

class ScriptEngine:
    """Executes custom scripts for level events and logic."""
    
    def __init__(self):
        self.triggers = {}
        self.conditions = {}
        self.actions = {}
        self.timers = {}
    
    def register_trigger(self, trigger_id, trigger_func):
        """Register a trigger function."""
        self.triggers[trigger_id] = trigger_func
    
    def execute_script(self, script_string, context):
        """
        Execute a script with IF/THEN logic.
        Example: 'IF player_on_plate_A THEN lower_wall_B 5 units AFTER 2 seconds'
        """
        try:
            # Parse script
            parts = script_string.split(' THEN ')
            if len(parts) != 2:
                return False
            
            condition, action = parts
            condition = condition.replace('IF ', '').strip()
            action = action.strip()
            
            # Evaluate condition
            if self.evaluate_condition(condition, context):
                # Execute action
                return self.execute_action(action, context)
            
            return False
        except Exception as e:
            print(f"Script error: {e}")
            return False
    
    def evaluate_condition(self, condition_str, context):
        """Evaluate a condition string."""
        # Simple condition evaluation
        if "player_on" in condition_str:
            return context.get("player_position") == context.get("trigger_plate")
        elif "collision" in condition_str:
            return context.get("collision") is True
        return False
    
    def execute_action(self, action_str, context):
        """Execute an action string."""
        # Parse action
        parts = action_str.split(' ')
        
        if "spawn" in action_str:
            return True  # Spawn item logic
        elif "lower" in action_str or "raise" in action_str:
            return True  # Platform movement logic
        elif "remove" in action_str:
            return True  # Object removal logic
        
        return False
