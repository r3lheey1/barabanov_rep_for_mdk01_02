class BMI:
    def __init__(self, first=0.0, second=0.0):
        self.__first = first
        self.__second = second

    @property
    def first(self):
        return self.__first

    @first.setter
    def first(self, value):
        if value <= 0:
            raise ValueError("Вес должен быть положительным")
        self.__first = value

    @property
    def second(self):
        return self.__second

    @second.setter
    def second(self, value):
        if value <= 0:
            raise ValueError("Рост должен быть положительным")
        self.__second = value

    def read(self):
        try:
            self.first = float(input("Введите вес (кг): "))
            self.second = float(input("Введите рост (см): ")) / 100
        except ValueError:
            print("Ошибка: введите корректное число!")

    def display(self):
        print(f"Вес: {self.first} кг")
        print(f"Рост: {self.second} м")

    def calculate_bmi(self):
        if self.second == 0:
            raise ValueError("Рост не может быть равен нулю")
        return self.first / (self.second ** 2)

    def get_category(self):
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return "Недостаточный вес"
        elif bmi < 25:
            return "Норма"
        elif bmi < 30:
            return "Избыточный вес"
        else:
            return "Ожирение"


bmi = BMI()
bmi.read()
bmi.display()
try:
    print(f"ИМТ: {bmi.calculate_bmi():.2f}")
    print(f"Категория: {bmi.get_category()}")
except ValueError as e:
    print(f"Ошибка: {e}")