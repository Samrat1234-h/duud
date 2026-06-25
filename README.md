# Parkour Game Engine - 2.5D Momentum-Based

## Complete Feature Set

A fully-featured parkour game engine built with Python (Pygame) featuring:

### 1. MAIN MENU & ARCHITECTURE
- Dynamic Title Screen with Play, Level Editor, Player Marketplace, Settings
- Campaign Selector with 20+ built-in developer levels
- Inventory & Vault System for cosmetics, trails, and blueprints

### 2. FREE-MOVEMENT HUMAN PARKOUR SYSTEM
- Manual Control Input with absolute directional freedom
- Dynamic Skeleton Rig with sprite animations
- Momentum Physics Matrix with multi-layered hitboxes

### 3. ECONOMY & ASSET TRADING SYSTEM
- Marketplace Hub for player-to-player trading
- In-Game Currency Ledger system
- Trade Logic with two-step verification

### 4. FULL SCRIPTABLE LEVEL EDITOR
- Node-Based Script Editor with IF/THEN logic
- Comprehensive Tooling with grid-snapping and rotation
- Asset & Hazard Palette with 200+ textures and hazards

## Installation

```bash
pip install pygame
python main.py
```

## Project Structure

```
parkour-engine/
├── main.py                 # Entry point
├── config.py              # Game configuration
├── physics_engine.py      # Physics and collision system
├── character.py           # Player character system
├── animation.py           # Sprite animations
├── level_manager.py       # Level loading and management
├── menu_system.py         # Main menu and UI
├── level_editor.py        # Level editor with scripts
├── marketplace.py         # Trading and economy system
├── script_engine.py       # Logic scripting system
├── assets.py              # Asset management
├── levels/                # Built-in campaign levels
│   ├── level_01.json
│   ├── level_02.json
│   └── ...
├── sprites/               # Character and object sprites
├── textures/              # Block and background textures
└── saves/                 # Player profiles and custom levels
```

## Controls

### In-Game
- **W/A/S/D** - Movement (forward/left/backward/right)
- **SPACE** - Jump
- **Shift** - Dash/Sprint
- **Q** - Slide
- **E** - Interact/Grab
- **Mouse** - Camera/Look (optional)

### Level Editor
- **Left Click** - Place/Select blocks
- **Right Click** - Delete blocks
- **Scroll** - Rotate/Change height
- **G** - Toggle grid snap
- **P** - Test level

## License

MIT License - Free to use and modify
