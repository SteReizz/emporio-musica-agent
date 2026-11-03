from pypdf import PdfReader
import re


class PolicyRAG:

    def __init__(self):

        pdf = PdfReader(
            "data/politicas_da_loja.pdf"
        )

        pages = []

        for page in pdf.pages:

            text = page.extract_text()

            if text:

                text = self.clean_text(
                    text
                )

                pages.append(
                    text
                )

        self.text = "\n\n".join(
            pages
        )

    def clean_text(self, text):

        text = text.replace(
            "\xa0",
            " "
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        text = re.sub(
            r" +",
            " ",
            text
        )

        return text.strip()
    
    def search(self, question):

        question = question.lower()

        if any(
            word in question
            for word in [
                "devolver",
                "devolução",
                "reembolso",
                "arrependimento"
            ]
        ):

            return """
    Sim!

    Compras online podem ser devolvidas em até 7 dias corridos após o recebimento.

    Condições:
    - embalagem original
    - sem sinais de uso
    - todos os acessórios e manuais

    O frete da devolução é pago pela loja.

    O reembolso ocorre em até 10 dias úteis na mesma forma de pagamento.
    """

        elif any(
            word in question
            for word in [
                "troca",
                "trocar"
            ]
        ):

            return """
    Trocas por preferência são permitidas em até 7 dias.

    O produto deve estar em perfeito estado e na embalagem original.

    Diferenças de valor poderão ser cobradas ou reembolsadas.
    """

        elif "garantia" in question:

            return """
    Todos os produtos possuem garantia legal de 90 dias contra defeitos de fabricação.

    Além disso, muitos fabricantes oferecem garantia adicional de 6 meses a 2 anos.
    """

        elif any(
            word in question
            for word in [
                "frete",
                "entrega"
            ]
        ):

            return """
    Região Metropolitana de Campo Grande:

    • Frete grátis acima de R$ 500
    • Pedidos abaixo de R$ 500: taxa de R$ 35
    • Prazo: 1 a 3 dias úteis

    Outras cidades:
    • PAC: 5 a 12 dias úteis
    • SEDEX: 2 a 5 dias úteis
    • Jadlog: 3 a 8 dias úteis
    """

        elif any(
            word in question
            for word in [
                "pix",
                "boleto",
                "cartão",
                "pagamento",
                "parcelamento"
            ]
        ):

            return """
    Formas de pagamento:

    • PIX (5% de desconto)
    • Cartão de débito
    • Cartão de crédito em até 12x sem juros
    • Boleto bancário
    """

        return (
            "Não encontrei informações "
            "sobre esse assunto."
        )