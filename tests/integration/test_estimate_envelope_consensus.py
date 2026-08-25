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
    owner, estimator = create_accounts(2)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "estimate_envelope.py")
    receipt = factory.deploy_contract_tx(args=[], account=owner, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(receipt)
    contract = factory.build_contract(extract_contract_address(receipt), account=owner)
    estimate_id = f"{str(owner.address).lower()}:BRIDGE-HOURS"
    _ok(contract.open_estimate(args=["bridge-hours", "How many labor hours will the public bridge inspection require?", "labor hours", 10, 100, 1, "Accept only rationales connecting scope, uncertainty, and all three numeric points." ]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {"Judge whether a public numeric estimate range": json.dumps({"coherent": True, "rationale_quality": 3})}})
    context = {"validators": [v.to_dict() for v in validators], "genvm_datetime": "2026-08-25T12:00:00Z"}
    as_estimator = factory.build_contract(contract.address, account=estimator)
    _ok(as_estimator.submit_range(args=[estimate_id, 20, 40, 70, "Four spans and bounded access assumptions justify the three stated points."]).transact(transaction_context=context, wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(contract.seal_envelope(args=[estimate_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert contract.get_estimate(args=[estimate_id]).call()["envelope"] == [20, 40, 70]
