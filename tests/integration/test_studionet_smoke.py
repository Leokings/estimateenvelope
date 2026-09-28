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
    accounts = wallet_accounts("estimateenvelope", 3)
    owner, estimator_a, estimator_b = accounts[:3]
    source = Path(__file__).resolve().parents[2] / "contracts" / "estimate_envelope.py"
    factory = get_contract_factory(contract_file_path=source)
    deployed = ok(factory.deploy_contract_tx(args=[], account=owner, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    admin = factory.build_contract(address, account=owner)
    contributor_a = factory.build_contract(address, account=estimator_a)
    contributor_b = factory.build_contract(address, account=estimator_b)
    estimate_id = f"{str(owner.address).lower()}:BRIDGE-HOURS"
    panel = json.dumps([str(estimator_a.address), str(estimator_b.address)])
    setup = ok(admin.open_estimate(args=["bridge-hours", "How many labor hours will the public bridge inspection require?", "labor hours", 10, 100, panel, 2, "Accept only rationales that connect scope, uncertainty, and all three numeric points." ]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = ok(contributor_a.submit_range(args=[estimate_id, 20, 40, 70, "Four spans, one inspection crew, and bounded access delays justify the low, midpoint, and high values." ]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    second = ok(contributor_b.submit_range(args=[estimate_id, 30, 50, 80, "Crew-hour assumptions cover inspection access, normal work, and an adverse-access upper case." ]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    sealed = ok(admin.seal_envelope(args=[estimate_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    state = admin.get_estimate(args=[estimate_id]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert state["schema"] == "estimateenvelope/estimate/v2"
    assert state["state"] == "SEALED"
    assert state["accepted_count"] == 2
    assert state["envelope"] == [20, 40, 70]
    proof = source_schema_proof(address, source, {"submit_range", "seal_envelope", "accepted_total"})
    emit_record("estimateenvelope", "A", address, deployed, [setup, second, sealed], intelligent, accounts, proof, {"state": state["state"], "accepted_count": state["accepted_count"], "envelope": state["envelope"]})
