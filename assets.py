"""Asset management system for textures, blocks, and cosmetics."""

import json
import os
from config import *

class Asset:
    """Represents a tradeable asset (block, cosmetic, trail, script)."""
    
    def __init__(self, asset_id, name, asset_type, rarity="common"):
        self.id = asset_id
        self.name = name
        self.type = asset_type  # "block", "cosmetic", "trail", "script"
        self.rarity = rarity  # common, uncommon, rare, epic, legendary
        self.creator = None
        self.creation_date = None
        self.marketplace_price = self.calculate_price()
    
    def calculate_price(self):
        """Calculate marketplace price based on rarity."""
        rarity_prices = {
            "common": 100,
            "uncommon": 250,
            "rare": 500,
            "epic": 1000,
            "legendary": 5000
        }
        return rarity_prices.get(self.rarity, 100)

class AssetLibrary:
    """Manages all game assets and their properties."""
    
    def __init__(self):
        self.assets = {}
        self.categories = {
            "BLOCKS": [],
            "COSMETICS": [],
            "TRAILS": [],
            "SCRIPTS": []
        }
        self.load_default_assets()
    
    def load_default_assets(self):
        """Load default game assets."""
        # Default blocks
        blocks = [
            ("concrete_block", "Concrete Block", "BLOCKS", "common"),
            ("metal_plate", "Metal Plate", "BLOCKS", "common"),
            ("glass_platform", "Glass Platform", "BLOCKS", "uncommon"),
            ("neon_block", "Neon Block", "BLOCKS", "rare"),
            ("crystal_block", "Crystal Block", "BLOCKS", "epic"),
        ]
        
        # Default cosmetics
        cosmetics = [
            ("black_hoodie", "Black Hoodie", "COSMETICS", "common"),
            ("neon_jacket", "Neon Jacket", "COSMETICS", "uncommon"),
            ("cyber_suit", "Cyber Suit", "COSMETICS", "rare"),
            ("legendary_coat", "Legendary Coat", "COSMETICS", "legendary"),
        ]
        
        # Default trails
        trails = [
            ("smoke_trail", "Smoke Trail", "TRAILS", "common"),
            ("fire_trail", "Fire Trail", "TRAILS", "uncommon"),
            ("neon_trail", "Neon Trail", "TRAILS", "rare"),
            ("electric_trail", "Electric Trail", "TRAILS", "epic"),
        ]
        
        # Default scripts
        scripts = [
            ("simple_trigger", "Simple Trigger", "SCRIPTS", "common"),
            ("timer_delay", "Timer Delay", "SCRIPTS", "uncommon"),
            ("complex_logic", "Complex Logic", "SCRIPTS", "rare"),
        ]
        
        all_assets = blocks + cosmetics + trails + scripts
        
        for asset_id, name, category, rarity in all_assets:
            asset = Asset(asset_id, name, category, rarity)
            self.assets[asset_id] = asset
            self.categories[category].append(asset)
    
    def get_asset(self, asset_id):
        """Get an asset by ID."""
        return self.assets.get(asset_id)
    
    def get_assets_by_category(self, category):
        """Get all assets in a category."""
        return self.categories.get(category, [])
    
    def get_assets_by_rarity(self, rarity):
        """Get all assets of a specific rarity."""
        return [asset for asset in self.assets.values() if asset.rarity == rarity]
    
    def create_custom_asset(self, name, asset_type, creator_id, rarity="common"):
        """Create a custom asset (for user-created content)."""
        asset_id = f"custom_{creator_id}_{int(time.time())}"
        asset = Asset(asset_id, name, asset_type, rarity)
        asset.creator = creator_id
        asset.creation_date = datetime.now().isoformat()
        
        self.assets[asset_id] = asset
        if asset_type in self.categories:
            self.categories[asset_type].append(asset)
        
        return asset

# Asset texture definitions (placeholder)
ASSET_TEXTURES = {
    "BLOCKS": {
        "concrete": {"color": (100, 100, 100), "style": "solid"},
        "metal": {"color": (150, 150, 150), "style": "metallic"},
        "glass": {"color": (200, 220, 255), "style": "transparent"},
        "neon": {"color": (0, 255, 200), "style": "glowing"},
    },
    "HAZARDS": {
        "spike": {"color": (255, 50, 50), "damage": 10},
        "lava": {"color": (255, 100, 0), "damage": 20},
        "laser": {"color": (255, 0, 0), "damage": 15},
        "buzz_saw": {"color": (150, 150, 150), "damage": 25},
    },
    "COSMETICS": {
        "hoodie_black": {"color": (20, 20, 20), "style": "clothing"},
        "jacket_neon": {"color": (0, 255, 150), "style": "clothing"},
    }
}
