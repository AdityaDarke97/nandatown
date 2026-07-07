# packages/nest-core/tests/test_scenario.py
import pytest
from nest_core.validators import validate_empic_pubsub_billing_caps

def test_validate_empic_pubsub_billing_caps_omits_mode():
    """Test that validator catches billing cap violations even if mode is omitted."""
    events = [
        {
            "kind": "send",
            "msg": '{"type": "empic_audit", "event_type": "empic_stream_opened", "payment_ref": "stream-1", "rate_per_tick": 10, "max_total": 100}',
            "tick": 0
        },
        {
            "kind": "send",
            # The 'mode' field is intentionally omitted here to simulate the attack
            "msg": '{"type": "empic_audit", "event_type": "empic_escrow_released", "payment_ref": "stream-1", "amount": 50, "delivery_id": "d1"}',
            "tick": 1
        }
    ]
    
    results = validate_empic_pubsub_billing_caps(events)
    assert len(results) == 1
    # The validator must now FAIL because 50 > rate 10, regardless of the missing mode
    assert results[0].passed is False
    assert "release 50 > rate 10" in results[0].detail