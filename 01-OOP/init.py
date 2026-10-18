class Car:
    def __init__(self, name, model, year):
        self.name = name
        self.model = model
        self.year = year

car1 = Car("Toyota", "Camry", 2020)

# print(f"Car: {car1.name, car1.model, car1.year}")

def divide(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b

try:
    result = divide(10, 0)
except ValueError as error:
    # print(f"Error: {error}")
    pass

class Car:
    def __init__(self):
        self.name = ""
        self.manufacturer = ""
        self.year = 0
        self.description = ""

all_cars = []

car1 = Car()
car1.name = "M3 GTR"
car1.manufacturer = "BMW"
car1.year = 2001
car1.description = "Best car in NFS Most Wanted"
all_cars.append(car1)

car2 = Car()
car2.name = "RX-8"
car2.manufacturer = "Mazda"
car2.year = 2002
car2.description = "Best car in NFS Underground 2"
all_cars.append(car2)

car3 = Car()
car3.name = "Le Mans Quattro"
car3.manufacturer = "Audi"
car3.year = 2003
car3.description = "Best car in NFS Carbon"
all_cars.append(car3)

for c in all_cars:
    print(f"Car name: {c.manufacturer} {c.name}")
    print(f"Description: {c.description}")
    print(f"Year released: {c.year}")
    print()