from medieval_monsters.creatures.monster import Monster
from medieval_monsters.data import load_monsters
from medieval_monsters.systems.combat import (

    simulate_attack,
)



    damage, fainted = simulate_attack(monster, defender)
    assert damage > 0
    assert defender.current_hp == defender.max_hp - damage
    assert fainted == defender.is_fainted

    defender.apply_damage(8)

