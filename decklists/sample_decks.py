"""
Sample deck archetypes, expressed as simplified PokemonCard stat blocks.
Names reference real archetypes for clarity in the Kaggle writeup; numeric
values are approximations for simulation, not reproductions of official
card text/art.
"""
from src.game_state import PokemonCard, Attack, Stage


def charizard_pidgeot_deck():
    charizard_ex = PokemonCard(
        name="Charizard ex", hp=330, stage=Stage.STAGE2,
        attacks=[Attack("Burning Darkness", cost=2, damage=180, effect="discard_energy:2")],
        weakness="Fighting", retreat_cost=2, is_ex=True,
    )
    pidgeot_ex = PokemonCard(
        name="Pidgeot ex", hp=280, stage=Stage.STAGE2,
        attacks=[Attack("Direction Rush", cost=1, damage=40)],
        weakness="Lightning", retreat_cost=1, is_ex=True,
    )
    charmander = PokemonCard("Charmander", hp=70, stage=Stage.BASIC,
                              attacks=[Attack("Ember", cost=1, damage=20)], retreat_cost=1)
    return [charizard_ex, pidgeot_ex, charmander, charmander]


def gardevoir_ex_deck():
    gardevoir_ex = PokemonCard(
        name="Gardevoir ex", hp=310, stage=Stage.STAGE2,
        attacks=[Attack("Psychic Embrace", cost=2, damage=120)],
        weakness="Metal", retreat_cost=2, is_ex=True,
    )
    kirlia = PokemonCard("Kirlia", hp=80, stage=Stage.STAGE1,
                          attacks=[Attack("Confusion", cost=1, damage=30)], retreat_cost=1)
    ralts = PokemonCard("Ralts", hp=60, stage=Stage.BASIC,
                         attacks=[Attack("Quick Attack", cost=1, damage=10)], retreat_cost=1)
    return [gardevoir_ex, kirlia, ralts, ralts]


def lost_zone_box_deck():
    sableye = PokemonCard("Sableye", hp=60, stage=Stage.BASIC,
                           attacks=[Attack("Impish Surprise", cost=0, damage=0)], retreat_cost=0)
    comfey = PokemonCard("Comfey", hp=90, stage=Stage.BASIC,
                          attacks=[Attack("Bouquet Hug", cost=2, damage=70)], retreat_cost=1)
    dusknoir = PokemonCard("Dusknoir", hp=160, stage=Stage.STAGE2,
                            attacks=[Attack("Sinister Hand", cost=2, damage=140)],
                            weakness="Dark", retreat_cost=2)
    return [sableye, comfey, dusknoir, comfey]
