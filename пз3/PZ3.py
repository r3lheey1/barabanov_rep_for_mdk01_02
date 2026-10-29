# --- 1. Кастомные исключения ---
class AssetError(Exception): pass


class InvalidPriceError(AssetError): pass


class InvalidMonthsError(AssetError): pass


class AssetLimitExceededError(AssetError): pass


# --- 2. Базовый класс и наследники ---
class ITAsset:
    lifetime = 0  # Полиморфный атрибут (переопределяется)

    def __init__(self, inv_id, model, price, months=0):
        if price <= 0:
            raise InvalidPriceError(f"Цена {price} должна быть > 0")
        if months < 0:
            raise InvalidMonthsError(f"Месяцы {months} должны быть >= 0")
        self.inv_id = inv_id
        self.model = model
        self.price = price
        self.months = months

    def get_value(self):  # Полиморфный метод
        return self.price * max(0, 1 - self.months / self.lifetime)

    def __str__(self):
        return f"{self.__class__.__name__} {self.model} (Остаток: {self.get_value():.0f} р.)"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.inv_id})"

    def __eq__(self, other):
        return self.inv_id == other.inv_id

    def __lt__(self, other):
        return self.get_value() < other.get_value()

    def __add__(self, other):
        return self.get_value() + other.get_value()

    def __sub__(self, months):
        return self.__class__(self.inv_id, self.model, self.price, self.months + months)


class Laptop(ITAsset): lifetime = 36


class Monitor(ITAsset): lifetime = 60


class Smartphone(ITAsset): lifetime = 24


# --- 3. Класс-контейнер (Склад) ---
class AssetWarehouse:
    LIMIT = 150_000

    def __init__(self, employee_name):
        self.employee_name = employee_name
        self.items = []

    def add(self, asset):
        current_total = sum(a.get_value() for a in self.items)
        if current_total + asset.get_value() > self.LIMIT:
            raise AssetLimitExceededError(
                f"Превышен лимит! Текущая сумма: {current_total:.0f} р., "
                f"добавляем: {asset.get_value():.0f} р., лимит: {self.LIMIT} р."
            )
        self.items.append(asset)

    def __len__(self): return len(self.items)

    def __getitem__(self, i): return self.items[i]


# --- 4. Демонстрация работы (ЭТАП 3) ---
if __name__ == "__main__":
    print("=== 1. Создание объектов и __str__ ===")
    laptop = Laptop("INV-001", "Lenovo ThinkPad", 80000, 18)
    monitor = Monitor("INV-002", "Dell U2419H", 25000, 12)
    phone = Smartphone("INV-003", "iPhone 13", 40000, 6)
    print(laptop)
    print(monitor)
    print(phone)

    print("\n=== 2. __add__ и __sub__ ===")
    print(f"Общая стоимость ноутбука и монитора: {laptop + monitor:.0f} р.")
    laptop_spisano = laptop - 6
    print(f"Ноутбук после списания 6 мес.: {laptop_spisano}")

    print("\n=== 3. Контейнер (__len__ и __getitem__) ===")
    warehouse = AssetWarehouse("Иван Петров")
    warehouse.add(laptop)
    warehouse.add(monitor)
    warehouse.add(phone)
    print(f"На складе у {warehouse.employee_name}: {len(warehouse)} единицы техники.")
    print(f"Техника по индексу 0: {warehouse[0]}")

    print("\n=== 4. Сортировка (__lt__) ===")
    for asset in sorted(warehouse.items):
        print(f"  {asset}")

    print("\n=== 5. Полиморфизм в цикле ===")
    for asset in warehouse:
        print(f"  {type(asset).__name__}: остаточная стоимость {asset.get_value():.0f} р.")

    print("\n=== 6. Перехват исключений ===")
    try:
        bad_asset = Laptop("INV-ERR", "Bad Laptop", -5000)
    except InvalidPriceError as e:
        print(f"✗ Ошибка цены: {e}")

    try:
        _ = laptop - (-10)
    except InvalidMonthsError as e:
        print(f"✗ Ошибка месяцев: {e}")

    try:
        warehouse.add(Laptop("INV-004", "MacBook Pro", 200000, 0))
    except AssetLimitExceededError as e:
        print(f"✗ {e}")