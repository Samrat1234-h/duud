"""Physics engine handling collision detection and momentum calculations."""

import pygame
from config import *

class PhysicsEngine:
    """Manages physics including collision detection and response."""
    
    def __init__(self):
        self.gravity = GRAVITY
        self.friction = FRICTION
        self.max_fall_speed = MAX_FALL_SPEED
    
    def update(self, character, level):
        """Update character physics based on level collisions."""
        # Update character
        character.update()
        
        # Check collisions with level platforms
        if level:
            self.check_collisions(character, level)
    
    def check_collisions(self, character, level):
        """Check and resolve collisions with level platforms."""
        char_rect = character.get_hitbox()
        
        # Check ground collision (simple version)
        character.on_ground = False
        
        for platform in level.platforms:
            platform_rect = pygame.Rect(platform["x"], platform["y"], 
                                       platform["width"], platform["height"])
            
            if char_rect.colliderect(platform_rect):
                # Determine collision direction
                # Coming from above
                if character.velocity[1] >= 0 and character.position[1] + CHAR_HEIGHT - platform["y"] < CHAR_HEIGHT // 2:
                    character.position[1] = platform["y"] - CHAR_HEIGHT
                    character.velocity[1] = 0
                    character.on_ground = True
                    character.is_jumping = False
                
                # Coming from below
                elif character.velocity[1] < 0 and platform["y"] + platform["height"] - character.position[1] < CHAR_HEIGHT // 2:
                    character.position[1] = platform["y"] + platform["height"]
                    character.velocity[1] = 0
                
                # Coming from left
                elif character.velocity[0] > 0 and character.position[0] + CHAR_WIDTH - platform["x"] < CHAR_WIDTH // 2:
                    character.position[0] = platform["x"] - CHAR_WIDTH
                    character.velocity[0] *= 0.5
                
                # Coming from right
                elif character.velocity[0] < 0 and platform["x"] + platform["width"] - character.position[0] < CHAR_WIDTH // 2:
                    character.position[0] = platform["x"] + platform["width"]
                    character.velocity[0] *= 0.5
        
        # Check hazard collisions
        for hazard in level.hazards:
            hazard_rect = pygame.Rect(hazard["x"], hazard["y"],
                                     hazard["width"], hazard["height"])
            
            if char_rect.colliderect(hazard_rect):
                # Reset character to last checkpoint
                if hasattr(level, 'last_checkpoint'):
                    character.position = level.last_checkpoint
                    character.velocity = [0, 0]
                else:
                    character.position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200]
                    character.velocity = [0, 0]
    
    def apply_momentum(self, character, velocity_change):
        """Apply additional momentum to the character."""
        character.velocity[0] += velocity_change[0]
        character.velocity[1] += velocity_change[1]
        
        # Clamp velocity
        character.velocity[0] = max(-MAX_SPEED * 2, min(character.velocity[0], MAX_SPEED * 2))
        character.velocity[1] = min(character.velocity[1], MAX_FALL_SPEED * 2)
