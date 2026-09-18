from logic_engine import KnowledgeBase


def test_forward_chaining():

    kb = KnowledgeBase()

    # ==================================================
    # DOMAIN RULES
    # ==================================================

    kb.tell_rule(
        ["TargetVisible", "HasDust"],
        "SafeToEngage"
    )

    kb.tell_rule(
        ["SafeToEngage", "BloodseekerMissing"],
        "Retreat"
    )


    # ==================================================
    # TEST CASE 1
    #
    # TargetVisible + HasDust
    #
    # Expected:
    # SafeToEngage
    #
    # NOT:
    # Retreat
    # ==================================================

    kb.clear_facts()

    kb.tell_fact(
        "TargetVisible"
    )

    kb.tell_fact(
        "HasDust"
    )

    kb.forward_chain()

    print("\nTest Case 1")
    print(
        "Facts:",
        kb.facts
    )

    assert (
        "SafeToEngage" in kb.facts
    ), (
        "Test 1 Failed: "
        "Should deduce SafeToEngage"
    )

    assert (
        "Retreat" not in kb.facts
    ), (
        "Test 1 Failed: "
        "Should NOT deduce Retreat"
    )


    # ==================================================
    # TEST CASE 2
    #
    # TargetVisible + HasDust +
    # BloodseekerMissing
    #
    # Expected:
    # SafeToEngage
    # Retreat
    # ==================================================

    kb.clear_facts()

    kb.tell_fact(
        "TargetVisible"
    )

    kb.tell_fact(
        "HasDust"
    )

    kb.tell_fact(
        "BloodseekerMissing"
    )

    kb.forward_chain()

    print("\nTest Case 2")
    print(
        "Facts:",
        kb.facts
    )

    assert (
        "SafeToEngage" in kb.facts
    ), (
        "Test 2 Failed: "
        "Should deduce SafeToEngage"
    )

    assert (
        "Retreat" in kb.facts
    ), (
        "Test 2 Failed: "
        "Should deduce Retreat"
    )


    print(
        "\n✅ All Logic Engine Test Cases Passed!"
    )


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    test_forward_chaining()