from datetime import datetime
data = datetime.now().strftime("%d.%m.%Y")
class Wydatek:
    def __init__(self, kwota, kategoria,opis, data):
        self.kwota = kwota
        self.kategoria = kategoria
        self.opis = opis
        self.data = data
    def __str__(self):
        return f"{self.kwota:.2f}, {self.kategoria}, {self.opis}, {self.data}"


print("---MENEDZER FINANSOW---")
print("1. Dodac wydatek")
print("2. Pokaz podsumowanie")
wybor = input("Co chcesz zrobic?")
match wybor:
    case "1":
        while True:
            try:
                kwota = float(input("Podaj kwota: "))
                kategoria = input("Podaj kategoria: ")
                opis = input("Podaj opis: ")
                break
            except ValueError:
                print("Cos zle wpisales")
        nowy_wydatek = Wydatek(kwota, kategoria, opis, data)
        with open("menedzersiana.txt", "a") as file:
            file.write(str(nowy_wydatek) + "\n")
    case "2":
        try:
            with open("menedzersiana.txt", "r") as file:
                suma = 0
                for line in file:
                    nowa_line=float(line.split(", ")[0])
                    suma += nowa_line
                print(f"Suma wszystkich wpisanych wydatkow to: {suma}zl")
        except FileNotFoundError:
            print("Nie znaleziono pliku.")
