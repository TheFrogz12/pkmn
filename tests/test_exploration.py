import random

from medieval_monsters.data import load_regions
from medieval_monsters.player.player import Player
from medieval_monsters.systems import exploration


def test_travel_returns_event_and_updates_location():
    regions = load_regions()
    glade = regions["Elder Glade"]
    destination = glade.neighbors["north"]
    player = Player(name="Scout")
    player.move_to(glade.name)

    rng = random.Random(0)
    event = exploration.travel(player, destination, rng=rng)

    assert player.location == destination.name
    assert event.encounter_chance == destination.get_encounter_chance()
    assert event.outcome in {"calm", "resource", "encounter"}


def test_forage_adds_resource_to_inventory():
    regions = load_regions()
    keep = regions["Stormwatch Keep"]
    player = Player(name="Forager")

    rng = random.Random(1)
    resource = exploration.forage(player, keep, rng=rng)

    assert resource in keep.biome.resources
    assert player.get_item_quantity(resource) == 1
