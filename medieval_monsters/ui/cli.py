"""Simple command line interface for exploring regions and managing the party."""
from __future__ import annotations

import random

from medieval_monsters.data import load_monsters, load_recipes, load_regions
from medieval_monsters.player.player import Player
from medieval_monsters.systems import exploration, survival


def _print_help() -> None:
    print(
        "Commands: move <direction> | status | party | inventory | forage | rest [full] | recipes | map | help | quit"
    )


def _print_map(region_name: str, neighbors) -> None:
    print(f"You are currently in {region_name}.")
    if not neighbors:
        print("No paths lead away from here.")
        return
    print("Available paths:")
    for direction, region in neighbors:
        print(f"  {direction.title()}: {region.name} (Danger {region.danger_level})")


def run_cli() -> None:
    rng = random.Random()
    regions = load_regions()
    monsters = load_monsters()
    recipes = load_recipes()

    player = Player(name="Aldric")
    if monsters:
        player.add_to_party(monsters[0])

    current_region = next(iter(regions.values()))
    player.move_to(current_region.name)

    print("Welcome to Medieval Monsters! Type 'help' for available commands.")
    _print_help()

    while True:
        command = input(f"[{player.location}] > ").strip().lower()
        if not command:
            continue
        parts = command.split()
        action = parts[0]

        if action == "help":
            _print_help()
        elif action == "quit":
            print("Farewell, adventurer!")
            break
        elif action == "status":
            print(player.status_report())
        elif action == "party":
            if not player.party:
                print("Your party is empty.")
            else:
                for idx, monster in enumerate(player.party, start=1):
                    marker = "*" if idx == 1 else "-"
                    print(
                        f"{marker} {monster.name} (Lv {monster.level}) - HP {monster.current_hp}/{monster.max_hp}"
                    )
        elif action == "inventory":
            print("Inventory:")
            for line in player.inventory_summary():
                print(f"  {line}")
        elif action == "rest":
            full_rest = len(parts) > 1 and parts[1] == "full"
            player.rest(full=full_rest)
            print("You take time to rest and recuperate.")
        elif action == "recipes":
            print("Known recipes:")
            for name, ingredients in recipes.items():
                parts_desc = ", ".join(f"{item} x{qty}" for item, qty in ingredients.items())
                print(f"  {name}: {parts_desc}")
        elif action == "map":
            _print_map(current_region.name, [(d, current_region.neighbors[d]) for d in current_region.available_directions()])
        elif action == "forage":
            resource = exploration.forage(player, current_region, rng=rng)
            if resource:
                print(f"You gather {resource} and add it to your packs.")
            else:
                print("There is little of use to gather here.")
        elif action == "move":
            if len(parts) != 2:
                print("Usage: move <direction>")
                continue
            direction = parts[1]
            if direction not in current_region.neighbors:
                print("You cannot travel that way.")
                continue
            current_region = current_region.neighbors[direction]
            event = exploration.travel(player, current_region, rng=rng)
            survival_events = survival.apply_survival_tick(player, current_region)
            print(current_region.describe())
            for note in survival_events:
                print(f"* {note}")
            print(event.description)
            if event.outcome == "encounter":
                print("(A placeholder encounter begins...)")
        else:
            print("Unknown command. Type 'help' for options.")


if __name__ == "__main__":
    run_cli()
