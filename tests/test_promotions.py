from src.data_loader import DataLoader
from src.tools import PromotionTool


db = DataLoader()

tool = PromotionTool(
    db.promotions,
    db.products
)


def test_promotions_exist():

    promotions = (
        tool.get_active_promotions()
    )

    assert (
        len(promotions) > 0
    )