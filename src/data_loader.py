import json
from pathlib import Path
from typing import List

from src.moduls import Category, Product


def load_categories_from_json(filepath: str) -> List[Category]:
    base_dir = Path(__file__).resolve().parent.parent  # корень проекта (на 2 уровня вверх от data_loader.py)
    file_path = base_dir / filepath

    with open(file_path, encoding="utf-8") as file:
        data = json.load(file)

    categories = []
    for category_data in data:
        products = [
            Product(
                name=prod["name"],
                description=prod["description"],
                price=prod["price"],
                quantity=prod["quantity"],
            )
            for prod in category_data.get("products", [])
        ]
        category = Category(
            name=category_data["name"],
            description=category_data["description"],
            products=products,
        )
        categories.append(category)
    return categories
