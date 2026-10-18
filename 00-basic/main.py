#%%
# print("hello world")
# %%
# komentar

nama_mahasiswa = "John Doe"
umur_mahasiswa = 30
nilai_ujian = 85.5
laki = True

# print("Nama: %s" %nama + ", Umur:", umur, ", Laki-laki:", laki)

# deklarasi banyak variable
nilai_mahasiswa_1, nilai_mahasiswa_2, nilai_mahasiswa_3 = 90, 85, 95
rata_nilai = (nilai_mahasiswa_1 + nilai_mahasiswa_2 + nilai_mahasiswa_3) / 3
# print("Rata-rata nilai mahasiswa: %f" %rata_nilai)

# konstanta
from typing import Final
PI : Final = 3.14
# print("Nilai PI: %f" %PI)

# null atau none
data = None
# print("Data: %s" %data)

list_1 = [1, 2, 3, 4, 5]
list_2 = ["adi", "budi", "caca"]

# list dengan tipe data campuran
list_3 = [1, "budi", 3.14, True]
# print(list_1[2])

# tuple tdak bisa diubah
tuple_1 = (1, 2, 3, 4, 5)
# print(tuple_1[3])

# tipe data dictionary
dict_1 = {
    "nama": "John Doe",
    "umur": 30,
    "nilai": 85.5,
    "laki": True
}

angka_1 = 2
angka_2 = 2
# print("apakah sama ? %s" %(angka_1 == angka_2))

# fungsi id
data_1 = "hello world"
is_data_1 = id(data_1)

# print("id data_1: %s" %is_data_1)

sample_list = [1, 2, 3, 4, 5]
is_3_exist = 3 in sample_list
# print("Apakah 3 ada di sample_list ? %s" %is_3_exist)

# str_input = input("Masukkan nilai anda: ")
# grade = int(str_input)

# if grade >= 90:
#     print("Grade A")
# elif grade >= 80:
#     print("Grade B")
# elif grade >= 70:
#     print("Grade C")
# else :
#     print("Grade D")


# for i in range(5):
#     print("Perulangan ke-%d" %i)

r = range(5)
# print("r", list(r))7
# output r [0, 1, 2, 3, 4]

# max = int(input("Masukkan nilai maksimal: "))

# for i in range(max):
#     for j in range(0, max - i):
#         print("*", end="")
#     print()

# n = int(input("Masukkan nilai n: "))
# i = 0

# while i < n:
#     print("Perulangan ke-%d" %i)
#     i += 1

# list_1 = [10, 20, 30, 40, 50]
# for i in range(0, len(list_1)):
#     print("Index ke-%d: %d" %(i, list_1[i]))

# list_1 = [10, 20, 30, 40, 50]
# for i, v in enumerate(list_1):
#     print("index ke:" , i, "element ke:", v)

# matrix = [
# [0, 1, 0, 1, 0],
# [1, 1, 1, 0, 0],
# [0, 0, 0, 1, 1],
# [0, 1, 1, 1, 0],
# ]
# for row in matrix:
#     for cell in row:
#         print(cell, end=" ")
#     print()

# range_1 = range(0, 10)
# list_1 = list(range_1)
# print("list_1:", list_1)

# genap = [i * 2 for i in range(10)]
# print("genap:", genap)

# ganjil_lagi = [i for i in range(10) if i % 2 == 1]
# print("ganjil_lagi:", ganjil_lagi)

# list_x = ['a', 'b', 'c']
# list_y = ['1', '2', '3']

# seq = []
# for x in list_x:
#     for y in list_y:
#         seq.append(x + y)

# seq_2 = [x + y for x in list_x for y in list_y]

# print("seq CARA_1:", seq)
# print("seq CARA_2:", seq_2)

# MATRIX
MATRIX = [
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12],
]

transposed = []
for i in range(4):
    tr = []
    for row in MATRIX:
        tr.append(row[i])
    transposed.append(tr)

transposed_cara_2 = [[row[i] for row in MATRIX] for i in range(4)]
# print(transposed)
# print(transposed_cara_2)

def print_hello():
    print("hello world")

def luas_lingkaran(r):
    area = 3.14 * (r ** 2)
    print("Luas lingkaran dengan jari-jari %d adalah %f" %(r, area))

def luas_lingkaran_lengkap(message: str, r: int):
    area = 3.14 * (r ** 2)
    print("%s dengan jari-jari %d adalah %f" %(message, r, area))

def calculate_circle_area(r: int) -> float:
    area = 3.14 * (r ** 2)
    return area

# print(calculate_circle_area(10))

def sum_the_print(*number):
    total = 0
    for n in number:
        total += n
    print("Total:", total)

# print(sum_the_print(1, 2, 3, 4, 5))

mahasiswa = [
    {"nama": "Budi", "nilai": 80},
    {"nama": "Ani", "nilai": 95},
    {"nama": "Citra", "nilai": 75}
]

mahasiswa.sort(key=lambda x: x["nilai"])
# print(mahasiswa)

def print_matrix(matrix=[]):
    if len(matrix) == 0:
        print("[]")

    for el in matrix:
        print(el)

# print_matrix(MATRIX)

def print_data(**data):
    print(f"type data: {type(data)}")
    print(f"data: {data}")

    for key in data:
        print(f"param: {key}, value: {data[key]}")

print_data(phone="nokia 3310", discontinue=False, year=2000,
networks=["GSM", "TDMA"])