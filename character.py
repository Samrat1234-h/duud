"""Player character system with animation and input handling."""

import pygame
import math
from config import *

class Character:
    """Represents the player character with movement and animation."""
    
    def __init__(self, x, y):
        self.position = [x, y]
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        
        # State
        self.is_jumping = False
        self.is_falling = False
        self.is_sliding = False
        self.is_wall_running = False
        self.facing_right = True
        self.on_ground = False
        
        # Stamina
        self.stamina = MAX_STAMINA
        self.stamina_regen_timer = 0
        
        # Animation
        self.animation_state = "idle"  # idle, running, jumping, falling, sliding, wall_running
        self.animation_frame = 0
        self.animation_timer = 0
        
        # Hitbox
        self.width = CHAR_WIDTH
        self.height = CHAR_HEIGHT
        self.hitbox_offset = CHAR_HITBOX_OFFSET
        
        # Slide mechanics
        self.slide_timer = 0
        self.original_height = CHAR_HEIGHT
    
    def get_hitbox(self):
        """Return the character's current hitbox."""
        return pygame.Rect(self.position[0] + self.hitbox_offset[0],
                          self.position[1] + self.hitbox_offset[1],
                          self.width, self.height)
    
    def handle_input(self, keys):
        """Handle keyboard input for movement."""
        # Movement input
        accel = 0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            accel += ACCELERATION
            self.animation_state = "running"
        
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            accel -= ACCELERATION * 0.5  # Backward is slower
            self.animation_state = "running"
        
        # Strafe (for future implementation)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.facing_right = False
        
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.facing_right = True
        
        # Jump
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
        
        # Dash/Sprint
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            if self.stamina >= DASH_COST:
                accel *= 1.5  # Speed boost
                self.stamina -= DASH_COST * 0.016  # Per frame cost
                self.animation_state = "sprinting"
        
        # Slide
        if keys[pygame.K_q]:
            self.slide()
        
        # Apply acceleration
        if self.on_ground:
            self.acceleration[0] = accel
        else:
            self.acceleration[0] = accel * 0.5  # Reduced air control
    
    def jump(self):
        """Handle jump mechanics."""
        if self.on_ground:
            self.velocity[1] = -JUMP_POWER
            self.is_jumping = True
            self.on_ground = False
            self.animation_state = "jumping"
    
    def slide(self):
        """Handle sliding mechanics."""
        if self.on_ground and not self.is_sliding:
            self.is_sliding = True
            self.slide_timer = SLIDE_DURATION
            self.height = CHAR_HEIGHT * SLIDE_HEIGHT_REDUCTION
            self.velocity[0] *= SLIDE_SPEED_MULTIPLIER
            self.animation_state = "sliding"
    
    def update(self, dt=1/FPS):
        """Update character state each frame."""
        # Apply gravity
        if not self.on_ground:
            self.velocity[1] += GRAVITY
            self.velocity[1] = min(self.velocity[1], MAX_FALL_SPEED)
            self.animation_state = "falling"
        
        # Apply friction
        friction = FRICTION if self.on_ground else AIR_FRICTION
        if not (self.is_sliding or self.is_wall_running):
            self.velocity[0] *= friction
        
        # Apply acceleration
        self.velocity[0] += self.acceleration[0]
        self.velocity[0] = max(-MAX_SPEED, min(self.velocity[0], MAX_SPEED))
        
        # Update position
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        # Update slide
        if self.is_sliding:
            self.slide_timer -= 1
            if self.slide_timer <= 0:
                self.is_sliding = False
                self.height = self.original_height
        
        # Update stamina
        if self.stamina < MAX_STAMINA:
            self.stamina += STAMINA_REGEN
        self.stamina = min(self.stamina, MAX_STAMINA)
        
        # Update animation
        self.update_animation()
    
    def update_animation(self):
        """Update animation frame based on state."""
        self.animation_timer += 1
        
        frame_duration = 5
        if self.animation_timer >= frame_duration:
            self.animation_frame = (self.animation_frame + 1) % 4
            self.animation_timer = 0
    
    def reset_position(self, x, y):
        """Reset character to a specific position (for checkpoints)."""
        self.position = [x, y]
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.on_ground = True
        self.animation_state = "idle"
