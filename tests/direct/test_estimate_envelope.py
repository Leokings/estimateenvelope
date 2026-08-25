def _open(contract, vm, owner, quorum=2):
    vm.sender = owner
    return contract.open_estimate(
        "bridge-hours",
        "How many labor hours will the public bridge inspection require?",
        "labor hours",
        10,
        100,
        quorum,
        "Accept only rationales that connect the stated scope, uncertainty, and all three numeric points.",
    )


def test_coherent_ranges_form_lower_median_envelope(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    estimate_id = _open(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_bob
    direct_vm.mock_llm(r".*Judge whether a public numeric estimate range.*", '{"coherent":true,"rationale_quality":3}')
    contract.submit_range(estimate_id, 20, 40, 70, "Scope totals four spans, with access uncertainty reflected in the low and high values.")
    direct_vm.sender = direct_charlie
    direct_vm.mock_llm(r".*Judge whether a public numeric estimate range.*", '{"coherent":true,"rationale_quality":2}')
    contract.submit_range(estimate_id, 30, 50, 80, "Crew-hour assumptions cover inspection access, normal work, and an adverse-access upper case.")
    direct_vm.sender = direct_alice
    contract.seal_envelope(estimate_id)
    assert contract.get_estimate(estimate_id)["envelope"] == [20, 40, 70]


def test_incoherent_range_is_recorded_but_not_counted(contract, direct_vm, direct_alice, direct_bob):
    estimate_id = _open(contract, direct_vm, direct_alice, 1)
    direct_vm.sender = direct_bob
    direct_vm.mock_llm(r".*Judge whether a public numeric estimate range.*", '{"coherent":false,"rationale_quality":0}')
    submission_id = contract.submit_range(estimate_id, 20, 40, 70, "This rationale is long enough but unrelated to how any numeric point was selected.")
    assert contract.get_submission(submission_id)["coherent"] is False
    assert contract.accepted_total(estimate_id) == 0


def test_wallet_cannot_submit_twice(contract, direct_vm, direct_alice, direct_bob):
    estimate_id = _open(contract, direct_vm, direct_alice, 1)
    direct_vm.sender = direct_bob
    direct_vm.mock_llm(r".*Judge whether a public numeric estimate range.*", '{"coherent":true,"rationale_quality":2}')
    contract.submit_range(estimate_id, 20, 40, 70, "The three points follow from bounded access assumptions and a four-span work estimate.")
    with direct_vm.expect_revert("wallet_already_submitted"):
        contract.submit_range(estimate_id, 25, 45, 75, "A second bounded range uses the same scope but revised access assumptions for testing.")


def test_range_order_is_enforced_before_consensus(contract, direct_vm, direct_alice, direct_bob):
    estimate_id = _open(contract, direct_vm, direct_alice, 1)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("range_out_of_order_or_bounds"):
        contract.submit_range(estimate_id, 60, 40, 70, "The rationale cannot rescue a deterministically malformed numeric interval.")
