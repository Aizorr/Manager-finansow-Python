from datetime import datetime
import os

MONTHS_NUM_TO_NAME = {
    "01": "Styczeń",    "02": "Luty",       "03": "Marzec",
    "04": "Kwiecień",   "05": "Maj",        "06": "Czerwiec",
    "07": "Lipiec",     "08": "Sierpień",   "09": "Wrzesień",
    "10": "Październik","11": "Listopad",   "12": "Grudzień"
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

    def pobierz_wszystkie_linie(self) -> list[str]:
        if not os.path.exists(self.sciezka_pliku):
            return []
        with open(self.sciezka_pliku, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def oblicz_sume_calkowita(self) -> float:
        total_sum = 0
        for line in self.pobierz_wszystkie_linie():
            amount_str = line.split("|")[0].strip()
            total_sum += float(amount_str)
        return total_sum

    def oblicz_sume_miesieczna(self, numer_miesiaca: str) -> float:
        total_month_sum = 0
        for line in self.pobierz_wszystkie_linie():
            parts = line.split("|")
            if len(parts) >= 4:
                amount = float(parts[0].strip())
                expense_date = parts[3].strip()
                month_in_file = expense_date.split(".")[1]

                if month_in_file == numer_miesiaca:
                    total_month_sum += amount
        return total_month_sum