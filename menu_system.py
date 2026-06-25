"""Main menu and UI system."""

import pygame
from config import *

class MenuSystem:
    """Handles all menu rendering and input."""
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.current_option = 0
        self.campaign_page = 0
        self.campaign_selected = None
        self.show_campaign_menu = False
    
    def handle_input(self, event):
        """Handle menu input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.current_option = (self.current_option - 1) % len(MENU_OPTIONS)
            elif event.key == pygame.K_DOWN:
                self.current_option = (self.current_option + 1) % len(MENU_OPTIONS)
            elif event.key == pygame.K_RETURN:
                self.current_option_selected = True
    
    def update(self):
        """Update menu state. Returns selected option index or None."""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.current_option = (self.current_option - 1) % len(MENU_OPTIONS)
        if keys[pygame.K_DOWN]:
            self.current_option = (self.current_option + 1) % len(MENU_OPTIONS)
        if keys[pygame.K_RETURN]:
            return self.current_option
        
        return None
    
    def update_campaign_select(self):
        """Update campaign selection menu. Returns selected level name or None."""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.campaign_page = (self.campaign_page - 1) % len(CAMPAIGN_LEVELS)
        if keys[pygame.K_DOWN]:
            self.campaign_page = (self.campaign_page + 1) % len(CAMPAIGN_LEVELS)
        if keys[pygame.K_RETURN]:
            return CAMPAIGN_LEVELS[self.campaign_page]
        
        return None
    
    def render(self, screen):
        """Render the main menu."""
        # Draw title
        title_font = pygame.font.Font(None, 96)
        title = title_font.render("PARKOUR", True, PRIMARY_COLOR)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        subtitle_font = pygame.font.Font(None, 48)
        subtitle = subtitle_font.render("2.5D Momentum Engine", True, SECONDARY_COLOR)
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 220))
        
        # Draw menu options
        menu_font = pygame.font.Font(None, 48)
        option_height = 80
        start_y = 400
        
        for i, option in enumerate(MENU_OPTIONS):
            color = PRIMARY_COLOR if i == self.current_option else TEXT_COLOR
            text = menu_font.render(option, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 
                              start_y + i * option_height))
        
        # Draw controls
        controls_font = pygame.font.Font(None, 24)
        controls = controls_font.render("UP/DOWN: Navigate | ENTER: Select | ESC: Exit", True, TEXT_COLOR)
        screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, SCREEN_HEIGHT - 50))
    
    def render_campaign_select(self, screen):
        """Render the campaign level selection menu."""
        # Title
        title_font = pygame.font.Font(None, 72)
        title = title_font.render("SELECT CAMPAIGN", True, PRIMARY_COLOR)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        # Level list with pagination
        levels_font = pygame.font.Font(None, 48)
        levels_per_page = 5
        page_start = (self.campaign_page // levels_per_page) * levels_per_page
        page_end = min(page_start + levels_per_page, len(CAMPAIGN_LEVELS))
        
        level_y = 200
        for i in range(page_start, page_end):
            level_name = CAMPAIGN_LEVELS[i]
            color = PRIMARY_COLOR if i == self.campaign_page else TEXT_COLOR
            text = levels_font.render(level_name, True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, level_y))
            level_y += 80
        
        # Current level info
        if 0 <= self.campaign_page < len(CAMPAIGN_LEVELS):
            info_font = pygame.font.Font(None, 32)
            current_level = CAMPAIGN_LEVELS[self.campaign_page]
            info = info_font.render(f"Level {self.campaign_page + 1} of {len(CAMPAIGN_LEVELS)}", 
                                   True, SECONDARY_COLOR)
            screen.blit(info, (SCREEN_WIDTH // 2 - info.get_width() // 2, SCREEN_HEIGHT - 150))
        
        # Controls
        controls_font = pygame.font.Font(None, 24)
        controls = controls_font.render("UP/DOWN: Select | ENTER: Play | ESC: Back", True, TEXT_COLOR)
        screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, SCREEN_HEIGHT - 50))
