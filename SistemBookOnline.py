import tkinter as tk
from tkinter import messagebox, ttk

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
JAM = ["08:00-10:00", "16:00-18:00", "19:00-21:00"]
KUOTA = 6  

BOOKING = {h: {j: [] for j in JAM} for h in HARI}


class AplikasiBookBoxing:
    def __init__(self, root):
        self.root = root
        root.title("Sistem Book Boxing Online ")
        root.geometry("420x560")
        root.resizable(False, False)

        self.buat_halaman_menu()
        self.buat_halaman_booking()
        self.tampil(self.halaman_menu)

    def tampil(self, halaman):
        self.halaman_menu.pack_forget()
        self.halaman_booking.pack_forget()
        halaman.pack(fill="both", expand=True)

    def buat_halaman_menu(self):
        self.halaman_menu = tk.Frame(self.root)

        tk.Label(self.halaman_menu, text="SISTEM BOOK BOXING ONLINE",
                 font=("Arial", 16, "bold")).pack(pady=(120, 5))
        tk.Label(self.halaman_menu, text="Silakan pilih menu di bawah ini",
                 font=("Arial", 10)).pack(pady=(0, 30))

        tk.Button(self.halaman_menu, text="Book Boxing", command=self.buka_booking,
                  bg="lightblue", width=25, height=2).pack(pady=8)
        tk.Button(self.halaman_menu, text="Keluar", command=self.keluar,
                  bg="lightcoral", width=25, height=2).pack(pady=8)

    def buat_halaman_booking(self):
        f = tk.Frame(self.root)
        self.halaman_booking = f

        tk.Label(f, text="Book Kelas Boxing", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(f, text="Pilih Hari:").pack()
        self.combo_hari = ttk.Combobox(f, values=HARI, state="readonly", width=22)
        self.combo_hari.current(0)
        self.combo_hari.pack(pady=3)
        self.combo_hari.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        tk.Label(f, text="Pilih Jam Latihan:").pack(pady=(12, 0))
        self.var_jam = tk.StringVar(value="")
        self.radio_jam = {}
        frame_jam = tk.Frame(f)
        frame_jam.pack()
        for jam in JAM:
            rb = tk.Radiobutton(frame_jam, text=jam, variable=self.var_jam,
                                value=jam, command=self.pilih_jam, anchor="w", width=28)
            rb.pack()
            self.radio_jam[jam] = rb

        self.label_status = tk.Label(f, text="", font=("Arial", 11, "bold"))
        self.label_status.pack(pady=10)

        tk.Label(f, text="Nama yang sudah book:").pack()
        self.listbox = tk.Listbox(f, height=6, width=32)
        self.listbox.pack(pady=3)

        tk.Label(f, text="Nama Anda:").pack(pady=(10, 0))
        self.entry_nama = tk.Entry(f, width=25)
        self.entry_nama.pack(pady=2)
        tk.Button(f, text="Book Sekarang", command=self.book,
                  bg="lightgreen", width=20).pack(pady=8)

        tk.Button(f, text="Kembali", command=self.kembali,
                  width=20).pack(pady=2)

        self.refresh()

    def buka_booking(self):
        self.tampil(self.halaman_booking)

    def kembali(self):
        self.var_jam.set("")
        self.entry_nama.delete(0, tk.END)
        self.refresh()
        self.tampil(self.halaman_menu)

    def keluar(self):
        if messagebox.askyesno("Keluar", "Yakin ingin keluar dari aplikasi?"):
            self.root.destroy()

    def refresh(self):
        hari = self.combo_hari.get()

        for jam, rb in self.radio_jam.items():
            terisi = len(BOOKING[hari][jam])
            rb.config(text=f"{jam}  ({terisi}/{KUOTA})")

        self.listbox.delete(0, tk.END)
        jam = self.var_jam.get()

        if jam == "":
            self.label_status.config(text="Silakan pilih jam latihan", fg="black")
            return

        daftar = BOOKING[hari][jam]
        if len(daftar) == 0:
            self.listbox.insert(tk.END, "(belum ada yang book)")
        for i, nama in enumerate(daftar, start=1):
            self.listbox.insert(tk.END, f"{i}. {nama}")

        if len(daftar) >= KUOTA:
            self.label_status.config(text="Maaf kelas ini penuh", fg="red")
        else:
            sisa = KUOTA - len(daftar)
            self.label_status.config(text=f"Slot tersedia: {sisa} dari {KUOTA}", fg="green")

    def pilih_jam(self):
        self.refresh()
        hari = self.combo_hari.get()
        jam = self.var_jam.get()
        if len(BOOKING[hari][jam]) >= KUOTA:
            messagebox.showwarning("Kelas Penuh", "Maaf kelas ini penuh")

    def book(self):
        hari = self.combo_hari.get()
        jam = self.var_jam.get()
        nama = self.entry_nama.get().strip()

        if jam == "":
            messagebox.showerror("Error", "Pilih jam latihan terlebih dahulu!")
            return
        if nama == "":
            messagebox.showerror("Error", "Nama wajib diisi!")
            return

        daftar = BOOKING[hari][jam]
        if len(daftar) >= KUOTA:
            messagebox.showwarning("Kelas Penuh", "Maaf kelas ini penuh")
            return
        if nama.lower() in [n.lower() for n in daftar]:
            messagebox.showerror("Error", f"{nama} sudah book di kelas ini!")
            return

        daftar.append(nama)
        messagebox.showinfo(
            "Booking Berhasil",
            f"Nama: {nama}\nHari: {hari}\nJam: {jam}\n\nBooking berhasil!"
        )
        self.entry_nama.delete(0, tk.END)
        self.refresh()


if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiBookBoxing(root)
    root.mainloop()