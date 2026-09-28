# EstimateEnvelope

EstimateEnvelope is a reusable GenLayer Intelligent Contract for collecting reasoned numeric ranges from a named panel and sealing a consensus-gated robust envelope.

## How it works

1. An owner calls `open_estimate` with a bounded question, unit, numeric limits, an explicit panel of 2–15 distinct estimator wallets, a quorum, and a public coherence policy.
2. Each named estimator may call `submit_range` once. GenLayer validators independently decide whether the rationale actually supports that submission's low, midpoint, and high values.
3. Every named panel member must respond before sealing. Incoherent submissions remain auditable but do not count toward quorum.
4. If the accepted count reaches quorum, the owner calls `seal_envelope`. Deterministic code takes the lower median of accepted lows, midpoints, and highs and stores the final envelope.

The panel allowlist prevents strangers from consuming submission slots. Requiring the full named panel before seal prevents the owner from timing the result around a preferred subset.

## Why it is GenLayer-native

Whether prose genuinely supports three numeric estimates is a semantic judgment. GenLayer's validators reproduce that bounded judgment, while ordinary deterministic contract code owns authorization, limits, state transitions, quorum, order statistics, and storage.

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
pytest tests/integration/test_estimate_envelope_consensus.py -q
```

Verified on 2026-09-28: lint PASS, strict typecheck PASS, 16 direct tests PASS, one five-validator integration flow PASS, and a complete three-wallet StudioNet flow PASS.

StudioNet contract: https://explorer-studio.genlayer.com/address/0x75a349Ee228dcDC3b186e8e26A78fd8ed9590037

The finalized live flow accepted two coherent panel submissions and sealed envelope `[20, 40, 70]`. The deployed source is byte-for-byte identical to `contracts/estimate_envelope.py`. See `deployments/studionet.json` for every transaction and the latest-final readback.

## Boundary

All questions, policies, rationales, ranges, wallet addresses, and results are public. Wallet separation does not prove real-world independence or expertise. The contract does not authenticate facts, fetch sources, move funds, or promise that an estimate is correct.
