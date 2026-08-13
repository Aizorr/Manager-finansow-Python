from datetime import datetime

# Słownik numer miesiąca -> nazwa (używany do ładnego wyświetlania)
MONTHS_NUM_TO_NAME = {
    "01": "Styczeń",    "02": "Luty",       "03": "Marzec",
    "04": "Kwiecień",   "05": "Maj",        "06": "Czerwiec",
    "07": "Lipiec",     "08": "Sierpień",   "09": "Wrzesień",
    "10": "Październik","11": "Listopad",   "12": "Grudzień"
}

class Expense:
    def __init__(self, amount: float, category: str, description: str, date: str):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    def __str__(self):
        # Format zapisu w pliku: Kwota | Kategoria | Opis | Data
        return f"{self.amount:.2f} | {self.category} | {self.description} | {self.date}"


# Generowanie dzisiejszej daty w formacie DD.MM.YYYY
current_date = datetime.now().strftime("%d.%m.%Y")

print("--- MENEDŻER FINANSÓW ---")
print("1. Dodaj wydatek")
print("2. Pokaż sumę WSZYSTKICH wydatków")
print("3. Pokaż wydatki z wybranego miesiąca")
print("4. Wyjdź")
while True:
    user_choice = input("\nCo chcesz zrobić? (1-4)").strip()
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
                    print("Błąd! Wpisz poprawną liczbę (użyj kropki dla groszy).")

            new_expense = Expense(amount, category, description, current_date)

            with open("menedzersiana.txt", "a", encoding="utf-8") as file:
                file.write(str(new_expense) + "\n")

            print("\n✅ Wydatek został pomyślnie dodany!")

        case "2":
            try:
                total_sum = 0
                with open("menedzersiana.txt", "r", encoding="utf-8") as file:
                    for line in file:
                        # Wyciągamy kwotę z pierwszej części linii (przed pierwszym |)
                        amount_str = line.split("|")[0].strip()
                        total_sum += float(amount_str)

                print(f"\nSuma wszystkich wpisanych wydatków to: {total_sum:.2f} zł")

            except FileNotFoundError:
                print("\nBrak zapisanych wydatków. Dodaj swój pierwszy wydatek!")

        case "3":
            # Pobieramy numer obecnego miesiąca (np. "08")
            current_month_num = datetime.now().strftime("%m")
            month_name = MONTHS_NUM_TO_NAME[current_month_num]

            total_month_sum = 0

            try:
                with open("menedzersiana.txt", "r", encoding="utf-8") as file:
                    for line in file:
                        parts = line.strip().split("|")

                        if len(parts) >= 4:
                            amount = float(parts[0].strip())
                            expense_date = parts[3].strip()  # np. "13.08.2026"
                            month_in_file = expense_date.split(".")[1]  # np. "08"

                            # Jeśli miesiąc z pliku zgadza się z obecnym miesiącem
                            if month_in_file == current_month_num:
                                total_month_sum += amount

                print(f"\nSuma wydatków za ten miesiąc ({month_name}): {total_month_sum:.2f} zł")

            except FileNotFoundError:
                print("\nBrak pliku z wydatkami.")
        case "4":
            break
        case _:
            print("\nNiepoprawny wybór. Wybierz opcję od 1 do 3.")