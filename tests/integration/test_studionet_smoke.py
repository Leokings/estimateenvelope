import json
import os
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address

from tests.studionet_support import emit_record, ok, source_schema_proof, wallet_accounts


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(os.environ.get("RUN_STUDIONET") != "1", reason="opt-in live StudioNet test"),
]


def test_studionet_robust_estimate_envelope():
    accounts = wallet_accounts("estimateenvelope", 2)
    owner, estimator = accounts[:2]
    source = Path(__file__).resolve().parents[2] / "contracts" / "estimate_envelope.py"
    factory = get_contract_factory(contract_file_path=source)
    deployed = ok(factory.deploy_contract_tx(args=[], account=owner, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    admin = factory.build_contract(address, account=owner)
    contributor = factory.build_contract(address, account=estimator)
    estimate_id = f"{str(owner.address).lower()}:BRIDGE-HOURS"
    setup = ok(admin.open_estimate(args=["bridge-hours", "How many labor hours will the public bridge inspection require?", "labor hours", 10, 100, 1, "Accept only rationales that connect scope, uncertainty, and all three numeric points." ]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = ok(contributor.submit_range(args=[estimate_id, 20, 40, 70, "Four spans, one inspection crew, and bounded access delays justify the low, midpoint, and high values." ]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    state = admin.get_estimate(args=[estimate_id]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert state["schema"] == "estimateenvelope/estimate/v1" and state["accepted_count"] in (0, 1)
    proof = source_schema_proof(address, source, {"submit_range", "seal_envelope", "accepted_total"})
    emit_record("estimateenvelope", "A", address, deployed, [setup], intelligent, accounts, proof, {"state": state["state"], "accepted_count": state["accepted_count"]})
