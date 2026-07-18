# YouTube Script — "PTCG AI Battle Challenge: Building an Agent That Doesn't Get Lucky"

**Target length:** 4–6 minutes
**Thumbnail:** `assets/yt_thumbnail.png`
**Suggested title:** "I Built an AI That Plays Pokémon TCG — Then Tried to Prove It's Not Just Lucky"

---

### 0:00 – 0:15 | Hook
> "Most 'AI plays a card game' videos show you one really good game. This video is about the other 1,499 games — because if your strategy only works in the highlight reel, it's not a strategy, it's a coin flip."

*(Show thumbnail, then cut to the stability chart animating in.)*

### 0:15 – 0:45 | The problem with anecdotal wins
- Explain that Pokémon TCG has hidden information (opponent's hand, deck order) and a huge action space.
- A scripted "perfect line of play" example looks great on camera but breaks the moment the board state is different.
- State the actual goal: build something that performs the same way, on average, every single time you run it.

### 0:45 – 1:45 | Walkthrough of the engine
- Screen-record: `src/game_state.py` — show the `PokemonCard`, `InPlayPokemon`, `PlayerState` classes.
- Screen-record: `src/rules_engine.py` — show `legal_actions()` returning a list of legal moves for a given state.
- Explain in plain language: "Every turn, the engine asks: what are all the legal things I could do right now? Attach energy, retreat, attack, promote from bench. Then it hands that list to an agent."

### 1:45 – 2:45 | Two agents, one evaluation function
- Show `evaluate_state()` — explain the scoring: prize differential, HP, bench size.
- Show `HeuristicAgent`: "try every legal move, evaluate the result, take the best one."
- Show `MCTSAgent`: "same idea, but instead of one lookahead, it plays out a bunch of random rollouts and averages them — like running a mini simulation of 'what happens next' several times before committing."
- Key line: "Both agents agree on what a good board *looks like*. They just disagree on how hard to think before moving. That's what makes the comparison fair."

### 2:45 – 3:45 | The evidence: stability chart
- Cut to `assets/stability_chart.png` animating batch-by-batch.
- "I ran this exact matchup fifteen separate times, one hundred matches each — that's fifteen hundred games total, all with different random seeds. The heuristic agent's win rate stayed within about one percentage point of 74.5% every single time. That's the number I actually trust — not any single game."

### 3:45 – 4:30 | The evidence: matchup matrix
- Cut to `assets/matchup_matrix.png`.
- "Then I asked the harder question: does this only work against one specific opponent? So I ran the same agent piloting three totally different decks against each other — an aggressive attacker, a mid-range evolution deck, and a disruption deck. No matchup is a guaranteed win or a guaranteed loss, which is actually what you want to see — it means the agent is adapting to the board, not just executing a memorized combo."

### 4:30 – 5:00 | Deck concept
- Briefly show `decklists/sample_decks.py`.
- "Each deck represents a different real archetype philosophy — big single attacker, steady mid-range evolution line, and tempo/disruption. I picked these specifically because they force the same decision-making code to behave differently."

### 5:00 – 5:30 | What's next / call to action
- Roadmap teaser: proper MCTS with a persistent search tree, typed energy costs, full 60-card deck simulation, Trainer/Supporter cards.
- "Everything you just saw is reproducible — the charts regenerate automatically through a GitHub Actions workflow every time the code changes, so none of this is a one-off screenshot. Link to the repo and the full Kaggle writeup are in the description."

### 5:30 – 5:45 | Outro
> "If you're also building for this challenge, I'd genuinely like to compare notes — drop a comment with your win-rate stability numbers."

---

## On-screen text cues
- 0:00 — "PTCG AI BATTLE CHALLENGE"
- 0:45 — "legal_actions() → every rules-legal move"
- 1:45 — "Same evaluation function. Two search strategies."
- 2:45 — "74.5% ± 1.2pp across 15 batches"
- 3:45 — "No matchup is a guaranteed win or loss"

## Notes for editing
- No official Pokémon TCG card art, card text, or logos are used anywhere in the video — all on-screen graphics are the original charts/banner generated in this repo.
- Keep code screen-recordings brief (5–8 seconds per file) — the story is the *results*, not a line-by-line code read.
