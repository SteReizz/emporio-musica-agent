from src.data_loader import DataLoader
from src.tools import ProductTool


db = DataLoader()
tool = ProductTool(
    db.products
)


def test_find_product():

    product = tool.find(
        "Takamine GD20"
    )

    assert (
        "Takamine GD20"
        in product["name"]
    )


def test_product_exists():

    product = tool.find(
        "Yamaha C40"
    )

    assert product is not None