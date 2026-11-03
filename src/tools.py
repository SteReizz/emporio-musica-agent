from rapidfuzz import process


class ProductTool:

    def __init__(self, products):

        self.products = products

    def find(self, product_name):

        names = self.products["name"].tolist()

        match = process.extractOne(
            product_name,
            names
        )

        if not match:
            return None

        row = self.products[
            self.products["name"] == match[0]
        ].iloc[0]

        return row.to_dict()

    def get_alternatives(
        self,
        category_id,
        current_product_id
    ):

        alternatives = self.products[
            (
                self.products["category_id"]
                == category_id
            )
            &
            (
                self.products["product_id"]
                != current_product_id
            )
            &
            (
                self.products["stock_quantity"]
                > 0
            )
        ]

        return (
            alternatives
            .head(3)
            .to_dict("records")
        )


class OrderTool:

    def __init__(self, orders):

        self.orders = orders

    def find(self, order_id):

        order = self.orders[
            self.orders["order_id"] == order_id
        ]

        if order.empty:
            return None

        return order.iloc[0].to_dict()

class PromotionTool:

    def __init__(
        self,
        promotions,
        products
    ):

        self.promotions = promotions
        self.products = products

    def get_active_promotions(self):

        promotions = self.promotions[
            self.promotions["is_active"] == 1
        ]

        results = []

        for _, promo in promotions.iterrows():

            product = self.products[
                self.products["product_id"]
                == promo["product_id"]
            ]

            if product.empty:
                continue

            product = product.iloc[0]

            original_price = (
                float(
                    product[
                        "price_brl"
                    ]
                )
            )

            discount = float(
                promo[
                    "discount_percent"
                ]
            )

            discounted_price = (
                original_price
                * (1 - discount / 100)
            )

            results.append(
                {
                    "name": product["name"],
                    "original_price": original_price,
                    "discount": discount,
                    "discounted_price": round(
                        discounted_price,
                        2
                    )
                }
            )

        return results