#!/usr/bin/env python3
"""Main entry point for the Parkour Game Engine."""

import pygame
import sys
from config import *
from menu_system import MenuSystem
from game_state import GameState

class Game:
    """Main game class managing the game loop and state transitions."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Parkour Game Engine - 2.5D Momentum-Based")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize game state
        self.state = GameState()
        self.menu = MenuSystem(self.state)
        self.current_state = "MENU"  # MENU, CAMPAIGN_SELECT, GAMEPLAY, EDITOR, MARKETPLACE, SETTINGS
        
        print("\n" + "="*60)
        print("  PARKOUR GAME ENGINE - 2.5D MOMENTUM-BASED")
        print("="*60)
        print(f"Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        print(f"FPS: {FPS}")
        print("Ready to start...\n")
    
    def handle_events(self):
        """Handle all input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_state == "GAMEPLAY":
                        self.current_state = "CAMPAIGN_SELECT"
                    elif self.current_state in ["EDITOR", "MARKETPLACE", "SETTINGS"]:
                        self.current_state = "MENU"
                    else:
                        self.running = False
                
                # Route event to current state
                if self.current_state == "MENU":
                    self.menu.handle_input(event)
    
    def update(self):
        """Update game logic based on current state."""
        if self.current_state == "MENU":
            selection = self.menu.update()
            if selection == 0:  # Play Campaign
                self.current_state = "CAMPAIGN_SELECT"
            elif selection == 1:  # Level Editor
                self.current_state = "EDITOR"
            elif selection == 2:  # Marketplace
                self.current_state = "MARKETPLACE"
            elif selection == 3:  # Settings
                self.current_state = "SETTINGS"
            elif selection == 4:  # Exit
                self.running = False
        
        elif self.current_state == "CAMPAIGN_SELECT":
            level = self.menu.update_campaign_select()
            if level is not None:
                self.state.current_level = level
                self.current_state = "GAMEPLAY"
        
        elif self.current_state == "GAMEPLAY":
            # Update gameplay (physics, character, etc.)
            self.state.update()
        
        elif self.current_state == "EDITOR":
            # Update level editor
            pass
        
        elif self.current_state == "MARKETPLACE":
            # Update marketplace
            pass
        
        elif self.current_state == "SETTINGS":
            # Update settings menu
            pass
    
    def render(self):
        """Render the current game state."""
        self.screen.fill(BG_COLOR)
        
        if self.current_state == "MENU":
            self.menu.render(self.screen)
        elif self.current_state == "CAMPAIGN_SELECT":
            self.menu.render_campaign_select(self.screen)
        elif self.current_state == "GAMEPLAY":
            self.state.render(self.screen)
        elif self.current_state == "EDITOR":
            self.render_editor()
        elif self.current_state == "MARKETPLACE":
            self.render_marketplace()
        elif self.current_state == "SETTINGS":
            self.render_settings()
        
        pygame.display.flip()
    
    def render_editor(self):
        """Render level editor."""
        font = pygame.font.Font(None, 48)
        text = font.render("LEVEL EDITOR", True, PRIMARY_COLOR)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100))
    
    def render_marketplace(self):
        """Render marketplace."""
        font = pygame.font.Font(None, 48)
        text = font.render("MARKETPLACE", True, SECONDARY_COLOR)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100))
    
    def render_settings(self):
        """Render settings menu."""
        font = pygame.font.Font(None, 48)
        text = font.render("SETTINGS", True, TERTIARY_COLOR)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100))
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        print("\n✓ Game closed successfully")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
