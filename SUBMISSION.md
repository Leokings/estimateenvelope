Project name: EstimateEnvelope

Category: Intelligent Contracts

Batch: A

One-line description: Coherence-gated robust estimate envelope.

What it does: Consensus checks whether each numeric range is supported by its rationale; deterministic order statistics seal a median envelope after quorum.

Why GenLayer: GenLayer consensus performs the bounded semantic step, then deterministic contract code executes and stores the mechanism-specific result.

Reusable: Yes. One deployment supports many independently keyed records and callers; the live fixture is only an example.

Repository: https://github.com/Leokings/estimateenvelope (private; reviewers require read access).

Contract source: contracts/estimate_envelope.py

Source SHA-256: 5820e5584cd2711fefaa1f5193d4049fc2fcf0539b1ea535a4a88ff254b16f09

StudioNet contract: https://explorer-studio.genlayer.com/address/0xEDBd4ad70eaA34a33e8d5bC39f4f3397DF1A4712

Deployment transaction: https://explorer-studio.genlayer.com/tx/0xf94759b7dde74bb5ea32cf0d1184c2ad7776eb9abe597895b9c971e8ebee071b

Intelligent transaction: https://explorer-studio.genlayer.com/tx/0x20ca55f8c973b37dccc3472d21b89b9f7737368221cfa9ba0e3e8ac3c92aff7f

Verification: GenVM lint PASS; strict typecheck PASS; 4 direct tests PASS; five-validator GLSim PASS; finalized StudioNet intelligent write and latest-final readback PASS; exact deployed-source and schema verification PASS.

Originality: Compared with 161 workspace contract sources. Nearest pre-existing structural score is 0.20854; mechanism and source hash are distinct.

Data boundary: Caller-supplied public data only. No external source fetching, funds, identity attestation, legal effect, or private-data guarantee.

Plain-text portal fields: SUBMISSION.txt. Notes / Description is within the 1,000-character form limit.
