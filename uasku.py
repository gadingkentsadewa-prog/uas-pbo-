import tkinter as tk
from tkinter import messagebox
import random

# ==================================================
#                     MODEL (OOP)
# ==================================================
class Kereta:
    def __init__(self, kode, nama, tujuan):
        self.__kode = kode
        self.__nama = nama
        self.__tujuan = tujuan

    def get_info(self):
        return f"{self.__nama} ({self.__tujuan})"


class Tiket:
    def __init__(self, nama, jumlah):
        self._nama = nama
        self._jumlah = jumlah

    def hitung_harga(self):
        return 0


class TiketEkonomi(Tiket):
    def hitung_harga(self):
        return 50000 * self._jumlah


class TiketBisnis(Tiket):
    def hitung_harga(self):
        return 100000 * self._jumlah


class TiketEksekutif(Tiket):
    def hitung_harga(self):
        return 150000 * self._jumlah


# ==================================================
#                     APLIKASI GUI
# ==================================================
class AplikasiTiketKereta:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Pemesanan Tiket Kereta")
        self.root.geometry("800x850")
        self.root.configure(bg="#EEF2F7")

        self.jam_list = ["06:00", "08:00", "10:00", "12:00",
                         "14:00", "16:00", "18:00", "20:00"]

        self.bangku_terpilih = []
        self.bangku_buttons = {}

        self.kereta_list = [
            Kereta("K01", "Argo Bromo", "Surabaya - Jakarta"),
            Kereta("K02", "Mutiara Timur", "Surabaya - Banyuwangi"),
            Kereta("K03", "Sancaka", "Surabaya - Yogyakarta")
        ]

        self.build_ui()

    # ==================================================
    #                     UI
    # ==================================================
    def build_ui(self):
        self.header()
        self.form_card()
        self.seat_card()
        self.button_area()
        self.output_card()
        self.history_card()

    def header(self):
        header = tk.Frame(self.root, bg="#0F172A", height=60)
        header.pack(fill="x")
        tk.Label(
            header,
            text="SISTEM PEMESANAN TIKET KERETA API",
            bg="#0F172A",
            fg="white",
            font=("Segoe UI", 15, "bold")
        ).pack(pady=15)

    def form_card(self):
        card = tk.Frame(self.root, bg="white", padx=15, pady=15)
        card.pack(padx=20, pady=10, fill="x")

        def field(text):
            tk.Label(card, text=text, bg="white",
                     font=("Segoe UI", 10, "bold")).pack(anchor="w")

        field("Nama Penumpang")
        self.entry_nama = tk.Entry(card)
        self.entry_nama.pack(fill="x")

        field("Tanggal Keberangkatan (DD/MM/YYYY)")
        self.entry_tanggal = tk.Entry(card)
        self.entry_tanggal.pack(fill="x")

        field("Jam Keberangkatan")
        self.var_jam = tk.StringVar(value=self.jam_list[0])
        tk.OptionMenu(card, self.var_jam, *self.jam_list).pack(fill="x")

        field("Pilih Kereta")
        self.var_kereta = tk.StringVar(value=self.kereta_list[0].get_info())
        tk.OptionMenu(
            card,
            self.var_kereta,
            *[k.get_info() for k in self.kereta_list]
        ).pack(fill="x")

        field("Jumlah Tiket")
        self.entry_jumlah = tk.Entry(card)
        self.entry_jumlah.pack(fill="x")

        field("Kelas Tiket")
        self.var_kelas = tk.StringVar(value="Ekonomi")
        kelas_frame = tk.Frame(card, bg="white")
        kelas_frame.pack(anchor="w")
        for k in ["Ekonomi", "Bisnis", "Eksekutif"]:
            tk.Radiobutton(
                kelas_frame,
                text=k,
                variable=self.var_kelas,
                value=k,
                bg="white"
            ).pack(side="left", padx=6)

    # ==================================================
    #                  PILIH BANGKU
    # ==================================================
    def seat_card(self):
        seat_frame = tk.Frame(self.root, bg="white", padx=15, pady=15)
        seat_frame.pack(padx=20, pady=10)

        tk.Label(
            seat_frame,
            text="Pilih Bangku Penumpang",
            bg="white",
            font=("Segoe UI", 11, "bold")
        ).pack()

        grid = tk.Frame(seat_frame, bg="white")
        grid.pack(pady=10)

        rows = ["A", "B", "C", "D"]
        for r, row in enumerate(rows):
            for c in range(1, 6):
                seat = f"{row}{c}"
                btn = tk.Button(
                    grid,
                    text=seat,
                    width=5,
                    bg="#22C55E",
                    fg="white",
                    command=lambda s=seat: self.toggle_seat(s)
                )
                btn.grid(row=r, column=c, padx=4, pady=4)
                self.bangku_buttons[seat] = btn

    def toggle_seat(self, seat):
        if not self.entry_jumlah.get().isdigit():
            messagebox.showwarning("Validasi", "Isi jumlah tiket terlebih dahulu!")
            return

        jumlah = int(self.entry_jumlah.get())

        if seat in self.bangku_terpilih:
            self.bangku_terpilih.remove(seat)
            self.bangku_buttons[seat].config(bg="#22C55E")
        else:
            if len(self.bangku_terpilih) >= jumlah:
                messagebox.showwarning(
                    "Validasi",
                    "Jumlah bangku sudah sesuai jumlah tiket!"
                )
                return
            self.bangku_terpilih.append(seat)
            self.bangku_buttons[seat].config(bg="#2563EB")

    # ==================================================
    #                   BUTTON
    # ==================================================
    def button_area(self):
        btn = tk.Frame(self.root, bg="#EEF2F7")
        btn.pack()

        tk.Button(
            btn,
            text="Pesan Tiket",
            bg="#2563EB",
            fg="white",
            width=15,
            command=self.pesan_tiket
        ).pack(side="left", padx=8)

        tk.Button(
            btn,
            text="Reset",
            bg="#DC2626",
            fg="white",
            width=12,
            command=self.reset_semua
        ).pack(side="left")

    # ==================================================
    #                 OUTPUT & HISTORY
    # ==================================================
    def output_card(self):
        self.output = tk.Label(
            self.root,
            bg="white",
            font=("Consolas", 9),
            justify="left",
            padx=15,
            pady=15
        )
        self.output.pack(padx=20, pady=10, fill="x")

    def history_card(self):
        tk.Label(
            self.root,
            text="Riwayat Pemesanan",
            bg="#EEF2F7",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=22)

        self.text_riwayat = tk.Text(
            self.root,
            height=6,
            font=("Consolas", 9)
        )
        self.text_riwayat.pack(padx=20, pady=5, fill="x")

    # ==================================================
    #                    LOGIC
    # ==================================================
    def pesan_tiket(self):
        # VALIDASI WAJIB ISI SEMUA
        if self.entry_nama.get().strip() == "":
            messagebox.showwarning("Validasi", "Nama penumpang wajib diisi!")
            return

        if self.entry_tanggal.get().strip() == "":
            messagebox.showwarning("Validasi", "Tanggal keberangkatan wajib diisi!")
            return

        if not self.entry_jumlah.get().isdigit():
            messagebox.showwarning("Validasi", "Jumlah tiket harus berupa angka!")
            return

        jumlah = int(self.entry_jumlah.get())
        if jumlah <= 0:
            messagebox.showwarning("Validasi", "Jumlah tiket harus lebih dari 0!")
            return

        if len(self.bangku_terpilih) != jumlah:
            messagebox.showwarning(
                "Validasi",
                "Jumlah bangku harus sama dengan jumlah tiket!"
            )
            return

        # PROSES PEMESANAN
        kode = f"BK-{random.randint(10000,99999)}"

        tiket_class = {
            "Ekonomi": TiketEkonomi,
            "Bisnis": TiketBisnis,
            "Eksekutif": TiketEksekutif
        }

        tiket = tiket_class[self.var_kelas.get()](
            self.entry_nama.get(),
            jumlah
        )

        total = tiket.hitung_harga()
        diskon = total * 0.1 if jumlah >= 3 else 0
        total -= diskon

        struk = (
            f"Kode Booking : {kode}\n"
            f"Nama         : {self.entry_nama.get()}\n"
            f"Tanggal      : {self.entry_tanggal.get()}\n"
            f"Jam          : {self.var_jam.get()}\n"
            f"Kereta       : {self.var_kereta.get()}\n"
            f"Kelas        : {self.var_kelas.get()}\n"
            f"Bangku       : {', '.join(self.bangku_terpilih)}\n"
            f"Jumlah       : {jumlah}\n"
            f"Total        : Rp {int(total):,}\n"
        )

        self.output.config(text=struk)
        self.text_riwayat.insert(tk.END, struk + "-" * 45 + "\n")

    # ==================================================
    #                     RESET
    # ==================================================
    def reset_semua(self):
        self.entry_nama.delete(0, tk.END)
        self.entry_tanggal.delete(0, tk.END)
        self.entry_jumlah.delete(0, tk.END)
        self.var_kelas.set("Ekonomi")
        self.var_jam.set(self.jam_list[0])
        self.output.config(text="")
        self.text_riwayat.delete("1.0", tk.END)
        self.bangku_terpilih.clear()

        for btn in self.bangku_buttons.values():
            btn.config(bg="#22C55E")


# ==================================================
#                     RUN APP
# ==================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiTiketKereta(root)
    root.mainloop()
