from datetime import datetime
import os

# Słownik numer miesiąca -> nazwa
MONTHS_NUM_TO_NAME = {
    "01": "Styczeń", "02": "Luty", "03": "Marzec",
    "04": "Kwiecień", "05": "Maj", "06": "Czerwiec",
    "07": "Lipiec", "08": "Sierpień", "09": "Wrzesień",
    "10": "Październik", "11": "Listopad", "12": "Grudzień"
}

EXPENSE_FILE = r"G:\Mój dysk\menedzer_finansow\historia_wydatkow.txt"


class Expense:
    """Klasa reprezentująca pojedynczy wydatek"""

    def __init__(self, amount: float, category: str, description: str, date: str):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    def __str__(self):
        return f"{self.amount:.2f} | {self.category} | {self.description} | {self.date}"


class MenedzerWydatkow:
    """Klasa odpowiedzialna za operacje na pliku (zapis/odczyt)"""

    def __init__(self, sciezka_pliku=EXPENSE_FILE):
        self.sciezka_pliku = sciezka_pliku
        self._upewnij_sie_ze_plik_istnieje()

    def _upewnij_sie_ze_plik_istnieje(self):
        folder = os.path.dirname(self.sciezka_pliku)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        if not os.path.exists(self.sciezka_pliku):
            with open(self.sciezka_pliku, "w", encoding="utf-8") as f:
                pass

    def zapisz_wydatek(self, wydatek: Expense):
        with open(self.sciezka_pliku, "a", encoding="utf-8") as f:
            f.write(str(wydatek) + "\n")

    def oblicz_sume_calkowita(self) -> float:
        total_sum = 0
        with open(self.sciezka_pliku, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    amount_str = line.split("|")[0].strip()
                    total_sum += float(amount_str)
        return total_sum

    def oblicz_sume_miesieczna(self, numer_miesiaca: str) -> float:
        total_month_sum = 0
        with open(self.sciezka_pliku, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) >= 4:
                    amount = float(parts[0].strip())
                    expense_date = parts[3].strip()
                    month_in_file = expense_date.split(".")[1]

                    if month_in_file == numer_miesiaca:
                        total_month_sum += amount
        return total_month_sum
    def list_all_expenses(self):
        with open(self.sciezka_pliku, "r", encoding="utf-8") as f:
            for line in f:
                print(line)



# --- INICJALIZACJA ---
menedzer = MenedzerWydatkow()

print("--- MENEDŻER FINANSÓW ---")

while True:
    print("\n1. Dodaj wydatek")
    print("2. Pokaż sumę WSZYSTKICH wydatków")
    print("3. Pokaż wydatki z wybranego miesiąca")
    print("4. Pokaz liste wszyzstkich wydatkow")
    print("5. Wyjdź")

    user_choice = input("\nCo chcesz zrobić? (1-4): ").strip()

    match user_choice:
        case "1":
            while True:
                try:
                    amount = float(input("Podaj kwotę (zł): "))
                    if amount <= 0:
                        print("Kwota musi być większa od zera!")
                        continue
                    category = input("Podaj kategorię (np. Jedzenie, Paliwo): ").strip()
                    description = input("Podaj opis: ").strip()
                    break
                except ValueError:
                    print("Błąd! Wpisz poprawną liczbę.")

            current_date = datetime.now().strftime("%d.%m.%Y")
            nowy_wydatek = Expense(amount, category, description, current_date)

            # Używamy dedykowanej metody!
            menedzer.zapisz_wydatek(nowy_wydatek)
            print("\n✅ Wydatek został pomyślnie dodany!")

        case "2":
            suma = menedzer.oblicz_sume_calkowita()
            print(f"\nSuma wszystkich wpisanych wydatków to: {suma:.2f} zł")

        case "3":
            current_month_num = datetime.now().strftime("%m")
            month_name = MONTHS_NUM_TO_NAME[current_month_num]

            suma_miesiac = menedzer.oblicz_sume_miesieczna(current_month_num)
            print(f"\nSuma wydatków za ten miesiąc ({month_name}): {suma_miesiac:.2f} zł")
        case "4":
            print(f"Wszystkie dotychczasowe wydatki:")
            list_all_expenses = menedzer.list_all_expenses()
        case "5":
            print("\nDo zobaczenia!")
            break

        case _:
            print("\nNiepoprawny wybór. Wybierz opcję od 1 do 4.")