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
    assert event.outcome in {"calm", "resource", "encounter", "hazard"}


def test_forage_adds_resource_to_inventory():
    regions = load_regions()
    keep = regions["Stormwatch Keep"]
    player = Player(name="Forager")

    rng = random.Random(1)
    resource = exploration.forage(player, keep, rng=rng)

    assert resource in keep.biome.resources
    assert player.get_item_quantity(resource) == 1


class FixedRandom:
    def __init__(self, *, roll: float, choice_value=None):
        self.roll = roll
        self.choice_value = choice_value

    def random(self):
        return self.roll

    def choice(self, seq):
        if self.choice_value is not None:
            return self.choice_value
        return seq[0]


def test_hazard_events_reduce_player_resources():
    regions = load_regions()
    fen = regions["Bogmire Fen"]
    player = Player(name="Surveyor", health=90, stamina=80, morale=60)

    rng = FixedRandom(roll=0.8)
    event = exploration.roll_event(fen, rng=rng)

    assert event.outcome == "hazard"

    notes = exploration.resolve_event(player, fen, event, rng=rng)

    assert player.health < 90
    assert player.stamina < 80
    assert player.morale < 60
    assert any("Hazards" in note for note in notes)
