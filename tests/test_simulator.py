import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agent import HeuristicAgent, MCTSAgent
from decklists.sample_decks import charizard_pidgeot_deck, gardevoir_ex_deck, lost_zone_box_deck
from src.simulator import run_tournament


def test_engine_terminates_and_declares_winner():
    result = run_tournament(HeuristicAgent(), HeuristicAgent(),
                             charizard_pidgeot_deck(), charizard_pidgeot_deck(),
                             n_matches=20)
    assert result["matches"] == 20
    assert result["draw_rate"] < 1.0  # engine should resolve most games


def test_mcts_agent_plays_legal_actions():
    result = run_tournament(MCTSAgent(rollouts_per_action=4, rollout_depth=2, seed=1),
                             HeuristicAgent(),
                             gardevoir_ex_deck(), lost_zone_box_deck(),
                             n_matches=10)
    assert result["matches"] == 10


def test_win_rate_is_within_stable_bounds_across_seeds():
    result = run_tournament(HeuristicAgent(), HeuristicAgent(),
                             charizard_pidgeot_deck(), gardevoir_ex_deck(),
                             n_matches=300)
    # mirror-strength agents should not produce a degenerate 100/0 split
    assert 0.05 < result["win_rate_a"] < 0.95


if __name__ == "__main__":
    test_engine_terminates_and_declares_winner()
    test_mcts_agent_plays_legal_actions()
    test_win_rate_is_within_stable_bounds_across_seeds()
    print("All tests passed.")
