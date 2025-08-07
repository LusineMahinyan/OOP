from typing import List

import pytest

from src.moduls import Category, Product


@pytest.fixture
def sample_products() -> List[Product]:
    """Возвращает несколько тестовых продуктов"""
    return [
        Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5),
        Product("Iphone 15", "512GB, Gray space", 210000.0, 8),
        Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14),
    ]


def test_product_initialization() -> None:
    """Проверка корректности инициализации Product"""
    product = Product("Test Product", "Описание товара", 999.99, 3)
    assert product.name == "Test Product"
    assert product.description == "Описание товара"
    assert product.price == 999.99
    assert product.quantity == 3


def test_category_initialization(sample_products: List[Product]) -> None:
    """Проверка корректности инициализации Category"""
    category = Category("Смартфоны", "Описание категории", sample_products)
    assert category.name == "Смартфоны"
    assert category.description == "Описание категории"
    assert category.products == sample_products


def test_category_and_product_count(sample_products: List[Product]) -> None:
    """Проверка подсчёта категорий и товаров"""
    # Сбрасываем счётчики перед тестом
    Category.category_count = 0
    Category.product_count = 0

    category1 = Category("Смартфоны", "Описание", sample_products)
    category2 = Category("Телевизоры", "Описание", [Product("TV", "Описание", 50000.0, 2)])

    assert category1.name == "Смартфоны"
    assert category2.name == "Телевизоры"

    assert Category.category_count == 2
    assert Category.product_count == len(sample_products) + 1
