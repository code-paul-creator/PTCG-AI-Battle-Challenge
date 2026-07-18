"""
Core data model for the PTCG AI Battle Challenge simulator.

NOTE ON IP: Stats below are simplified/approximate numbers used purely to
model turn structure and decision-making. No official card text, artwork,
or copyrighted flavor text is reproduced. Card *names* are used only as
factual labels (comparable to a strategy article referencing a deck by name).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional
import copy


class Stage(Enum):
    BASIC = 0
    STAGE1 = 1
    STAGE2 = 2


@dataclass
class Attack:
    name: str
    cost: int              # simplified energy cost (count, not typed)
    damage: int
    effect: Optional[str] = None  # e.g. "self_damage:20", "discard_energy:1"


@dataclass
class PokemonCard:
    name: str
    hp: int
    stage: Stage
    attacks: List[Attack]
    weakness: Optional[str] = None   # +2x damage multiplier if type matches (abstracted)
    resistance: Optional[str] = None # -30 damage if type matches (abstracted)
    retreat_cost: int = 1
    is_ex: bool = False               # ex/ GX style cards give up 2 prizes when KO'd


@dataclass
class InPlayPokemon:
    card: PokemonCard
    damage_taken: int = 0
    energy_attached: int = 0
    turns_in_play: int = 0

    @property
    def remaining_hp(self) -> int:
        return max(0, self.card.hp - self.damage_taken)

    @property
    def is_knocked_out(self) -> bool:
        return self.remaining_hp <= 0


@dataclass
class PlayerState:
    name: str
    deck: List[PokemonCard] = field(default_factory=list)
    hand_energy: int = 4          # abstracted "energy in hand" pool
    active: Optional[InPlayPokemon] = None
    bench: List[InPlayPokemon] = field(default_factory=list)
    prizes_remaining: int = 6
    energy_played_this_turn: bool = False

    def all_in_play(self) -> List[InPlayPokemon]:
        return ([self.active] if self.active else []) + self.bench

    def has_pokemon(self) -> bool:
        return self.active is not None or len(self.bench) > 0


@dataclass
class MatchState:
    player: PlayerState
    opponent: PlayerState
    turn_number: int = 1
    active_player: str = "player"  # whose turn it is

    def clone(self) -> "MatchState":
        return copy.deepcopy(self)

    def winner(self) -> Optional[str]:
        if self.player.prizes_remaining <= 0 or not self.opponent.has_pokemon():
            return self.player.name
        if self.opponent.prizes_remaining <= 0 or not self.player.has_pokemon():
            return self.opponent.name
        return None
