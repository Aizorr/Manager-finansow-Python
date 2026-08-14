from datetime import datetime
import customtkinter as ctk

# Importujemy logikę z drugiego pliku!
from menedzersiana import Expense, MenedzerWydatkow, MONTHS_NUM_TO_NAME

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.menedzer = MenedzerWydatkow()

        # Konfiguracja głównego okna
        self.title("Menedżer Finansów")
        self.geometry("480x720")
        self.resizable(False, False)

        # --- NAGŁÓWEK ---
        self.title_label = ctk.CTkLabel(
            self, text="Menedżer Finansów", font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.pack(pady=(15, 5))

        # --- SEKCJA: DODAWANIE WYDATKU ---
        self.frame_add = ctk.CTkFrame(self)
        self.frame_add.pack(padx=20, pady=5, fill="x")

        self.entry_amount = ctk.CTkEntry(self.frame_add, placeholder_text="Kwota (zł)")
        self.entry_amount.pack(padx=10, pady=4, fill="x")

        self.entry_category = ctk.CTkEntry(self.frame_add, placeholder_text="Kategoria (np. Jedzenie)")
        self.entry_category.pack(padx=10, pady=4, fill="x")

        self.entry_description = ctk.CTkEntry(self.frame_add, placeholder_text="Opis")
        self.entry_description.pack(padx=10, pady=4, fill="x")

        self.btn_add = ctk.CTkButton(
            self.frame_add, text="➕ Dodaj wydatek", command=self.dodaj_wydatek, fg_color="#2b8a3e", hover_color="#216a30"
        )
        self.btn_add.pack(padx=10, pady=8, fill="x")

        # --- SEKCJA: STATYSTYKI I SUMY ---
        self.frame_stats = ctk.CTkFrame(self)
        self.frame_stats.pack(padx=20, pady=5, fill="x")

        self.btn_sum_all = ctk.CTkButton(
            self.frame_stats, text="💰 Suma wszystkich wydatków", command=self.pokaz_sume_wszystkich
        )
        self.btn_sum_all.pack(padx=10, pady=4, fill="x")

        self.btn_sum_month = ctk.CTkButton(
            self.frame_stats, text="📅 Suma z obecnego miesiąca", command=self.pokaz_sume_miesieczna
        )
        self.btn_sum_month.pack(padx=10, pady=4, fill="x")

        # --- POLE KOMUNIKATÓW / WYNIKÓW ---
        self.lbl_status = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=14, weight="bold"), text_color="yellow"
        )
        self.lbl_status.pack(pady=5)

        # --- SEKCJA: LISTA PRZEWIJANA (HISTORIA WYDATKÓW) ---
        self.lbl_history = ctk.CTkLabel(
            self, text="📋 Historia Wydatków", font=ctk.CTkFont(size=15, weight="bold")
        )
        self.lbl_history.pack(pady=(5, 0))

        self.scrollable_frame = ctk.CTkScrollableFrame(self, height=200)
        self.scrollable_frame.pack(padx=20, pady=5, fill="both", expand=True)

        self.odswiez_liste_wydatkow()

    # --- LOGIKA OBSŁUGI ---
    def dodaj_wydatek(self):
        try:
            amount = float(self.entry_amount.get().replace(",", "."))
            if amount <= 0:
                self.lbl_status.configure(text="⚠️ Kwota musi być większa od zera!", text_color="orange")
                return

            category = self.entry_category.get().strip()
            description = self.entry_description.get().strip()

            if not category or not description:
                self.lbl_status.configure(text="⚠️ Uzupełnij kategorię i opis!", text_color="orange")
                return

            current_date = datetime.now().strftime("%d.%m.%Y")
            nowy_wydatek = Expense(amount, category, description, current_date)
            self.menedzer.zapisz_wydatek(nowy_wydatek)

            self.entry_amount.delete(0, "end")
            self.entry_category.delete(0, "end")
            self.entry_description.delete(0, "end")

            self.lbl_status.configure(text="✅ Wydatek został dodany!", text_color="#51cf66")
            self.odswiez_liste_wydatkow()

        except ValueError:
            self.lbl_status.configure(text="❌ Błąd! Wpisz poprawną kwotę.", text_color="#ff6b6b")

    def odswiez_liste_wydatkow(self):
        for child in self.scrollable_frame.winfo_children():
            child.destroy()

        linie = self.menedzer.pobierz_wszystkie_linie()

        if not linie:
            lbl_empty = ctk.CTkLabel(self.scrollable_frame, text="Brak zapisanych wydatków.", text_color="gray")
            lbl_empty.pack(pady=10)
            return

        for line in reversed(linie):
            parts = line.split("|")
            if len(parts) >= 4:
                kwota = parts[0].strip()
                kategoria = parts[1].strip()
                opis = parts[2].strip()
                data = parts[3].strip()

                item_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#2b2b2b")
                item_frame.pack(fill="x", pady=3, padx=2)

                text_main = f"💰 {kwota} zł  |  {kategoria} - {opis}"
                lbl_text = ctk.CTkLabel(item_frame, text=text_main, font=ctk.CTkFont(size=12, weight="bold"), anchor="w")
                lbl_text.pack(side="left", padx=10, pady=5)

                lbl_date = ctk.CTkLabel(item_frame, text=data, font=ctk.CTkFont(size=11), text_color="gray")
                lbl_date.pack(side="right", padx=10, pady=5)

    def pokaz_sume_wszystkich(self):
        suma = self.menedzer.oblicz_sume_calkowita()
        self.lbl_status.configure(
            text=f"Suma wszystkich wydatków: {suma:.2f} zł", text_color="white"
        )

    def pokaz_sume_miesieczna(self):
        current_month_num = datetime.now().strftime("%m")
        month_name = MONTHS_NUM_TO_NAME.get(current_month_num, "ten miesiąc")
        suma_miesiac = self.menedzer.oblicz_sume_miesieczna(current_month_num)

        self.lbl_status.configure(
            text=f"Suma za {month_name}: {suma_miesiac:.2f} zł", text_color="white"
        )


if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()