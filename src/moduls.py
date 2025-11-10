from typing import Any, Dict, List, Optional


class Product:
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property  # type: ignore[no-redef]
    def price(self) -> float:
        """Геттер для цены"""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой на положительное значение"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        if new_price < self.__price:
            answer = input(f"Вы действительно хотите понизить цену с {self.__price} до {new_price}? (y/n): ").lower()
            if answer != "y":
                print("Действие отменено. Цена не изменена.")
                return

        self.__price = new_price

    @classmethod
    def new_product(cls, data: Dict[str, Any], existing_products: Optional[List["Product"]] = None) -> "Product":

        if existing_products is None:
            existing_products = []

        for product in existing_products:
            if product.name == data["name"]:
                product.quantity += data["quantity"]
                if data["price"] > product.price:
                    product.price = data["price"]
                return product

        new_product = cls(
            name=data["name"], description=data["description"], price=data["price"], quantity=data["quantity"]
        )
        return new_product

    def __str__(self) -> str:
        """Возвращает строковое представление продукта"""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Возвращает сумму стоимости остатков двух продуктов"""
        total = (self.price * self.quantity) + (other.price * other.quantity)
        return float(total)


class Category:
    category_count: int = 0
    product_count: int = 0

    name: str
    description: str
    __products: List[Product]

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None) -> None:
        self.name = name
        self.description = description
        self.__products = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в приватный список и увеличивает счетчик продуктов"""
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
        total_quantity = 0
        for product in self.__products:
            total_quantity += product.quantity
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
