from src.data_loader import DataLoader
from src.tools import OrderTool


db = DataLoader()

tool = OrderTool(
    db.orders
)


def test_order_exists():

    order = tool.find(8)

    assert (
        order["order_id"]
        == 8
    )


def test_order_tracking():

    order = tool.find(8)

    assert (
        len(
            order[
                "tracking_code"
            ]
        ) > 0
    )