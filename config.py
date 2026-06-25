"""Game configuration and constants."""

import pygame

# Display Settings
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60

# Physics Constants
GRAVITY = 0.6
MAX_FALL_SPEED = 20
FRICTION = 0.92
AIR_FRICTION = 0.99
DASH_SPEED = 15
MAX_SPEED = 12
ACCELERATION = 0.8

# Jump Physics
JUMP_POWER = 15
WALL_JUMP_POWER = 12
WALL_SLIDE_FRICTION = 0.95
DOUBLE_JUMP_POWER = 13

# Slide Mechanics
SLIDE_SPEED_MULTIPLIER = 1.3
SLIDE_DURATION = 30
SLIDE_HEIGHT_REDUCTION = 0.6

# Stamina System
MAX_STAMINA = 100
DASH_COST = 25
WALL_RUN_DRAIN = 1.5
STAMINA_REGEN = 0.5

# Character Settings
CHAR_WIDTH = 32
CHAR_HEIGHT = 64
CHAR_HITBOX_OFFSET = (0, 8)

# Colors
BG_COLOR = (15, 20, 30)
PRIMARY_COLOR = (0, 200, 255)
SECONDARY_COLOR = (255, 100, 200)
TERTIARY_COLOR = (100, 255, 100)
TEXT_COLOR = (255, 255, 255)
UI_COLOR = (30, 40, 60)

# Menu
MENU_OPTIONS = [
    "PLAY CAMPAIGN",
    "LEVEL EDITOR",
    "MARKETPLACE",
    "SETTINGS",
    "EXIT"
]

CAMPAIGN_LEVELS = [
    "Beginner Roofs",
    "Urban Junction",
    "Warehouse Maze",
    "Factory Floor",
    "Glass Towers",
    "Neon District",
    "Sky Bridges",
    "Underground Tunnels",
    "Mountain Ridge",
    "Cyber Vaults",
    "Jungle Ruins",
    "Steam Pipes",
    "Crystal Caverns",
    "Storm Temple",
    "Void Sanctum",
    "Gravity Wells",
    "Temporal Rifts",
    "Infinite Loop",
    "Mirror Realm",
    "Impossibly Flawless Vaults"
]

# Trading
BASE_LEVEL_REWARD = 500
DIFFICULTY_MULTIPLIER = 1.5
TIME_BONUS = 100

# Asset Categories
ASSET_CATEGORIES = {
    "COSMETICS": ["Hoodies", "Pants", "Shoes", "Masks", "Hair"],
    "TRAILS": ["Neon", "Fire", "Ice", "Electric", "Smoke"],
    "BLOCKS": ["Concrete", "Metal", "Glass", "Neon", "Organic"],
    "SCRIPTS": ["Logic Gates", "Triggers", "Timers", "Hazards"]
}

# Level Editor
GRID_SIZE = 32
MIN_ZOOM = 0.5
MAX_ZOOM = 3.0
DEFAULT_ZOOM = 1.0
MAX_LEVEL_SIZE = 200  # In tiles

# Layers
LAYER_BACKGROUND = 0
LAYER_PLATFORMS = 1
LAYER_OBJECTS = 2
LAYER_HAZARDS = 3
LAYER_PARTICLES = 4
LAYER_UI = 5

print("✓ Configuration loaded successfully")
