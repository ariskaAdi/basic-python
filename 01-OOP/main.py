from models import company
from models import product

if __name__ == "__main__":

    data = []
    c1 = company.Company(name="Microsoft", products=[product.Product(name="Windows", category="Operating System")])

# print(c1.name, c1.products[0].name, c1.products[0].category)


class Song:
    note = "A class type to represent a song"
    version = 1.0

    def __init__(self, name = "", artist = "", album = "", released_year
= 2000):
        self.name = name
        self.artist = artist
        self.album = album
        self.released_year = released_year
def info(self):

    print(f"Song: {self.name} by {self.artist}")
    print(f"Album: {self.album}")
    print(f"Released year: {self.released_year}")

songs = [
Song(
name="The Ytse Jam",
artist="Dream Theater",
album="When Dream and Day Unite",
released_year=2004,
)]

# print(f"Song: {songs}")

def say_hello():
    print("Hello!")

# say_hello()

def my_decorator(func):
    def wrapper():
        print("Sebelum function dijalankan")

        func()

        print("Setelah function dijalankan")

    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

# say_hello()

from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int


user = User("Adi", 25)

print(user.name)  # Adi
print(user.age)   # 25

print(user)
# User(name='Adi', age=25)