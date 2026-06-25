"""Sprite sheet animation system for character and objects."""

import pygame
from config import *

class SpriteSheet:
    """Manages sprite sheets and animations."""
    
    def __init__(self, filepath, frame_width, frame_height):
        self.image = pygame.Surface((frame_width, frame_height))
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frames = []
        self.load_frames()
    
    def load_frames(self):
        """Load animation frames from sprite sheet."""
        # Placeholder: would load actual sprite sheets
        for i in range(4):
            frame = pygame.Surface((self.frame_width, self.frame_height))
            frame.fill(PRIMARY_COLOR)
            self.frames.append(frame)

class AnimationPlayer:
    """Manages animation playback for sprites."""
    
    def __init__(self):
        self.animations = {}
        self.current_animation = None
        self.frame_index = 0
        self.frame_timer = 0
        self.is_playing = False
    
    def add_animation(self, name, frames, frame_duration):
        """Add an animation to the player."""
        self.animations[name] = {
            "frames": frames,
            "duration": frame_duration
        }
    
    def play(self, animation_name, loop=True):
        """Play an animation."""
        if animation_name in self.animations:
            self.current_animation = animation_name
            self.frame_index = 0
            self.frame_timer = 0
            self.is_playing = True
    
    def stop(self):
        """Stop the current animation."""
        self.is_playing = False
    
    def update(self):
        """Update animation playback."""
        if not self.is_playing or not self.current_animation:
            return
        
        anim = self.animations[self.current_animation]
        self.frame_timer += 1
        
        if self.frame_timer >= anim["duration"]:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(anim["frames"])
    
    def get_current_frame(self):
        """Get the current animation frame."""
        if not self.current_animation:
            return None
        
        anim = self.animations[self.current_animation]
        return anim["frames"][self.frame_index]

# Predefined animations for the character
CHARACTER_ANIMATIONS = {
    "idle": {
        "frames": 2,
        "duration": 10
    },
    "running": {
        "frames": 4,
        "duration": 5
    },
    "jumping": {
        "frames": 3,
        "duration": 4
    },
    "falling": {
        "frames": 2,
        "duration": 8
    },
    "sliding": {
        "frames": 3,
        "duration": 5
    },
    "wall_running": {
        "frames": 3,
        "duration": 6
    },
    "sprinting": {
        "frames": 4,
        "duration": 4
    }
}
