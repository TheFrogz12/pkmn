"""Simple command line interface for exploring regions and managing the party."""
from __future__ import annotations


from medieval_monsters.data import load_monsters, load_recipes, load_regions
from medieval_monsters.player.player import Player
from medieval_monsters.systems import exploration, survival


def _print_help() -> None:

    regions = load_regions()
    monsters = load_monsters()
    recipes = load_recipes()

    player = Player(name="Aldric")


    current_region = next(iter(regions.values()))
    player.move_to(current_region.name)

    print("Welcome to Medieval Monsters! Type 'help' for available commands.")
    _print_help()

    while True:
        command = input(f"[{player.location}] > ").strip().lower()
        if not command:
            continue

            if len(parts) != 2:
                print("Usage: move <direction>")
                continue
            direction = parts[1]
            if direction not in current_region.neighbors:
                print("You cannot travel that way.")
                continue
            current_region = current_region.neighbors[direction]

        else:
            print("Unknown command. Type 'help' for options.")


if __name__ == "__main__":
    run_cli()
