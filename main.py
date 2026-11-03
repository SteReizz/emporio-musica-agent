import re

from src.data_loader import DataLoader
from src.tools import (
    ProductTool,
    OrderTool,
    PromotionTool
)
from src.rag import PolicyRAG


# =========================
# INICIALIZAÇÃO
# =========================

db = DataLoader()

product_tool = ProductTool(
    db.products
)

order_tool = OrderTool(
    db.orders
)

promotion_tool = PromotionTool(
    db.promotions,
    db.products
)

policy_rag = PolicyRAG()


print(
    "\nAssistente Empório da Música"
)

print(
    "Bem-vindo(a)!Digite sua pergunta ou 'sair' para encerrar."
)


# =========================
# LOOP PRINCIPAL
# =========================

while True:

    question = input(
        "\nCliente: "
    )

    if question.lower() == "sair":
        print(
            "\nAssistente:"
        )

        print(
            "Obrigado pelo contato. Até logo!"
        )

        break

    text = question.lower()

    # =========================
    # ACESSÓRIOS NÃO VENDIDOS
    # =========================

    accessories = [
        "corda",
        "cordas",
        "cabo",
        "cabos",
        "palheta",
        "palhetas",
        "pedal",
        "pedais",
        "case",
        "cases",
        "amplificador",
        "amplificadores"
    ]

    if any(
        item in text
        for item in accessories
    ):

        print(
            """
Assistente:

A Empório da Música trabalha exclusivamente com instrumentos musicais.

No momento não comercializamos:

- cordas
- cabos
- palhetas
- cases
- pedais
- amplificadores
"""
        )

        continue

    # =========================
    # PROMOÇÕES
    # =========================

    if (
        "promoção" in text
        or "promoções" in text
        or "desconto" in text
    ):

        promotions = (
            promotion_tool
            .get_active_promotions()
        )

        print(
            "\nAssistente:"
        )

        print(
            "\nPromoções ativas:\n"
        )

        for item in promotions:

            print(
                f"""
Produto: {item['name']}
Preço original: R$ {item['original_price']}
Desconto: {item['discount']}%
Preço promocional: R$ {item['discounted_price']}
"""
            )

        continue

    # =========================
    # PEDIDOS
    # =========================

    if "pedido" in text:

        numbers = re.findall(
            r"\d+",
            text
        )

        print(
            "\nAssistente:"
        )

        if not numbers:

            print(
                "Informe o número do pedido."
            )

            continue

        order_id = int(
            numbers[0]
        )

        order = order_tool.find(
            order_id
        )

        if order:

            status = str(
                order["status"]
            ).lower()

            if status == "shipped":

                status_msg = (
                    "Seu pedido já foi enviado e está em transporte."
                )

            elif status == "delivered":

                status_msg = (
                    "Seu pedido já foi entregue."
                )

            elif status == "confirmed":

                status_msg = (
                    "Seu pedido foi confirmado e está sendo preparado para envio."
                )

            elif status == "pending":

                status_msg = (
                    "Seu pedido ainda aguarda processamento."
                )

            elif status == "cancelled":

                status_msg = (
                    "Seu pedido foi cancelado."
                )

            else:

                status_msg = status

            print(
                f"""
Pedido: {order['order_id']}

Status:
{status_msg}

Data do pedido:
{order['order_date']}

Valor:
R$ {order['total_brl']}

Pagamento:
{order['payment_method']}

Código de rastreamento:
{order['tracking_code']}

Previsão de entrega:
{order['estimated_delivery']}
"""
            )

        else:

            print(
                "Pedido não encontrado."
            )

        continue

    # =========================
    # POLÍTICAS
    # =========================

    policy_keywords = [
        "troca",
        "trocar",
        "devolução",
        "devolver",
        "garantia",
        "frete",
        "entrega",
        "rastreamento",
        "pix",
        "boleto",
        "cartão",
        "pagamento",
        "parcelamento",
        "reembolso"
    ]

    if any(
        keyword in text
        for keyword in policy_keywords
    ):

        answer = policy_rag.search(
            question
        )

        print(
            "\nAssistente:"
        )

        print(answer)

        continue

    # =========================
    # PRODUTOS
    # =========================

    product = product_tool.find(
        question
    )

    if product:

        status = product[
            "status"
        ]

        if status == "active":

            status_text = (
                "Disponível"
            )

        elif status == "discontinued":

            status_text = (
                "Descontinuado"
            )

        elif status == "coming_soon":

            status_text = (
                "Em breve"
            )

        else:

            status_text = status

        print(
            "\nAssistente:"
        )

        print(
            f"""
Produto: {product['name']}
Preço: R$ {product['price_brl']}
Estoque: {product['stock_quantity']}
Status: {status_text}
"""
        )

        # Produto descontinuado

        if (
            product["status"]
            == "discontinued"
        ):

            print(
                "\nEste produto foi descontinuado."
            )

            alternatives = (
                product_tool
                .get_alternatives(
                    product["category_id"],
                    product["product_id"]
                )
            )

            print(
                "\nModelos semelhantes disponíveis:"
            )

            for item in alternatives:

                print(
                    f"- {item['name']} "
                    f"(R$ {item['price_brl']})"
                )

        # Produto sem estoque

        elif (
            product["stock_quantity"]
            == 0
        ):

            print(
                "\nProduto temporariamente sem estoque."
            )

            alternatives = (
                product_tool
                .get_alternatives(
                    product["category_id"],
                    product["product_id"]
                )
            )

            print(
                "\nAlternativas disponíveis:"
            )

            for item in alternatives:

                print(
                    f"- {item['name']} "
                    f"(R$ {item['price_brl']})"
                )

        # Produto em breve

        elif (
            product["status"]
            == "coming_soon"
        ):

            print(
                "\nEste produto ainda não está disponível para venda."
            )

    else:

        print(
            "\nAssistente:"
        )

        print(
            "Não encontrei informações sobre isso."
        )