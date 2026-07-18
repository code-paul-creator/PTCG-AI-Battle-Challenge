"""
Simulator: plays full matches between two agents using two decks, and reports
win rate + turn-count statistics across many repeated matches (this is the
evidence used for the "consistency under repeated matches" judging criterion).
"""
from __future__ import annotations
import random
import statistics
from typing import List, Tuple

from src.game_state import MatchState, PlayerState, InPlayPokemon
from src.rules_engine import legal_actions, apply_action, end_turn

MAX_TURNS = 60


def build_player(name: str, deck) -> PlayerState:
    shuffled = list(deck)
    random.shuffle(shuffled)  # models hand variance across repeated matches
    p = PlayerState(name=name, deck=shuffled, hand_energy=random.randint(3, 5))
    p.active = InPlayPokemon(card=shuffled[0])
    p.bench = [InPlayPokemon(card=c) for c in shuffled[1:3]]
    return p


def play_match(agent_a, agent_b, deck_a, deck_b, seed: int = 0) -> Tuple[str, int]:
    random.seed(seed)
    state = MatchState(
        player=build_player("player", deck_a),
        opponent=build_player("opponent", deck_b),
    )
    agents = {"player": agent_a, "opponent": agent_b}

    for _ in range(MAX_TURNS):
        side = state.active_player
        agent = agents[side]
        # an agent may take multiple non-attack actions, then must end with attack/pass
        for _ in range(4):
            action = agent.choose_action(state, side)
            state = apply_action(state, side, action)
            if action.kind in ("attack", "pass"):
                break
            if state.winner():
                break
        w = state.winner()  # returns "player", "opponent", or None
        if w:
            return w, state.turn_number
        state = end_turn(state)

    return "draw", MAX_TURNS


def run_tournament(agent_a, agent_b, deck_a, deck_b, n_matches: int = 200) -> dict:
    wins = {"player": 0, "opponent": 0, "draw": 0}
    turn_counts: List[int] = []
    for i in range(n_matches):
        winner, turns = play_match(agent_a, agent_b, deck_a, deck_b, seed=i)
        wins[winner] += 1
        turn_counts.append(turns)

    return {
        "matches": n_matches,
        "wins": {agent_a.name: wins["player"], agent_b.name: wins["opponent"], "draw": wins["draw"]},
        "win_rate_a": wins["player"] / n_matches,
        "win_rate_b": wins["opponent"] / n_matches,
        "draw_rate": wins["draw"] / n_matches,
        "avg_turns": statistics.mean(turn_counts),
        "stdev_turns": statistics.pstdev(turn_counts),
    }


if __name__ == "__main__":
    from src.agent import HeuristicAgent, MCTSAgent
    from decklists.sample_decks import charizard_pidgeot_deck, gardevoir_ex_deck

    result = run_tournament(
        HeuristicAgent(), MCTSAgent(rollouts_per_action=6, rollout_depth=3, seed=42),
        charizard_pidgeot_deck(), gardevoir_ex_deck(),
        n_matches=200,
    )
    print(result)
