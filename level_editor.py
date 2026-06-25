"""Full scriptable level editor with node-based logic system."""

import pygame
import json
from config import *
from level_manager import Level

class ScriptNode:
    """Represents a logic node in the script editor."""
    
    def __init__(self, node_type, x, y):
        self.node_type = node_type  # "trigger", "condition", "action", "timer"
        self.position = [x, y]
        self.inputs = []
        self.outputs = []
        self.params = {}
        self.width = 120
        self.height = 60
    
    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.width, self.height)
    
    def render(self, screen, camera_x, camera_y):
        """Render the node."""
        x = self.position[0] - camera_x
        y = self.position[1] - camera_y
        rect = pygame.Rect(x, y, self.width, self.height)
        
        # Node colors based on type
        colors = {
            "trigger": TERTIARY_COLOR,
            "condition": PRIMARY_COLOR,
            "action": SECONDARY_COLOR,
            "timer": (200, 100, 255)
        }
        color = colors.get(self.node_type, TEXT_COLOR)
        
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, TEXT_COLOR, rect, 2)
        
        # Draw type text
        font = pygame.font.Font(None, 16)
        text = font.render(self.node_type, True, TEXT_COLOR)
        screen.blit(text, (x + 5, y + 20))

class LevelEditor:
    """Full-featured level editor with scripting."""
    
    def __init__(self):
        self.level = Level("Untitled Level")
        self.selected_tool = "platform"  # platform, hazard, checkpoint, script
        self.grid_snap = True
        self.zoom = DEFAULT_ZOOM
        self.camera_x = 0
        self.camera_y = 0
        self.selected_platforms = []
        self.selected_hazard = None
        self.script_nodes = []
        self.script_mode = False
        self.preview_mode = False
        self.clipboard = None
    
    def handle_input(self, event):
        """Handle editor input."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.place_object(event.pos)
            elif event.button == 3:  # Right click
                self.delete_object(event.pos)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                self.grid_snap = not self.grid_snap
            elif event.key == pygame.K_p:
                self.preview_mode = not self.preview_mode
            elif event.key == pygame.K_e:
                self.script_mode = not self.script_mode
            elif event.key == pygame.K_1:
                self.selected_tool = "platform"
            elif event.key == pygame.K_2:
                self.selected_tool = "hazard"
            elif event.key == pygame.K_3:
                self.selected_tool = "checkpoint"
            elif event.key == pygame.K_4:
                self.selected_tool = "script"
            elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.copy_selection()
            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.paste_selection(event.pos)
    
    def place_object(self, pos):
        """Place an object in the level."""
        world_x = pos[0] + self.camera_x
        world_y = pos[1] + self.camera_y
        
        if self.grid_snap:
            world_x = (world_x // GRID_SIZE) * GRID_SIZE
            world_y = (world_y // GRID_SIZE) * GRID_SIZE
        
        if self.selected_tool == "platform":
            self.level.add_platform(world_x, world_y, 100, 30)
        elif self.selected_tool == "hazard":
            self.level.add_hazard(world_x, world_y, 30, 30, "spike")
        elif self.selected_tool == "checkpoint":
            self.level.add_checkpoint(world_x, world_y)
        elif self.selected_tool == "script":
            node = ScriptNode("trigger", world_x, world_y)
            self.script_nodes.append(node)
    
    def delete_object(self, pos):
        """Delete an object from the level."""
        world_x = pos[0] + self.camera_x
        world_y = pos[1] + self.camera_y
        
        # Check platforms
        for platform in self.level.platforms[:]:
            if (platform["x"] <= world_x <= platform["x"] + platform["width"] and
                platform["y"] <= world_y <= platform["y"] + platform["height"]):
                self.level.platforms.remove(platform)
                return
        
        # Check hazards
        for hazard in self.level.hazards[:]:
            if (hazard["x"] <= world_x <= hazard["x"] + hazard["width"] and
                hazard["y"] <= world_y <= hazard["y"] + hazard["height"]):
                self.level.hazards.remove(hazard)
                return
    
    def copy_selection(self):
        """Copy selected objects to clipboard."""
        self.clipboard = {
            "platforms": self.selected_platforms.copy(),
            "hazards": [h for h in self.level.hazards if h in self.selected_platforms]
        }
    
    def paste_selection(self, pos):
        """Paste objects from clipboard."""
        if not self.clipboard:
            return
        
        world_x = pos[0] + self.camera_x
        world_y = pos[1] + self.camera_y
        
        for platform in self.clipboard.get("platforms", []):
            self.level.add_platform(world_x + platform["x"], world_y + platform["y"],
                                   platform["width"], platform["height"])
    
    def update(self, keys):
        """Update editor state."""
        # Pan camera with arrow keys
        if keys[pygame.K_LEFT]:
            self.camera_x -= 20
        if keys[pygame.K_RIGHT]:
            self.camera_x += 20
        if keys[pygame.K_UP]:
            self.camera_y -= 20
        if keys[pygame.K_DOWN]:
            self.camera_y += 20
    
    def render(self, screen):
        """Render the editor."""
        # Draw grid
        if self.grid_snap:
            for x in range(-int(self.camera_x) % GRID_SIZE, SCREEN_WIDTH, GRID_SIZE):
                pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT))
            for y in range(-int(self.camera_y) % GRID_SIZE, SCREEN_HEIGHT, GRID_SIZE):
                pygame.draw.line(screen, (50, 50, 50), (0, y), (SCREEN_WIDTH, y))
        
        # Draw level
        self.level.render(screen, self.camera_x, self.camera_y)
        
        # Draw script nodes
        for node in self.script_nodes:
            node.render(screen, self.camera_x, self.camera_y)
        
        # Draw UI
        self.render_ui(screen)
    
    def render_ui(self, screen):
        """Render editor UI."""
        font = pygame.font.Font(None, 24)
        
        # Tool indicator
        tool_text = f"Tool: {self.selected_tool.upper()}"
        text = font.render(tool_text, True, PRIMARY_COLOR)
        screen.blit(text, (10, 10))
        
        # Grid indicator
        grid_text = f"Grid: {'ON' if self.grid_snap else 'OFF'}"
        text = font.render(grid_text, True, PRIMARY_COLOR)
        screen.blit(text, (10, 40))
        
        # Mode indicator
        mode_text = f"Mode: {'SCRIPT' if self.script_mode else 'LAYOUT'}"
        text = font.render(mode_text, True, SECONDARY_COLOR)
        screen.blit(text, (10, 70))
        
        # Platform count
        count_text = f"Platforms: {len(self.level.platforms)} | Hazards: {len(self.level.hazards)}"
        text = font.render(count_text, True, TEXT_COLOR)
        screen.blit(text, (10, 100))
        
        # Controls
        controls_font = pygame.font.Font(None, 20)
        controls = [
            "1-4: Select Tool | G: Toggle Grid | P: Preview | E: Script Mode",
            "L-Click: Place | R-Click: Delete | Arrows: Pan | Ctrl+C: Copy | Ctrl+V: Paste"
        ]
        for i, ctrl in enumerate(controls):
            text = controls_font.render(ctrl, True, TEXT_COLOR)
            screen.blit(text, (10, SCREEN_HEIGHT - 50 + i * 25))

def save_level_to_file(level, filename):
    """Save level to JSON file."""
    data = {
        "name": level.name,
        "width": level.width,
        "height": level.height,
        "platforms": level.platforms,
        "hazards": level.hazards,
        "checkpoints": level.checkpoints,
        "difficulty": level.difficulty
    }
    with open(f"saves/custom_levels/{filename}.json", 'w') as f:
        json.dump(data, f, indent=2)

def load_level_from_file(filename):
    """Load level from JSON file."""
    try:
        with open(f"saves/custom_levels/{filename}.json", 'r') as f:
            data = json.load(f)
            level = Level(data["name"], data["width"], data["height"])
            level.platforms = data.get("platforms", [])
            level.hazards = data.get("hazards", [])
            level.checkpoints = data.get("checkpoints", [])
            return level
    except Exception as e:
        print(f"Error loading level: {e}")
        return None
