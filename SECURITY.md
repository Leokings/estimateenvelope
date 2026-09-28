# Security

## Controls

- concrete GenVM runner and Python dependencies are pinned;
- the estimator panel contains 2–15 distinct, nonzero, non-owner addresses;
- only named estimators may use a slot, and each may submit once;
- sealing requires the full named panel and the configured quorum;
- keys, numbers, text lengths, JSON, and loops are bounded;
- each submitted range must satisfy stored bounds and `low <= midpoint <= high`;
- all caller-controlled prompt fields are explicitly delimited as untrusted data;
- model output has one exact boolean field, normalized before storage;
- a custom validator independently repeats the nondeterministic judgment;
- envelope calculation and tie behavior are deterministic;
- finalized live state, deployed source bytes, and schema methods are checked against StudioNet.

## Threat boundary

The contract prevents unauthorized slot use, duplicate submissions, owner-as-estimator membership, and early sealing. It cannot prove that separate wallets belong to separate people, that estimators are qualified, that rationales use true premises, or that an estimate will be accurate. The owner can choose a biased panel or policy; users must inspect both.

## Liveness

Any named estimator can withhold its one required response, leaving an estimate in `COLLECTING`. This fail-closed rule is intentional: replacing or silently omitting a named estimator would reintroduce subset cherry-picking. No funds are locked.

## Public-data warning

All questions, policies, rationales, ranges, panel addresses, and results are public. Do not submit secrets, personal data, private documents, or confidential forecasts.
