"""Game state management and core game systems."""

import pygame
from config import *
from character import Character
from physics_engine import PhysicsEngine
from level_manager import LevelManager

class GameState:
    """Manages the overall game state, including character, level, and physics."""
    
    def __init__(self):
        self.character = Character(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)
        self.physics = PhysicsEngine()
        self.level_manager = LevelManager()
        self.current_level = "Beginner Roofs"
        self.level = None
        self.camera_x = 0
        self.camera_y = 0
        self.score = 0
        self.elapsed_time = 0
        self.load_level(self.current_level)
    
    def load_level(self, level_name):
        """Load a campaign level by name."""
        self.level = self.level_manager.load_campaign_level(level_name)
        if self.level:
            print(f"✓ Loaded level: {level_name}")
    
    def update(self):
        """Update game state each frame."""
        # Handle input
        keys = pygame.key.get_pressed()
        self.character.handle_input(keys)
        
        # Update physics
        self.physics.update(self.character, self.level)
        
        # Update camera
        self.update_camera()
        
        # Increment time
        self.elapsed_time += 1 / FPS
        
        # Check level completion
        if self.character.position[0] > self.level.width - 100:
            self.score += int(BASE_LEVEL_REWARD * DIFFICULTY_MULTIPLIER)
            print(f"Level complete! Score: {self.score}")
    
    def update_camera(self):
        """Update camera position to follow player."""
        target_x = self.character.position[0] - SCREEN_WIDTH // 3
        target_y = self.character.position[1] - SCREEN_HEIGHT // 2
        
        # Smooth camera movement
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.1
        
        # Clamp camera
        if self.level:
            self.camera_x = max(0, min(self.camera_x, self.level.width - SCREEN_WIDTH))
            self.camera_y = max(0, min(self.camera_y, self.level.height - SCREEN_HEIGHT))
    
    def render(self, screen):
        """Render the game to the screen."""
        # Draw level
        if self.level:
            self.level.render(screen, self.camera_x, self.camera_y)
        
        # Draw character
        char_x = self.character.position[0] - self.camera_x
        char_y = self.character.position[1] - self.camera_y
        
        # Character sprite (placeholder rectangle)
        pygame.draw.rect(screen, PRIMARY_COLOR, 
                         (char_x, char_y, CHAR_WIDTH, CHAR_HEIGHT))
        
        # Draw UI
        self.render_ui(screen)
    
    def render_ui(self, screen):
        """Render UI elements."""
        font = pygame.font.Font(None, 32)
        
        # Score
        score_text = font.render(f"Score: {self.score}", True, TEXT_COLOR)
        screen.blit(score_text, (20, 20))
        
        # Stamina bar
        stamina_percent = self.character.stamina / MAX_STAMINA
        bar_width = 200
        bar_height = 20
        pygame.draw.rect(screen, (100, 100, 100), (20, 60, bar_width, bar_height))
        pygame.draw.rect(screen, TERTIARY_COLOR, 
                         (20, 60, bar_width * stamina_percent, bar_height))
        pygame.draw.rect(screen, TEXT_COLOR, (20, 60, bar_width, bar_height), 2)
        
        stamina_text = font.render("Stamina", True, TEXT_COLOR)
        screen.blit(stamina_text, (20, 85))
        
        # Position
        pos_text = font.render(f"Pos: {int(self.character.position[0])}, {int(self.character.position[1])}", 
                              True, TEXT_COLOR)
        screen.blit(pos_text, (20, 120))
        
        # Time
        time_text = font.render(f"Time: {int(self.elapsed_time)}s", True, TEXT_COLOR)
        screen.blit(time_text, (SCREEN_WIDTH - 300, 20))
