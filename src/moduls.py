from abc import ABC, abstractmethod
from typing import Any, List, Optional


class BaseProduct(ABC):
    """Абстрактный класс для всех продуктов"""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def __add__(self, other: "BaseProduct") -> float:
        pass


class BaseEntity(ABC):
    """Абстрактный класс для объектов с названием и количеством (Category и Order)"""

    @abstractmethod
    def __init__(self, name: str, quantity: int):
        self.name = name
        self.quantity = quantity


class InitInfoMixin:
    """Миксин для вывода информации о созданном объекте"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        print(f"Создан объект класса {self.__class__.__name__} с параметрами {kwargs or args}")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {vars(self)}>"


class Product(InitInfoMixin, BaseProduct):
    """Класс для общего продукта"""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        super().__init__(name, description, price, quantity)

    def __str__(self) -> str:
        """Возвращает строковое представление продукта"""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "BaseProduct") -> float:
        """Возвращает сумму стоимости остатков двух продуктов"""
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов")

        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    """Класс, представляющий смартфон, как товар"""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс, представляющий газонную траву, как товар"""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category(BaseEntity):
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None) -> None:
        super().__init__(name, quantity=len(products) if products else 0)
        self.description = description
        self.__products = products if products else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в категорию, только если он экземпляр Product или его наследников"""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> List[Product]:
        """Геттер по критериям — возвращает список объектов Product"""
        return self.__products

    def products_str(self) -> str:
        """Возвращает строковое представление всех продуктов"""
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result.strip()

    def __str__(self) -> str:
        """Возвращает строковое представление категории"""
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."


class CategoryIterator:
    def __init__(self, category: Category) -> None:
        self._products = category.products
        self._index = 0

    def __iter__(self) -> "CategoryIterator":
        return self

    def __next__(self) -> "Product":
        if self._index < len(self._products):
            product = self._products[self._index]
            self._index += 1
            return product
        else:
            raise StopIteration


class Order(BaseEntity):
    """Класс заказа: один продукт, количество и итоговая стоимость"""

    def __init__(self, product: Product, quantity: int):
        if quantity > product.quantity:
            raise ValueError("Недостаточно товара на складе")
        super().__init__(product.name, quantity)
        self.product = product
        self.total_price = product.price * quantity

    def __str__(self) -> str:
        return f"Заказ: {self.product.name}, количество: {self.quantity}, итого: {self.total_price} руб."
