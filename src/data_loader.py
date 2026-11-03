import pandas as pd


class DataLoader:

    def __init__(self):

        self.products = pd.read_csv(
            "data/products.csv"
        )

        self.orders = pd.read_csv(
            "data/orders.csv"
        )

        self.promotions = pd.read_csv(
            "data/promotions.csv"
        )