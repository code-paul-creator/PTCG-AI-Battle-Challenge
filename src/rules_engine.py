"""
Rules engine: enumerates legal actions for a state and applies them.
Simplified but structurally faithful to real PTCG turn order:
  draw -> attach energy (1/turn) -> play/evolve/retreat -> attack -> end turn
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from src.game_state import MatchState, PlayerState, InPlayPokemon, PokemonCard, Attack


@dataclass
class Action:
    kind: str          # "attach_energy" | "retreat" | "bench_swap" | "attack" | "pass"
    payload: dict = None

    def __repr__(self):
        return f"{self.kind}({self.payload or ''})"


def legal_actions(state: MatchState, side: str) -> List[Action]:
    me: PlayerState = getattr(state, side)
    actions: List[Action] = []

    if me.active is None:
        if me.bench:
            actions.append(Action("promote", {"index": 0}))
        return actions

    if not me.energy_played_this_turn and me.hand_energy > 0:
        actions.append(Action("attach_energy", {"target": "active"}))
        for i, b in enumerate(me.bench):
            actions.append(Action("attach_energy", {"target": f"bench_{i}"}))

    for i, atk in enumerate(me.active.card.attacks):
        if me.active.energy_attached >= atk.cost:
            actions.append(Action("attack", {"attack_index": i}))

    if me.active.card.retreat_cost <= me.active.energy_attached and me.bench:
        actions.append(Action("retreat", {}))

    actions.append(Action("pass", {}))
    return actions


def apply_action(state: MatchState, side: str, action: Action) -> MatchState:
    new_state = state.clone()
    me: PlayerState = getattr(new_state, side)
    opp_side = "opponent" if side == "player" else "player"
    opp: PlayerState = getattr(new_state, opp_side)

    if action.kind == "promote":
        idx = action.payload["index"]
        me.active = me.bench.pop(idx)

    elif action.kind == "attach_energy":
        target = action.payload["target"]
        if target == "active":
            me.active.energy_attached += 1
        else:
            idx = int(target.split("_")[1])
            me.bench[idx].energy_attached += 1
        me.hand_energy -= 1
        me.energy_played_this_turn = True

    elif action.kind == "retreat":
        me.bench.append(me.active)
        me.active = me.bench.pop(0)

    elif action.kind == "attack":
        atk: Attack = me.active.card.attacks[action.payload["attack_index"]]
        dmg = atk.damage
        if opp.active and me.active.card.weakness and opp.active.card.name == me.active.card.weakness:
            dmg *= 2
        if opp.active and me.active.card.resistance and opp.active.card.name == me.active.card.resistance:
            dmg = max(0, dmg - 30)
        if opp.active:
            opp.active.damage_taken += dmg
            if opp.active.is_knocked_out:
                prizes_taken = 2 if opp.active.card.is_ex else 1
                opp.prizes_remaining = max(0, opp.prizes_remaining - prizes_taken)
                opp.active = opp.bench.pop(0) if opp.bench else None

    # "pass" requires no state change

    return new_state


def end_turn(state: MatchState) -> MatchState:
    new_state = state.clone()
    new_state.turn_number += 1
    new_state.active_player = "opponent" if state.active_player == "player" else "player"
    side = new_state.active_player
    me: PlayerState = getattr(new_state, side)
    me.energy_played_this_turn = False
    me.hand_energy = min(me.hand_energy + 1, 8)  # simplified draw/energy income
    for p in me.all_in_play():
        p.turns_in_play += 1
    return new_state
