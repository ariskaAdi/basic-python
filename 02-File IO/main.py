# file = open("data.txt", "r")

# # content = file.read() # baca semua isi file
# # content = file.readline() # baca satu baris saja
# content = file.readlines() # baca semua baris dan simpan dalam list
# print(content)

# file.close()


# with open("data.txt", "r", encoding="utf-8") as file:
#     content = file.read()
#     print(content)

# tulis


# with open("hasil.txt", "w", encoding="utf-8") as file:
#     file.write("Hasil analisis data\n")
#     file.write("Rata-rata nilai: 85\n")


# hitung rata-rata
with open("nilai.txt", "r", encoding="utf-8") as file:
    values = [float(line.strip()) for line in file]

average = sum(values) / len(values)

print("Nilai:", values)
print("Rata-rata:", average)

with open("hasil.txt", "w", encoding="utf-8") as file:
    file.write(f"Rata-rata nilai: {average:.2f}\n")


from pathlib import Path

file = Path("data.txt")

print(file.exists())  # Apakah file ada?
print(file.name)      # Nama file: data.txt
print(file.suffix)    # Ekstensi: .txt
print(file.parent)    # Folder induk