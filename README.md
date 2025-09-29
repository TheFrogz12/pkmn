# Medieval Survival Monster RPG Design Blueprint

This document outlines the initial structure and gameplay pillars for the medieval, survival-focused monster-catching game to be implemented in Python. It establishes the guiding principles, module layout, and data-driven approach that the upcoming codebase will follow.

## Core Fantasy and Pillars
- **Mythic Monster Companions:** Collect, befriend, and battle with creatures inspired by medieval folklore.
- **Survival Mechanics:** Manage hunger, stamina, shelter, and crafting in a harsh overworld.
- **Exploration:** Traverse procedurally generated regions filled with biomes, events, and secrets.
- **Medieval Flavor:** Gear, settlements, and resources rooted in a low-fantasy setting.

## High-Level Architecture
```
medieval_monsters/
├── __init__.py
├── player/
│   ├── __init__.py
│   └── player.py
├── creatures/
│   ├── __init__.py
│   └── monster.py
├── world/
│   ├── __init__.py
│   └── regions.py
├── systems/
│   ├── __init__.py
│   ├── exploration.py
│   ├── combat.py
│   └── survival.py
├── data/
│   ├── monsters.json
│   ├── regions.json
│   └── recipes.json
└── ui/
    ├── __init__.py
    └── cli.py
```

### Module Responsibilities
- `player`: Player stats, inventory, party management, and survival vitals.
- `creatures`: Monster classes, elemental affinities, abilities, and lore hooks.
- `world`: Region definitions, biome data, and encounter tables.
- `systems`
  - `exploration`: Tile/hex-grid traversal, biome generation, and random events.
  - `combat`: Turn-based resolution mixing monster skills and player gear.
  - `survival`: Hunger, fatigue, crafting, and shelter upkeep.
- `ui`: Command-line loop for exploration, encounters, and resource management.
- `data`: JSON/YAML assets powering monsters, regions, items, and events.

## Key Gameplay Loops
1. **Explore:** Player selects movement direction, triggering biome updates and chance-based encounters.
2. **Encounter:** Combat against roaming monsters or story events, with options to capture creatures.
3. **Survive:** Consume resources, craft equipment, and rest to maintain health, morale, and stamina.

These loops feed into each other, creating an emergent rhythm: exploration yields resources and monsters, which support survival and expand the roster, enabling deeper exploration.

## Systems Overview
### Exploration
- Procedurally generate regions based on biome templates.
- Track time of day, weather, and risk levels affecting encounters.
- Surface events (ambushes, ruins, NPCs) via weighted tables.

### Combat
- Turn order derived from agility and initiative bonuses.
- Monster abilities use elemental strengths/weaknesses, status effects, and combo actions with player gear.
- Capture mechanics influenced by monster morale, health, and special items.

### Survival
- Vitals: health, stamina, hunger, morale, exposure.
- Resource loops: gather → craft → upgrade gear or shelter.
- Camp management for rest, crafting, and party interactions.

## Data-Driven Content
All content (monsters, regions, recipes, events) should be defined via JSON/YAML and loaded at runtime. This allows tuning and expansion without altering core logic.

## Next Steps
1. Scaffold the Python package with the module structure above.
2. Implement foundational classes (`Player`, `Monster`, `Region`).
3. Set up data loaders for monsters, regions, and recipes.
4. Build initial command-line interface enabling movement and status checks.
5. Add tests for combat resolution, survival tick updates, and capture calculations.

This blueprint serves as the north star for subsequent implementation passes.
