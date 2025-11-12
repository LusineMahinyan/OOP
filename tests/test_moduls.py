from typing import List

import pytest

from src.moduls import Category, Product, Smartphone, LawnGrass, BaseProduct


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
    products_str = category.products_str()
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
    initial_count = Category.product_count
    new_product = Product("OnePlus 12", "256GB", 90000.0, 4)
    category.add_product(new_product)
    assert Category.product_count == initial_count + 1
    assert "OnePlus 12" in category.products_str()


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


def test_smartphone_inherits_product() -> None:
    """Проверяет, что Smartphone наследуется от Product"""
    smartphone = Smartphone("Samsung", "Galaxy", 100000.0, 5, 95.5, "S23", 256, "Серый")
    assert isinstance(smartphone, Product)
    assert smartphone.model == "S23"
    assert smartphone.memory == 256
    assert smartphone.color == "Серый"


def test_lawngrass_inherits_product() -> None:
    """Проверяет, что LawnGrass наследуется от Product"""
    grass = LawnGrass("Газон", "Элитная трава", 500.0, 20, "Россия", "7 дней", "Зеленый")
    assert isinstance(grass, Product)
    assert grass.country == "Россия"
    assert grass.color == "Зеленый"


def test_add_different_class_products_raises_typeerror() -> None:
    """Попытка сложить продукты разных классов вызывает TypeError"""
    smartphone = Smartphone("Samsung", "Galaxy", 100000.0, 5, 95.5, "S23", 256, "Серый")
    grass = LawnGrass("Газон", "Элитная трава", 500.0, 20, "Россия", "7 дней", "Зеленый")

    with pytest.raises(TypeError):
        _ = smartphone + grass


def test_add_product_allows_only_product_instances() -> None:
    """Можно добавлять только объекты Product и его наследников"""
    smartphone = Smartphone("Samsung", "Galaxy", 100000.0, 5, 95.5, "S23", 256, "Серый")
    category = Category("Смартфоны", "Описание", [])

    category.add_product(smartphone)
    assert len(category.products) == 1

    with pytest.raises(TypeError):
        category.add_product("Не продукт")


def test_inheritance_from_baseproduct():
    p = Product("Test", "Desc", 100, 1)
    s = Smartphone("TestPhone", "Desc", 200, 2, 90, "X", 128, "Black")
    g = LawnGrass("Grass", "Desc", 50, 10, "RU", "5 дней", "Green")

    assert isinstance(p, BaseProduct)
    assert isinstance(s, BaseProduct)
    assert isinstance(g, BaseProduct)



def test_add_same_class_products():
    p1 = Product("A", "Desc", 100, 2)
    p2 = Product("B", "Desc", 200, 3)
    s1 = Smartphone("Phone1", "Desc", 200, 1, 90, "X", 128, "Black")
    s2 = Smartphone("Phone2", "Desc", 300, 2, 95, "Y", 256, "White")

    assert p1 + p2 == 100 * 2 + 200 * 3
    assert s1 + s2 == 200 * 1 + 300 * 2


def test_add_different_class_raises_typeerror():
    p = Product("A", "Desc", 100, 1)
    g = LawnGrass("Grass", "Desc", 50, 10, "RU", "5 дней", "Green")

    with pytest.raises(TypeError):
        _ = p + g


def test_category_add_product_typecheck():
    from src.moduls import Category
    cat = Category("TestCat", "Desc", [])
    p = Product("A", "Desc", 100, 1)

    cat.add_product(p)

    with pytest.raises(TypeError):
        cat.add_product("Не продукт")
