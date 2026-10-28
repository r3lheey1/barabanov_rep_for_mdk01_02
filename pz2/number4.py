class Average:
    def get_average(self, *args):
        if len(args) == 0:
            return 0
        return sum(args) / len(args)


avg = Average()
numbers = []

while True:
    s = input("введите число (enter для расчета): ")
    if s == "":
        break
    try:
        numbers.append(float(s))
    except ValueError:
        print("Ошибка: введите число!")

print(f"Среднее значение: {avg.get_average(*numbers)}")

