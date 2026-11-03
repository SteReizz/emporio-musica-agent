from src.rag import PolicyRAG


rag = PolicyRAG()


def test_return_policy():

    answer = rag.search(
        "Posso devolver um produto?"
    )

    assert (
        "7 dias"
        in answer
    )


def test_payment_policy():

    answer = rag.search(
        "formas de pagamento"
    )

    assert (
        "PIX"
        in answer
    )