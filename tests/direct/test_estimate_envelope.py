import json


QUESTION = "How many labor hours will the public bridge inspection require?"
UNIT = "labor hours"
POLICY = "Accept only rationales that connect the stated scope, uncertainty, and all three numeric points."
RATIONALE_A = "Scope totals four spans, with access uncertainty reflected in the low and high values."
RATIONALE_B = "Crew-hour assumptions cover inspection access, normal work, and an adverse-access upper case."


def _address(value) -> str:
    if isinstance(value, (bytes, bytearray)):
        return "0x" + bytes(value).hex()
    return str(value)


def _open(contract, vm, owner, estimators, quorum=2, key="bridge-hours"):
    vm.sender = owner
    return contract.open_estimate(
        key,
        QUESTION,
        UNIT,
        10,
        100,
        json.dumps([_address(estimator) for estimator in estimators]),
        quorum,
        POLICY,
    )


def _submit(contract, vm, estimator, estimate_id, values, coherent=True, rationale=RATIONALE_A):
    vm.sender = estimator
    vm.clear_mocks()
    vm.mock_llm(
        r".*Judge whether a public numeric estimate range.*",
        json.dumps({"coherent": coherent}),
    )
    return contract.submit_range(estimate_id, *values, rationale)


def test_complete_panel_forms_lower_median_envelope(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    estimate_id = _open(contract, direct_vm, direct_alice, [direct_bob, direct_charlie])
    _submit(contract, direct_vm, direct_bob, estimate_id, (20, 40, 70))
    _submit(contract, direct_vm, direct_charlie, estimate_id, (30, 50, 80), rationale=RATIONALE_B)
    direct_vm.sender = direct_alice
    contract.seal_envelope(estimate_id)
    state = contract.get_estimate(estimate_id)
    assert state["schema"] == "estimateenvelope/estimate/v2"
    assert state["state"] == "SEALED"
    assert state["envelope"] == [20, 40, 70]
    assert state["accepted_count"] == 2


def test_three_member_panel_uses_coordinate_medians(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie, direct_accounts
):
    third = direct_accounts[3]
    estimate_id = _open(contract, direct_vm, direct_alice, [direct_bob, direct_charlie, third], 2, "median")
    _submit(contract, direct_vm, direct_bob, estimate_id, (15, 35, 65))
    _submit(contract, direct_vm, direct_charlie, estimate_id, (30, 50, 80), rationale=RATIONALE_B)
    _submit(contract, direct_vm, third, estimate_id, (25, 45, 75), rationale=RATIONALE_A)
    direct_vm.sender = direct_alice
    contract.seal_envelope(estimate_id)
    assert contract.get_estimate(estimate_id)["envelope"] == [25, 45, 75]


def test_incoherent_range_is_recorded_but_does_not_satisfy_quorum(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    estimate_id = _open(contract, direct_vm, direct_alice, [direct_bob, direct_charlie])
    submission_id = _submit(
        contract,
        direct_vm,
        direct_bob,
        estimate_id,
        (20, 40, 70),
        False,
        "This rationale is long enough but unrelated to how any numeric point was selected.",
    )
    _submit(contract, direct_vm, direct_charlie, estimate_id, (30, 50, 80), rationale=RATIONALE_B)
    assert contract.get_submission(submission_id)["coherent"] is False
    assert contract.accepted_total(estimate_id) == 1
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("quorum_not_met"):
        contract.seal_envelope(estimate_id)


def test_outsider_cannot_consume_a_panel_slot(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie, direct_accounts
):
    estimate_id = _open(contract, direct_vm, direct_alice, [direct_bob, direct_charlie])
    direct_vm.sender = direct_accounts[3]
    with direct_vm.expect_revert("only_estimator"):
        contract.submit_range(estimate_id, 20, 40, 70, RATIONALE_A)
    assert contract.get_estimate(estimate_id)["submission_count"] == 0


def test_owner_cannot_submit_as_estimator(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    estimate_id = _open(contract, direct_vm, direct_alice, [direct_bob, direct_charlie])
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("only_estimator"):
        contract.submit_range(estimate_id, 20, 40, 70, RATIONALE_A)


def test_estimator_cannot_submit_twice(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    estimate_id = _open(contract, direct_vm, direct_alice, [direct_bob, direct_charlie])
    _submit(contract, direct_vm, direct_bob, estimate_id, (20, 40, 70))
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("wallet_already_submitted"):
        contract.submit_range(estimate_id, 25, 45, 75, RATIONALE_B)


def test_range_order_is_enforced_before_consensus(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    estimate_id = _open(contract, direct_vm, direct_alice, [direct_bob, direct_charlie])
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("range_out_of_order_or_bounds"):
        contract.submit_range(
            estimate_id,
            60,
            40,
            70,
            "The rationale cannot rescue a deterministically malformed numeric interval.",
        )


def test_owner_cannot_cherry_pick_before_full_panel_submits(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    estimate_id = _open(contract, direct_vm, direct_alice, [direct_bob, direct_charlie])
    _submit(contract, direct_vm, direct_bob, estimate_id, (20, 40, 70))
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("panel_incomplete"):
        contract.seal_envelope(estimate_id)


def test_only_owner_can_seal(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    estimate_id = _open(contract, direct_vm, direct_alice, [direct_bob, direct_charlie])
    _submit(contract, direct_vm, direct_bob, estimate_id, (20, 40, 70))
    _submit(contract, direct_vm, direct_charlie, estimate_id, (30, 50, 80), rationale=RATIONALE_B)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_owner"):
        contract.seal_envelope(estimate_id)


def test_model_output_must_have_one_exact_boolean_field(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    estimate_id = _open(contract, direct_vm, direct_alice, [direct_bob, direct_charlie])
    direct_vm.sender = direct_bob
    direct_vm.mock_llm(
        r".*Judge whether a public numeric estimate range.*",
        json.dumps({"coherent": True, "quality": 3}),
    )
    with direct_vm.expect_revert("[LLM_ERROR] wrong_gate_shape"):
        contract.submit_range(estimate_id, 20, 40, 70, RATIONALE_A)


def test_model_cannot_return_non_boolean_decision(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    estimate_id = _open(contract, direct_vm, direct_alice, [direct_bob, direct_charlie])
    direct_vm.sender = direct_bob
    direct_vm.mock_llm(r".*Judge whether a public numeric estimate range.*", json.dumps({"coherent": 1}))
    with direct_vm.expect_revert("[LLM_ERROR] invalid_gate_value"):
        contract.submit_range(estimate_id, 20, 40, 70, RATIONALE_A)


def test_panel_must_be_valid_distinct_nonzero_and_exclude_owner(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    direct_vm.sender = direct_alice
    args = ["panel", QUESTION, UNIT, 10, 100]
    with direct_vm.expect_revert("duplicate_estimator"):
        contract.open_estimate(*args, json.dumps([_address(direct_bob), _address(direct_bob)]), 2, POLICY)
    with direct_vm.expect_revert("invalid_estimator"):
        contract.open_estimate(*args, json.dumps([_address(direct_bob), "0x" + "0" * 40]), 2, POLICY)
    with direct_vm.expect_revert("owner_cannot_be_estimator"):
        contract.open_estimate(*args, json.dumps([_address(direct_bob), _address(direct_alice)]), 2, POLICY)
    with direct_vm.expect_revert("invalid_estimators"):
        contract.open_estimate(*args, json.dumps([_address(direct_bob)]), 2, POLICY)


def test_quorum_must_be_at_least_two_and_not_exceed_panel(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    direct_vm.sender = direct_alice
    panel = json.dumps([_address(direct_bob), _address(direct_charlie)])
    with direct_vm.expect_revert("invalid_quorum"):
        contract.open_estimate("low-quorum", QUESTION, UNIT, 10, 100, panel, 1, POLICY)
    with direct_vm.expect_revert("invalid_quorum"):
        contract.open_estimate("high-quorum", QUESTION, UNIT, 10, 100, panel, 3, POLICY)


def test_malformed_panel_json_is_rejected(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("invalid_estimators_json"):
        contract.open_estimate("bad-json", QUESTION, UNIT, 10, 100, "not-json", 2, POLICY)


def test_estimate_key_is_unique_for_owner(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    _open(contract, direct_vm, direct_alice, [direct_bob, direct_charlie], key="unique")
    with direct_vm.expect_revert("estimate_exists"):
        _open(contract, direct_vm, direct_alice, [direct_bob, direct_charlie], key="unique")


def test_sealed_estimate_rejects_further_submissions_and_second_seal(
    contract, direct_vm, direct_alice, direct_bob, direct_charlie
):
    estimate_id = _open(contract, direct_vm, direct_alice, [direct_bob, direct_charlie])
    _submit(contract, direct_vm, direct_bob, estimate_id, (20, 40, 70))
    _submit(contract, direct_vm, direct_charlie, estimate_id, (30, 50, 80), rationale=RATIONALE_B)
    direct_vm.sender = direct_alice
    contract.seal_envelope(estimate_id)
    with direct_vm.expect_revert("estimate_not_collecting"):
        contract.seal_envelope(estimate_id)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("estimate_not_collecting"):
        contract.submit_range(estimate_id, 20, 40, 70, RATIONALE_A)
