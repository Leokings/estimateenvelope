import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def test_five_validator_envelope_flow():
    owner, estimator_a, estimator_b = create_accounts(3)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "estimate_envelope.py")
    receipt = factory.deploy_contract_tx(args=[], account=owner, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(receipt)
    contract = factory.build_contract(extract_contract_address(receipt), account=owner)
    estimate_id = f"{str(owner.address).lower()}:BRIDGE-HOURS"
    panel = json.dumps([str(estimator_a.address), str(estimator_b.address)])
    _ok(contract.open_estimate(args=["bridge-hours", "How many labor hours will the public bridge inspection require?", "labor hours", 10, 100, panel, 2, "Accept only rationales connecting scope, uncertainty, and all three numeric points." ]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    validator_factory = get_validator_factory()
    validators_a = validator_factory.batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {"Judge whether a public numeric estimate range": json.dumps({"coherent": True})}})
    validators_b = validator_factory.batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {"Judge whether a public numeric estimate range": json.dumps({"coherent": True})}})
    context_a = {"validators": [v.to_dict() for v in validators_a], "genvm_datetime": "2026-09-28T12:00:00Z"}
    context_b = {"validators": [v.to_dict() for v in validators_b], "genvm_datetime": "2026-09-28T12:01:00Z"}
    as_estimator_a = factory.build_contract(contract.address, account=estimator_a)
    as_estimator_b = factory.build_contract(contract.address, account=estimator_b)
    _ok(as_estimator_a.submit_range(args=[estimate_id, 20, 40, 70, "Four spans and bounded access assumptions justify the three stated points."]).transact(transaction_context=context_a, wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(as_estimator_b.submit_range(args=[estimate_id, 30, 50, 80, "Crew-hour assumptions cover inspection access, normal work, and an adverse-access upper case."]).transact(transaction_context=context_b, wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(contract.seal_envelope(args=[estimate_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    state = contract.get_estimate(args=[estimate_id]).call()
    assert state["schema"] == "estimateenvelope/estimate/v2"
    assert state["state"] == "SEALED"
    assert state["envelope"] == [20, 40, 70]
