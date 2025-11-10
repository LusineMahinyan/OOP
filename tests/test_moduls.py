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

@pytest.fixture
def category(sample_products) -> Category:
    return Category("Смартфоны", "Категория для смартфонов", sample_products)


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
    products_str = category.products
    for product in sample_products:
        assert product.name in products_str


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

def test_add_product(category: Category) -> None:
    """Проверка метода add_product"""
    initial_count = Category.product_count
    new_product = Product("OnePlus 12", "256GB", 90000.0, 4)
    category.add_product(new_product)
    assert Category.product_count == initial_count + 1
    assert "OnePlus 12" in category.products


def test_product_price_setter_positive() -> None:
    """Проверка корректного изменения цены"""
    product = Product("Xiaomi", "128GB", 31000.0, 10)
    product.price = 35000.0
    assert product.price == 35000.0


def test_product_price_setter_negative(capsys) -> None:
    """Проверка на отрицательную цену"""
    product = Product("Xiaomi", "128GB", 31000.0, 10)
    product.price = -100
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 31000.0


def test_new_product_merges_existing() -> None:
    """Проверка слияния товаров при одинаковом имени"""
    existing = [Product("Iphone 15", "512GB", 200000.0, 5)]
    new_data = {"name": "Iphone 15", "description": "512GB", "price": 210000.0, "quantity": 3}
    product = Product.new_product(new_data, existing)
    assert product.quantity == 8
    assert product.price == 210000.0


def test_product_str() -> None:
    product = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    assert str(product) == "Iphone 15, 210000.0 руб. Остаток: 8 шт."


def test_product_add() -> None:
    p_1 = Product("Xiaomi", "Redmi", 30000.0, 10)
    p_2 = Product("Samsung", "Galaxy", 60000.0, 5)
    result = p_1 + p_2
    assert result == (30000.0 * 10) + (60000.0 * 5)


def test_category_str(sample_products) -> None:
    category = Category("Смартфоны", "Описание", sample_products)
    assert str(category) == "Смартфоны, количество продуктов: 27 шт."