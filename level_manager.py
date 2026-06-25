"""Level loading and management system."""

import json
import os
from config import *

class Level:
    """Represents a game level with platforms, hazards, and properties."""
    
    def __init__(self, name, width=3000, height=SCREEN_HEIGHT):
        self.name = name
        self.width = width
        self.height = height
        self.platforms = []
        self.hazards = []
        self.pickups = []
        self.spawn_point = (100, SCREEN_HEIGHT - 200)
        self.checkpoints = []
        self.scripts = []
        self.last_checkpoint = self.spawn_point
        self.difficulty = "Normal"
        self.time_limit = 300  # seconds
    
    def render(self, screen, camera_x, camera_y):
        """Render the level to the screen."""
        import pygame
        
        # Draw platforms
        for platform in self.platforms:
            x = platform["x"] - camera_x
            y = platform["y"] - camera_y
            width = platform["width"]
            height = platform["height"]
            
            if -width < x < SCREEN_WIDTH and -height < y < SCREEN_HEIGHT:
                pygame.draw.rect(screen, PRIMARY_COLOR, (x, y, width, height))
                pygame.draw.rect(screen, TEXT_COLOR, (x, y, width, height), 2)
        
        # Draw hazards
        for hazard in self.hazards:
            x = hazard["x"] - camera_x
            y = hazard["y"] - camera_y
            width = hazard["width"]
            height = hazard["height"]
            
            if -width < x < SCREEN_WIDTH and -height < y < SCREEN_HEIGHT:
                pygame.draw.rect(screen, SECONDARY_COLOR, (x, y, width, height))
                pygame.draw.rect(screen, TEXT_COLOR, (x, y, width, height), 2)
        
        # Draw checkpoints (visual guides)
        for checkpoint in self.checkpoints:
            x = checkpoint[0] - camera_x
            y = checkpoint[1] - camera_y
            pygame.draw.circle(screen, TERTIARY_COLOR, (int(x), int(y)), 15)
            pygame.draw.circle(screen, TEXT_COLOR, (int(x), int(y)), 15, 2)
    
    def add_platform(self, x, y, width, height):
        """Add a platform to the level."""
        self.platforms.append({
            "x": x,
            "y": y,
            "width": width,
            "height": height
        })
    
    def add_hazard(self, x, y, width, height, hazard_type="spike"):
        """Add a hazard to the level."""
        self.hazards.append({
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "type": hazard_type
        })
    
    def add_checkpoint(self, x, y):
        """Add a checkpoint to the level."""
        self.checkpoints.append((x, y))
        self.last_checkpoint = (x, y)

class LevelManager:
    """Manages loading and creating levels."""
    
    def __init__(self):
        self.levels_dir = "levels"
        self.custom_levels_dir = "saves/custom_levels"
        self.ensure_directories()
        self.campaign_levels = {}
        self.load_campaign_levels()
    
    def ensure_directories(self):
        """Ensure level directories exist."""
        os.makedirs(self.levels_dir, exist_ok=True)
        os.makedirs(self.custom_levels_dir, exist_ok=True)
        os.makedirs("saves", exist_ok=True)
    
    def load_campaign_levels(self):
        """Load all campaign levels."""
        for i, level_name in enumerate(CAMPAIGN_LEVELS):
            self.campaign_levels[level_name] = self.create_procedural_level(level_name, i)
    
    def create_procedural_level(self, name, index):
        """Create a procedural level based on its name."""
        level = Level(name, width=3000 + index * 500)
        
        # Base platform
        level.add_platform(0, SCREEN_HEIGHT - 100, level.width, 100)
        
        # Add platforms based on difficulty progression
        difficulty_multiplier = 1 + (index * 0.15)
        platform_spacing = int(300 * difficulty_multiplier)
        platform_height_variance = int(50 * difficulty_multiplier)
        
        current_x = 300
        current_y = SCREEN_HEIGHT - 200
        
        while current_x < level.width - 500:
            # Platform width
            width = 150 + (index % 3) * 50
            
            # Height variation for difficulty
            height_change = (index % 5 - 2) * platform_height_variance
            current_y = max(100, min(SCREEN_HEIGHT - 150, current_y - height_change))
            
            level.add_platform(current_x, current_y, width, 30)
            
            # Add hazards at higher difficulties
            if index > 5:
                if (index // 5) % 2 == 0:
                    level.add_hazard(current_x + width // 2 - 15, current_y - 50, 30, 40, "spike")
            
            # Add checkpoints
            if current_x % (platform_spacing * 3) == 0:
                level.add_checkpoint(current_x, current_y - 100)
            
            current_x += platform_spacing
        
        # End platform
        level.add_platform(level.width - 300, SCREEN_HEIGHT - 200, 300, 30)
        level.add_checkpoint(level.width - 150, SCREEN_HEIGHT - 300)
        
        level.difficulty = ["Beginner", "Easy", "Normal", "Hard", "Very Hard", 
                           "Extreme", "Nightmare", "Insane", "Godlike", "Impossible"][min(index // 2, 9)]
        
        return level
    
    def load_campaign_level(self, level_name):
        """Load a campaign level by name."""
        if level_name in self.campaign_levels:
            return self.campaign_levels[level_name]
        return self.create_procedural_level(level_name, 0)
    
    def load_custom_level(self, filename):
        """Load a custom level from JSON file."""
        filepath = os.path.join(self.custom_levels_dir, filename)
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                level = Level(data.get("name", "Custom Level"), 
                            data.get("width", 3000),
                            data.get("height", SCREEN_HEIGHT))
                
                for platform in data.get("platforms", []):
                    level.add_platform(**platform)
                
                for hazard in data.get("hazards", []):
                    level.add_hazard(**hazard)
                
                return level
        except Exception as e:
            print(f"Error loading level {filename}: {e}")
            return None
    
    def save_custom_level(self, level, filename):
        """Save a custom level to JSON file."""
        filepath = os.path.join(self.custom_levels_dir, filename)
        try:
            data = {
                "name": level.name,
                "width": level.width,
                "height": level.height,
                "platforms": level.platforms,
                "hazards": level.hazards,
                "checkpoints": level.checkpoints,
                "scripts": level.scripts
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✓ Level saved: {filename}")
        except Exception as e:
            print(f"Error saving level {filename}: {e}")
