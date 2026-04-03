import datetime
def manager():
    suma_wydatkow_na_miesiac = 0
    try:
        with open("wydatki.txt" ,"r") as file:
            for line in file:
                if ":" in line:
                    szukane_wydatki = line.split(sep=":")[-1]
                    wydatki_float = szukane_wydatki.replace("zl","").strip()
                    suma_wydatkow_na_miesiac += float(wydatki_float)
            ostatnia_data_w_pliku = line.split()[0]
            ostatnia_data_w_pliku = datetime.datetime.strptime(ostatnia_data_w_pliku, "[%Y-%m-%d]").date()
            print(ostatnia_data_w_pliku)
        dzisiaj = datetime.date.today()
        ile_dni_przerwy = (dzisiaj - ostatnia_data_w_pliku).days
        if ile_dni_przerwy >=1:
            print(f"Tyle dni ciebie nie bylo: {ile_dni_przerwy}")
            for i in range(1,ile_dni_przerwy+1):
                brakujaca_data = ostatnia_data_w_pliku + datetime.timedelta(days=i-1)
                print(f"Uzupelnianie {brakujaca_data}")
                try:
                    kwota = float(input(f"Ile wtedy wydałeś? "))
                    kat = input("Na co? ")
                    with open("wydatki.txt", "a") as file:
                        file.write(f"[{brakujaca_data}] [{kat}]: {kwota}zl\n")
                    suma_wydatkow_na_miesiac += kwota
                except ValueError:
                    print("Pominąłeś ten dzień przez błędną kwotę!")
                    continue
        else:
            print("Jestes na biezaco")
    except FileNotFoundError:
        print("Nie znaleziono pliku")

    while True:
        print("1.Chcesz dodac wydatek\n"
              "2.Chcesz zobaczyc sume wydatkow"
              "\n3.Wyjdz")
        try:
            wybor = int(input())
            match wybor:
                case 1:
                    try:
                        wydatek = float(input("Ile wydales dzisiaj kasy: "))
                        suma_wydatkow_na_miesiac += wydatek
                        kategoria_wydatku = str(input("Na co wydales te pieniadze: "))
                        with open("wydatki.txt", "a") as file:
                            (file.write(f"[{dzisiaj}] [{kategoria_wydatku}]: {wydatek}zl\n"))
                        print("zapisano")
                    except ValueError:
                        print("Zle wpisales kwote. Wpisz jeszcze raz")
                case 2:
                    print(f"Suma wydatkow w tym miesiacu = {suma_wydatkow_na_miesiac}zl")
                case 3:
                    break
                case _:
                    print("Wybierz z listy 1-3")
        except ValueError :
            print("zle wpisales numer")
if __name__ == "__main__":
    manager()