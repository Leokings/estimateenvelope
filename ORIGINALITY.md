# Originality audit

The final source was compared against 161 GenLayer
contract sources in the workspace. All twenty new target contracts were excluded
from the pre-existing comparison pool.

Nearest pre-existing source: `rulebender\contracts\policy_amendment_chain.py`

Combined structural score: `0.20854`

Token score: `0.339956`

AST score: `0.110177`

Nearest contract in this new set: `condorcetagenda\contracts\condorcet_agenda.py` with combined
score `0.315692`. That score reflects shared safe GenLayer
boilerplate. The mechanisms differ materially:

- This repository: Consensus checks whether each numeric range is supported by its rationale; deterministic order statistics seal a median envelope after quorum.
- Other repository: Consensus compiles each narrative preference into a complete ranking; deterministic strongest-path comparison chooses the pairwise winner.

The two do not share the same semantic input, deterministic algorithm, storage
record, state lifecycle, or decision views. Exact source SHA-256 values are also
unique across all twenty repositories. The complete machine-readable reports are
`review-tools/twenty-originality-audit.json` and
`review-tools/twenty-pairwise-audit.json` at the workspace level.

Similarity scoring is a review aid, not a guarantee of a human review outcome.
