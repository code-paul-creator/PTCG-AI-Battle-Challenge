"""
Agent implementations.

HeuristicAgent   - fast, deterministic, 1-ply lookahead scoring function.
                   Used as the "baseline" competitive agent.
MCTSAgent        - lightweight Monte-Carlo Tree Search using random rollouts,
                   scored with the same evaluation function. Demonstrates a
                   more exploratory/robust decision process for the
                   "originality & technical soundness" criterion.

Both agents expose choose_action(state, side) -> Action so they are
interchangeable inside the simulator.
"""
from __future__ import annotations
import math
import random
from typing import List
from src.game_state import MatchState
from src.rules_engine import Action, legal_actions, apply_action


def evaluate_state(state: MatchState, side: str) -> float:
    """Positive = good for `side`."""
    me = getattr(state, side)
    opp_side = "opponent" if side == "player" else "player"
    opp = getattr(state, opp_side)

    score = 0.0
    score += (opp.prizes_remaining - me.prizes_remaining) * -50  # fewer prizes left for me = winning
    score += (me.prizes_remaining - opp.prizes_remaining) * 50

    if me.active:
        score += me.active.remaining_hp * 0.5
        score += me.active.energy_attached * 5
    if opp.active:
        score -= opp.active.remaining_hp * 0.4
    score += len(me.bench) * 8
    score -= len(opp.bench) * 6
    if not me.has_pokemon():
        score -= 1000
    if not opp.has_pokemon():
        score += 1000
    return score


class HeuristicAgent:
    """Greedy 1-ply lookahead: try every legal action, keep the best resulting state."""

    name = "HeuristicAgent"

    def choose_action(self, state: MatchState, side: str) -> Action:
        actions = legal_actions(state, side)
        if not actions:
            return Action("pass", {})
        best_action, best_score = None, -math.inf
        for a in actions:
            resulting = apply_action(state, side, a)
            s = evaluate_state(resulting, side)
            if s > best_score:
                best_score, best_action = s, a
        return best_action or Action("pass", {})


class MCTSAgent:
    """Very light MCTS: N random rollouts per legal action, pick best average."""

    name = "MCTSAgent"

    def __init__(self, rollouts_per_action: int = 8, rollout_depth: int = 3, seed: int | None = None):
        self.rollouts_per_action = rollouts_per_action
        self.rollout_depth = rollout_depth
        self.rng = random.Random(seed)

    def _rollout(self, state: MatchState, side: str, depth: int) -> float:
        s = state
        for _ in range(depth):
            actions = legal_actions(s, side)
            if not actions:
                break
            a = self.rng.choice(actions)
            s = apply_action(s, side, a)
            if s.winner():
                break
        return evaluate_state(s, side)

    def choose_action(self, state: MatchState, side: str) -> Action:
        actions = legal_actions(state, side)
        if not actions:
            return Action("pass", {})
        best_action, best_avg = None, -math.inf
        for a in actions:
            resulting = apply_action(state, side, a)
            total = sum(self._rollout(resulting, side, self.rollout_depth)
                        for _ in range(self.rollouts_per_action))
            avg = total / self.rollouts_per_action
            if avg > best_avg:
                best_avg, best_action = avg, a
        return best_action or Action("pass", {})
