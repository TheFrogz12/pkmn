from medieval_monsters.data import load_monsters, load_recipes, load_regions


def test_data_loaders_return_expected_structures():
    monsters = load_monsters()
    assert len(monsters) >= 3
    fire_monsters = [monster for monster in monsters if monster.element == "fire"]
    assert any(monster.skills for monster in fire_monsters)

    regions = load_regions()
    assert "Elder Glade" in regions
    glade = regions["Elder Glade"]
    assert "north" in glade.neighbors
    assert glade.neighbors["north"].name == "Stormwatch Keep"

    recipes = load_recipes()
    assert "Trail Rations" in recipes
    assert recipes["Trail Rations"]["wild grain"] == 2
