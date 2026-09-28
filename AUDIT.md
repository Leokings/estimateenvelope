# Security audit

Reviewed: 2026-09-28

Scope: `contracts/estimate_envelope.py` at SHA-256 `c59dbc01cb2cde31826ab5cc564feb41e60312de5ed06295f927abf2e78bf614`, direct and integration tests, review documents, and the exact StudioNet deployment in `deployments/studionet.json`.

## Findings resolved

| Severity | Finding | Resolution |
| --- | --- | --- |
| High | Any wallet could consume one of the 15 submission slots, enabling denial of service and unapproved influence. | `open_estimate` now commits an explicit 2–15 wallet panel; only those distinct, nonzero, non-owner addresses may submit. |
| High | The owner could seal after quorum but before all intended participants answered, enabling timing and subset cherry-picking. | Sealing now requires `submission_count == panel_size`; rejected answers remain visible but cannot be silently omitted. |
| Medium | Question, unit, policy, and rationale were not all placed inside explicit untrusted-data boundaries. | Every caller-controlled prompt field now has a named start/end delimiter and an instruction-injection warning. |
| Medium | Validators agreed only on `coherent` while an unverified `rationale_quality` value was stored. | Model output is now exactly `{"coherent": bool}`; no unverified model field enters storage. |
| Evidence | The old StudioNet record stopped at `COLLECTING` with zero accepted submissions. | A fresh schema-v2 deployment completed two independent intelligent submissions and reached `SEALED`. |
| Coverage | The original suite had four tests and missed panel authorization, early seal, exact model shape, and address validation. | Direct coverage increased to 16 tests and the five-validator flow was rerun. |

## Verification results

| Gate | Result |
| --- | --- |
| GenVM lint and semantic validation | PASS |
| Strict typecheck | PASS, zero diagnostics |
| Direct invariant and negative-path tests | PASS, 16 tests |
| Independent local validators | PASS, exactly 5 validators |
| StudioNet owner plus two-estimator flow | PASS |
| StudioNet transaction finality | PASS, every recorded transaction `FINALIZED` / `MAJORITY_AGREE` |
| Minimum agreeing StudioNet votes | PASS, 3 of 5; some receipts were 5 of 5 |
| Latest-final `SEALED` readback | PASS |
| Deployed source byte equality | PASS |
| Deployed schema method verification | PASS |
| Private key or mnemonic in repository | NONE |

StudioNet contract: `0x75a349Ee228dcDC3b186e8e26A78fd8ed9590037`

Deployment transaction: `0xaf0a5ec33f6b7a32df21e46ce0035ef13ae5815ac164ac81482dcecf7ae5891f`

First intelligent transaction: `0xf892c1fcc0c8278f387efa73054707c547e430686c32f7f124da64178668d533`

Seal transaction: `0x0c25aa3ccdf92e03d77cf92ab27f4674f263fdc14d306111da2fc2c09c8d3abd`

Observed state: `{"schema":"estimateenvelope/estimate/v2","state":"SEALED","panel_size":2,"submission_count":2,"accepted_count":2,"quorum":2,"envelope":[20,40,70]}`

## Residual trust assumptions

- The owner chooses the panel, policy, bounds, and question. Multiple wallets do not prove independent people or qualified experts.
- A named estimator can withhold a submission and prevent sealing. No funds are locked, but that estimate may remain unfinished.
- Consensus checks whether a rationale supports its numbers; it does not prove the premise, data, expertise, or eventual outcome.
- Component-wise lower medians are deterministic and outlier-resistant, but they are a mechanism choice rather than statistical advice.
- StudioNet is a test network.

No known review-blocking source, authorization, state-machine, validation, consensus, test, or provenance defect remains. This is a focused engineering audit, not a formal proof or a promise of program acceptance.
