import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.agent import HeuristicAgent, MCTSAgent
from decklists.sample_decks import charizard_pidgeot_deck, gardevoir_ex_deck
from src.simulator import run_tournament

N_BATCHES = 15
MATCHES_PER_BATCH = 100

heuristic_rates, mcts_rates = [], []
for b in range(N_BATCHES):
    r = run_tournament(
        HeuristicAgent(), MCTSAgent(rollouts_per_action=6, rollout_depth=3, seed=b),
        charizard_pidgeot_deck(), gardevoir_ex_deck(),
        n_matches=MATCHES_PER_BATCH,
    )
    heuristic_rates.append(r["win_rate_a"] * 100)
    mcts_rates.append(r["win_rate_b"] * 100)

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(range(1, N_BATCHES + 1), heuristic_rates, marker="o", color="#EE6B2F", label="HeuristicAgent win rate")
ax.plot(range(1, N_BATCHES + 1), mcts_rates, marker="s", color="#3B6FE0", label="MCTSAgent win rate")
ax.axhline(sum(heuristic_rates) / N_BATCHES, color="#EE6B2F", linestyle="--", alpha=0.4)
ax.axhline(sum(mcts_rates) / N_BATCHES, color="#3B6FE0", linestyle="--", alpha=0.4)
ax.set_xlabel(f"Batch (n={MATCHES_PER_BATCH} matches each)")
ax.set_ylabel("Win rate (%)")
ax.set_title("Agent Win-Rate Stability Across Repeated Batches")
ax.set_ylim(0, 100)
ax.legend()
ax.grid(alpha=0.25)
fig.tight_layout()

out_path = os.path.join(os.path.dirname(__file__), "..", "assets", "stability_chart.png")
fig.savefig(out_path, dpi=160)
print(f"Saved {out_path}")
print("Heuristic mean/stdev:", sum(heuristic_rates)/N_BATCHES,
      (sum((x-sum(heuristic_rates)/N_BATCHES)**2 for x in heuristic_rates)/N_BATCHES)**0.5)
