"""Simple command line interface for exploring regions and managing the party."""
from __future__ import annotations

from medieval_monsters.data import load_monsters, load_recipes, load_regions
from medieval_monsters.player.player import Player
from medieval_monsters.systems import exploration, survival


def _print_help() -> None:
    print("Commands: move <direction> | status | party | rest | recipes | help | quit")


def run_cli() -> None:
    regions = load_regions()
    monsters = load_monsters()
    recipes = load_recipes()

    player = Player(name="Aldric")
    player.add_to_party(monsters[0])

    current_region = next(iter(regions.values()))
    player.move_to(current_region.name)

    print("Welcome to Medieval Monsters! Type 'help' for available commands.")
    _print_help()

    while True:
        command = input(f"[{player.location}] > ").strip().lower()
        if not command:
            continue
        if command == "help":
            _print_help()
        elif command == "quit":
            print("Farewell, adventurer!")
            break
        elif command == "status":
            print(
                f"Health: {player.health} | Stamina: {player.stamina} | Hunger: {player.hunger}\n"
                f"Morale: {player.morale} | Exposure: {player.exposure}"
            )
        elif command == "party":
            if not player.party:
                print("Your party is empty.")
            else:
                for monster in player.party:
                    print(
                        f"{monster.name} (Lv {monster.level}) - HP {monster.current_hp}/{monster.max_hp}"
                    )
        elif command == "rest":
            player.rest()
            print("You rest and recover strength.")
        elif command == "recipes":
            for name, ingredients in recipes.items():
                parts = ", ".join(f"{item} x{qty}" for item, qty in ingredients.items())
                print(f"{name}: {parts}")
        elif command.startswith("move"):
            parts = command.split()
            if len(parts) != 2:
                print("Usage: move <direction>")
                continue
            direction = parts[1]
            if direction not in current_region.neighbors:
                print("You cannot travel that way.")
                continue
            current_region = current_region.neighbors[direction]
            exploration.travel(player, current_region)
            survival.apply_survival_tick(player, current_region)
            print(current_region.describe())
            encounter_chance = current_region.get_encounter_chance()
            print(
                "A tense aura surrounds you..." if encounter_chance > 0.4 else "The path seems calm."
            )
        else:
            print("Unknown command. Type 'help' for options.")


if __name__ == "__main__":
    run_cli()
