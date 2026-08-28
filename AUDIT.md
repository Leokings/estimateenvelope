# Final audit

Reviewed: 2026-08-25

Scope: `contracts/estimate_envelope.py` at SHA-256 `5820e5584cd2711fefaa1f5193d4049fc2fcf0539b1ea535a4a88ff254b16f09`, its
tests and review documents, and the exact StudioNet deployment recorded in
`deployments/studionet.json`.

## Results

| Gate | Result |
| --- | --- |
| GenVM lint and semantic validation | PASS |
| Strict Pyright typecheck | PASS, zero diagnostics |
| Direct invariant tests | PASS, 4 tests |
| Independent GLSim validators | PASS, exactly 5 validators |
| StudioNet deployment | PASS, FINALIZED |
| Real intelligent write | PASS, AGREE or MAJORITY_AGREE |
| Latest-final state readback | PASS |
| Deployed source byte equality | PASS |
| Deployed schema required-method read | PASS |
| Dependency and GenVM runner pins | PASS |
| Prompt-injection boundary and JSON normalization | PASS |
| External wallet isolation | PASS, 5 unique roles for this repository |
| Cross-repository wallet reuse | NONE across 100 roles |
| Private key or mnemonic in repository | NONE |
| Workspace-wide originality scan | PASS, 161 contract sources scanned |
| GitHub destination (2026-08-28 publication update) | Private repository: Leokings/estimateenvelope |

StudioNet contract: 0xEDBd4ad70eaA34a33e8d5bC39f4f3397DF1A4712

Deployment transaction: 0xf94759b7dde74bb5ea32cf0d1184c2ad7776eb9abe597895b9c971e8ebee071b

Intelligent transaction: 0x20ca55f8c973b37dccc3472d21b89b9f7737368221cfa9ba0e3e8ac3c92aff7f

Observed live state: `{"accepted_count":0,"state":"COLLECTING"}`

## Consensus review

Validators reproduce the coherence decision that controls acceptance; the explanatory quality band may differ without changing the gate.

## Review conclusion

No known source, build, test, consensus, wallet, secret, dependency, provenance,
or repository-hygiene blocker remains. Human program review can still apply its
own policy judgment; this audit does not promise acceptance.

Publication note: private GitHub evidence requires reviewer access. The original
StudioNet source and wallets are unchanged. CI uses the server's GET /health route
for readiness; /api is a POST-only JSON-RPC route. No live wallet keys are used by CI.
