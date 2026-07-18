import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from src.agent import HeuristicAgent
from decklists.sample_decks import charizard_pidgeot_deck, gardevoir_ex_deck, lost_zone_box_deck
from src.simulator import run_tournament

decks = {
    "Charizard/Pidgeot": charizard_pidgeot_deck,
    "Gardevoir ex": gardevoir_ex_deck,
    "Lost Zone Box": lost_zone_box_deck,
}
names = list(decks.keys())
matrix = np.zeros((len(names), len(names)))

for i, a in enumerate(names):
    for j, b in enumerate(names):
        if i == j:
            matrix[i][j] = 50.0
            continue
        r = run_tournament(HeuristicAgent(), HeuristicAgent(), decks[a](), decks[b](), n_matches=150)
        matrix[i][j] = r["win_rate_a"] * 100

fig, ax = plt.subplots(figsize=(6.5, 5.5))
im = ax.imshow(matrix, cmap="RdYlBu_r", vmin=0, vmax=100)
ax.set_xticks(range(len(names))); ax.set_xticklabels(names, rotation=20, ha="right")
ax.set_yticks(range(len(names))); ax.set_yticklabels(names)
ax.set_xlabel("Opponent deck")
ax.set_ylabel("Piloted deck (row) win rate vs column")
for i in range(len(names)):
    for j in range(len(names)):
        ax.text(j, i, f"{matrix[i][j]:.0f}%", ha="center", va="center", fontsize=11,
                color="white" if abs(matrix[i][j]-50) > 25 else "black")
ax.set_title("Heuristic Agent: Win Rate Across Deck Matchups")
fig.colorbar(im, ax=ax, label="Row win rate (%)")
fig.tight_layout()

out_path = os.path.join(os.path.dirname(__file__), "..", "assets", "matchup_matrix.png")
fig.savefig(out_path, dpi=160)
print("Saved", out_path)
