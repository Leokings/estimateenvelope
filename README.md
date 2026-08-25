# EstimateEnvelope

Coherence-gated robust estimate envelope.

Batch: A

## Why it is GenLayer-native

Consensus checks whether each numeric range is supported by its rationale; deterministic order statistics seal a median envelope after quorum.

The LLM handles only the bounded semantic step. Deterministic contract code owns
the reusable algorithm, state transitions, access control, tie-breaking, and
views. One deployment supports many caller-keyed records; it is not tied to the
StudioNet fixture or one organization.

## Public interface

Write methods: `open_estimate`, `submit_range`, `seal_envelope`

View methods: `get_estimate`, `get_submission`, `accepted_total`

## Verification

```text
pip install -r requirements.txt
genvm-lint check contracts/estimate_envelope.py
genvm-lint typecheck contracts/estimate_envelope.py --strict
pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5
gltest tests/integration -q --network localnet
```

The live smoke test is opt-in and requires a repository-specific wallet bundle
outside the repository. It waits for finalized receipts, reads `LATEST_FINAL`,
retrieves deployed source and schema from StudioNet, and fails unless the source
bytes exactly match this repository.

StudioNet contract: https://explorer-studio.genlayer.com/address/0xEDBd4ad70eaA34a33e8d5bC39f4f3397DF1A4712

See `AUDIT.md`, `ORIGINALITY.md`, `SOURCE_POLICY.md`, `SECURITY.md`,
`SUBMISSION.md`, and `deployments/studionet.json` for the final evidence.

## Boundary

The contract moves no funds and does not establish identity, ownership,
professional authority, source authenticity, physical truth, or legal effect.
All caller inputs and calldata are public. Off-chain clients own authentication,
privacy, source curation, indexing, and the decision to rely on a result.
