# Design

## Mechanism

EstimateEnvelope separates the semantic and deterministic work. Validators decide only whether a rationale supports its submitted low, midpoint, and high under the stored question, unit, and policy. The contract normalizes that answer to exact JSON `{"coherent": bool}`.

The deterministic layer authorizes a precommitted panel, accepts one submission per wallet, stores rejected and accepted submissions, enforces full-panel completion and quorum, and computes a component-wise lower median across accepted ranges.

## State machine

`COLLECTING` → `SEALED`.

Only named estimators may submit. Every panel member must submit before the owner can seal. This keeps the membership fixed and prevents an owner from choosing a favorable stopping point. A rejected rationale consumes that wallet's one response and cannot be edited; clients should preview and review public inputs carefully.

## Deterministic envelope

Accepted lows, midpoints, and highs are sorted separately. For each list, index `(n - 1) // 2` is stored. This is the ordinary median for odd `n` and the lower median for even `n`. Because every accepted range satisfies `low <= midpoint <= high`, the resulting component-wise quantiles remain ordered.

## Off-chain responsibilities

Real-world identity, expertise, panel independence, source collection, private drafts, notifications, statistical interpretation, and actions based on the envelope remain off-chain.
