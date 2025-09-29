from medieval_monsters.data import load_regions
from medieval_monsters.player.player import Player
from medieval_monsters.systems.survival import apply_survival_tick


def test_survival_tick_increases_need_and_causes_penalties():
    regions = load_regions()
    glade = regions["Elder Glade"]
    player = Player(name="Test", hunger=90, exposure=90, morale=50, health=80, stamina=70)

    events = apply_survival_tick(player, glade, hours=3, auto_consume_rations=False)

    assert events == []
    assert player.hunger >= 90
    assert player.exposure >= 90
    assert player.morale < 50

    # Hunger should eventually drain health when maxed
    player.hunger = player.MAX_STAT
    apply_survival_tick(player, glade, hours=1, auto_consume_rations=False)
    assert player.health < 80


def test_survival_tick_consumes_rations_when_available():
    regions = load_regions()
    keep = regions["Stormwatch Keep"]
    player = Player(name="Test", hunger=75, morale=40)
    player.add_item("Trail Rations", 1)

    events = apply_survival_tick(player, keep)

    assert any("Trail Rations" in event for event in events)
    assert player.get_item_quantity("Trail Rations") == 0
    assert player.hunger < 75
    assert player.morale >= 40


def test_player_rest_recovers_resources():
    player = Player(name="Test", hunger=60, exposure=60, morale=20, health=50, stamina=30)
    player.rest()
    assert player.hunger < 60
    assert player.exposure < 60
    assert player.health > 50
    assert player.stamina > 30

    player.rest(full=True)
    assert player.health == player.MAX_STAT or player.health > 50
