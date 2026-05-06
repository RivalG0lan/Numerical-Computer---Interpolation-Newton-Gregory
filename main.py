"""
main.py — Program Interpolasi Numerik
======================================
Mata Kuliah: Komputasi Numerik

Interpolasi adalah metode untuk mengestimasi nilai fungsi f(x) pada titik x
yang tidak diketahui, berdasarkan sejumlah titik data yang sudah diketahui.

Tersedia 5 metode interpolasi:
  1. Linear       — f(x) sebagai garis lurus antara 2 titik
  2. Kuadratik    — polinom derajat 2 menggunakan 3 titik
  3. Kubik        — polinom derajat 3 menggunakan 4 titik
  4. Newton Maju  — tabel selisih maju, cocok untuk x mendekati awal data
  5. Newton Mundur— tabel selisih mundur, cocok untuk x mendekati akhir data
"""

import os
from interpolasi.linear import linear_interpolation
from interpolasi.kuadratik import quadratic_interpolation
from interpolasi.kubik import cubic_interpolation
from interpolasi.newton_maju import newton_forward
from interpolasi.newton_mundur import newton_backward
from utils.plot import plot_interpolation


# ── helpers ────────────────────────────────────────────────────────────────────

def input_xy(min_points=None, exact=None):
    """
    Minta input titik data (x, y) dari pengguna dengan validasi.

    Parameter:
        min_points : int — jumlah minimum titik yang diperlukan
        exact      : int — jumlah titik yang tepat diperlukan

    Return:
        (x_points, y_points) — list float yang sudah diurutkan berdasarkan x.

    Catatan Numerik:
        Data diurutkan berdasarkan x secara ascending sebelum diproses.
        Ini penting karena metode tabel selisih mengasumsikan x₀ < x₁ < ... < xₙ.
    """
    while True:
        try:
            x_points = list(map(float, input("Masukkan nilai x (pisah spasi): ").split()))
            y_points = list(map(float, input("Masukkan nilai y (pisah spasi): ").split()))

            if len(x_points) != len(y_points):
                print("  ✖ Error: jumlah x dan y harus sama!\n")
                continue

            if exact and len(x_points) != exact:
                print(f"  ✖ Error: metode ini butuh tepat {exact} titik!\n")
                continue

            if min_points and len(x_points) < min_points:
                print(f"  ✖ Error: minimal {min_points} titik dibutuhkan!\n")
                continue

            # --- Sorting otomatis ---
            # Urutkan pasangan (x, y) berdasarkan nilai x naik (ascending).
            # Penting untuk Newton Forward/Backward agar tabel selisih konsisten.
            combined = sorted(zip(x_points, y_points))
            x_points, y_points = map(list, zip(*combined))

            if len(set(x_points)) != len(x_points):
                print("  ✖ Error: nilai x tidak boleh duplikat!\n")
                continue

            return x_points, y_points

        except ValueError:
            print("  ✖ Input tidak valid, coba lagi.\n")


def input_x_target():
    """Minta input nilai x yang ingin diinterpolasi."""
    while True:
        try:
            return float(input("Masukkan x yang dicari: "))
        except ValueError:
            print("  ✖ Input tidak valid.\n")


def tanya_tampilkan_grafik():
    """Tanya apakah pengguna ingin melihat grafik hasil interpolasi."""
    ans = input("Tampilkan grafik? (y/n): ").strip().lower()
    return ans == "y"


def cetak_info_metode(nama_metode, deskripsi):
    """
    Cetak header informasi metode yang sedang digunakan.
    Membantu pengguna memahami metode apa yang dipakai dan mengapa.
    """
    print(f"\n[Metode: {nama_metode}]")
    print(f"  ℹ  {deskripsi}")


# ── menu ───────────────────────────────────────────────────────────────────────

def main():
    while True:
        print("\n" + "=" * 45)
        print("       PROGRAM INTERPOLASI NUMERIK")
        print("=" * 45)
        print("  1. Interpolasi Linear")
        print("  2. Interpolasi Kuadratik")
        print("  3. Interpolasi Kubik")
        print("  4. Newton Forward")
        print("  5. Newton Backward")
        print("  6. Bandingkan Semua Metode")
        print("  7. Input dari File CSV")
        print("  8. Contoh Kasus Nyata (Suhu / Penjualan / Fisika)")
        print("  0. Keluar")
        print("-" * 45)

        try:
            choice = int(input("  Pilih metode [0-8]: "))
        except ValueError:
            print("  ✖ Masukkan angka!")
            continue

        # ── 1. Linear ──────────────────────────────────────────────────────────
        if choice == 1:
            cetak_info_metode(
                "Interpolasi Linear",
                "Estimasi f(x) dengan garis lurus antara dua titik.\n"
                "  Rumus: f(x) = y0 + [(x-x0)/(x1-x0)] * (y1-y0)"
            )
            try:
                x0 = float(input("x0: "))
                y0 = float(input("y0: "))
                x1 = float(input("x1: "))
                y1 = float(input("y1: "))
            except ValueError:
                print("  ✖ Input tidak valid.")
                continue

            x = input_x_target()

            try:
                hasil = linear_interpolation(x0, y0, x1, y1, x)
                print(f"\n  ✔ Hasil f({x}) = {hasil:.6f}")

                if tanya_tampilkan_grafik():
                    def func(xi):
                        return linear_interpolation(x0, y0, x1, y1, xi)
                    plot_interpolation([x0, x1], [y0, y1], func, "Interpolasi Linear")

            except ValueError as e:
                print(f"  ✖ Error: {e}")

        # ── 2. Kuadratik ───────────────────────────────────────────────────────
        elif choice == 2:
            cetak_info_metode(
                "Interpolasi Kuadratik",
                "Polinom derajat 2 melalui 3 titik menggunakan divided differences.\n"
                "  P(x) = b0 + b1(x-x0) + b2(x-x0)(x-x1)"
            )
            x_points, y_points = input_xy(exact=3)
            x = input_x_target()

            try:
                result, coef = quadratic_interpolation(x_points, y_points, x)
                b0, b1, b2 = coef
                print(f"\n  Koefisien Newton (Divided Differences):")
                print(f"    b0 = {b0:.6f}  ← f[x0]")
                print(f"    b1 = {b1:.6f}  ← f[x0,x1]")
                print(f"    b2 = {b2:.6f}  ← f[x0,x1,x2]")
                print(f"\n  ✔ Hasil f({x}) = {result:.6f}")

                if tanya_tampilkan_grafik():
                    def func(xi):
                        return quadratic_interpolation(x_points, y_points, xi)[0]
                    plot_interpolation(x_points, y_points, func, "Interpolasi Kuadratik")

            except ValueError as e:
                print(f"  ✖ Error: {e}")

        # ── 3. Kubik ───────────────────────────────────────────────────────────
        elif choice == 3:
            cetak_info_metode(
                "Interpolasi Kubik",
                "Polinom derajat 3 melalui 4 titik menggunakan divided differences.\n"
                "  P(x) = b0 + b1(x-x0) + b2(x-x0)(x-x1) + b3(x-x0)(x-x1)(x-x2)"
            )
            x_points, y_points = input_xy(exact=4)
            x = input_x_target()

            try:
                result = cubic_interpolation(x_points, y_points, x)
                print(f"\n  ✔ Hasil f({x}) = {result:.6f}")

                if tanya_tampilkan_grafik():
                    def func(xi):
                        return cubic_interpolation(x_points, y_points, xi)
                    plot_interpolation(x_points, y_points, func, "Interpolasi Kubik")

            except ValueError as e:
                print(f"  ✖ Error: {e}")

        # ── 4. Newton Forward ──────────────────────────────────────────────────
        elif choice == 4:
            cetak_info_metode(
                "Newton Forward (Interpolasi Selisih Maju)",
                "Gunakan saat x yang dicari mendekati awal data.\n"
                "  Syarat: jarak antar x harus sama (equal spacing).\n"
                "  u = (x - x0) / h"
            )
            x_points, y_points = input_xy(min_points=2)
            x = input_x_target()

            try:
                result, table = newton_forward(x_points, y_points, x, verbose=True)

                print("\n  Tabel Selisih Maju (Forward Difference Table):")
                print(table.to_string(index=False))
                print(f"\n  ✔ Hasil f({x}) = {result:.6f}")

                if tanya_tampilkan_grafik():
                    def func(xi):
                        return newton_forward(x_points, y_points, xi)[0]
                    plot_interpolation(x_points, y_points, func, "Newton Forward")

            except ValueError as e:
                print(f"  ✖ Error: {e}")

        # ── 5. Newton Backward ─────────────────────────────────────────────────
        elif choice == 5:
            cetak_info_metode(
                "Newton Backward (Interpolasi Selisih Mundur)",
                "Gunakan saat x yang dicari mendekati akhir data.\n"
                "  Syarat: jarak antar x harus sama (equal spacing).\n"
                "  u = (x - xn) / h"
            )
            x_points, y_points = input_xy(min_points=2)
            x = input_x_target()

            try:
                result = newton_backward(x_points, y_points, x, verbose=True)
                print(f"\n  ✔ Hasil f({x}) = {result:.6f}")

                if tanya_tampilkan_grafik():
                    def func(xi):
                        return newton_backward(x_points, y_points, xi)
                    plot_interpolation(x_points, y_points, func, "Newton Backward")

            except ValueError as e:
                print(f"  ✖ Error: {e}")

        # ── 6. Bandingkan semua metode ─────────────────────────────────────────
        elif choice == 6:
            print("\n── Bandingkan Semua Metode ──")
            print("  Perbandingan berguna untuk melihat seberapa dekat")
            print("  hasil tiap metode dan memilih yang paling akurat.\n")
            x_points, y_points = input_xy(min_points=2)
            x = input_x_target()

            print("\n" + "=" * 45)
            print("         HASIL PERBANDINGAN METODE")
            print("=" * 45)

            # Linear: polinom derajat 1 — hanya pakai 2 titik pertama
            if len(x_points) >= 2:
                try:
                    r = linear_interpolation(x_points[0], y_points[0], x_points[1], y_points[1], x)
                    print(f"  Linear            : {r:.6f}  (derajat 1, 2 titik)")
                except Exception as e:
                    print(f"  Linear            : gagal ({e})")
            else:
                print("  Linear            : butuh >= 2 titik")

            # Kuadratik: polinom derajat 2 — pakai 3 titik pertama
            if len(x_points) >= 3:
                try:
                    r, _ = quadratic_interpolation(x_points[:3], y_points[:3], x)
                    print(f"  Kuadratik         : {r:.6f}  (derajat 2, 3 titik)")
                except Exception as e:
                    print(f"  Kuadratik         : gagal ({e})")
            else:
                print("  Kuadratik         : butuh >= 3 titik")

            # Kubik: polinom derajat 3 — pakai 4 titik pertama
            if len(x_points) >= 4:
                try:
                    r = cubic_interpolation(x_points[:4], y_points[:4], x)
                    print(f"  Kubik             : {r:.6f}  (derajat 3, 4 titik)")
                except Exception as e:
                    print(f"  Kubik             : gagal ({e})")
            else:
                print("  Kubik             : butuh >= 4 titik")

            # Newton Forward: akurat untuk x mendekati awal data
            try:
                r, _ = newton_forward(x_points, y_points, x)
                print(f"  Newton Forward    : {r:.6f}  (x ≈ awal data)")
            except Exception as e:
                print(f"  Newton Forward    : tidak bisa ({e})")

            # Newton Backward: akurat untuk x mendekati akhir data
            try:
                r = newton_backward(x_points, y_points, x)
                print(f"  Newton Backward   : {r:.6f}  (x ≈ akhir data)")
            except Exception as e:
                print(f"  Newton Backward   : tidak bisa ({e})")

            print("=" * 45)

            if tanya_tampilkan_grafik():
                try:
                    def func(xi):
                        return newton_forward(x_points, y_points, xi)[0]
                    plot_interpolation(x_points, y_points, func, "Perbandingan (Newton Forward)")
                except Exception:
                    if len(x_points) >= 3:
                        def func(xi):
                            return quadratic_interpolation(x_points[:3], y_points[:3], xi)[0]
                        plot_interpolation(x_points, y_points, func, "Perbandingan (Kuadratik)")

        # ── 7. Input dari file CSV ─────────────────────────────────────────────
        elif choice == 7:
            print("\n── Input dari File CSV ──")
            print("  Format CSV: dua kolom bernama 'x' dan 'y'")
            filepath = input("  Path file CSV: ").strip()

            if not os.path.exists(filepath):
                print(f"  ✖ File tidak ditemukan: {filepath}")
                continue

            try:
                import pandas as pd
                df = pd.read_csv(filepath)

                if "x" not in df.columns or "y" not in df.columns:
                    print("  ✖ CSV harus punya kolom 'x' dan 'y'")
                    continue

                x_points = df["x"].tolist()
                y_points = df["y"].tolist()

                # Urutkan data dari CSV juga — file CSV tidak selalu terurut
                combined = sorted(zip(x_points, y_points))
                x_points, y_points = map(list, zip(*combined))

                print(f"\n  ✔ Loaded {len(x_points)} titik dari file (sudah diurutkan).")
                print(f"  x: {x_points}")
                print(f"  y: {y_points}")

                x = input_x_target()

                print("\n  Menjalankan semua metode dengan data file...")

                if len(x_points) >= 2:
                    try:
                        r = linear_interpolation(x_points[0], y_points[0], x_points[1], y_points[1], x)
                        print(f"  Linear            : {r:.6f}")
                    except Exception as e:
                        print(f"  Linear            : gagal ({e})")

                if len(x_points) >= 3:
                    try:
                        r, _ = quadratic_interpolation(x_points[:3], y_points[:3], x)
                        print(f"  Kuadratik         : {r:.6f}")
                    except Exception as e:
                        print(f"  Kuadratik         : gagal ({e})")

                if len(x_points) >= 4:
                    try:
                        r = cubic_interpolation(x_points[:4], y_points[:4], x)
                        print(f"  Kubik             : {r:.6f}")
                    except Exception as e:
                        print(f"  Kubik             : gagal ({e})")

                try:
                    r, _ = newton_forward(x_points, y_points, x)
                    print(f"  Newton Forward    : {r:.6f}")
                except Exception as e:
                    print(f"  Newton Forward    : tidak bisa ({e})")

                try:
                    r = newton_backward(x_points, y_points, x)
                    print(f"  Newton Backward   : {r:.6f}")
                except Exception as e:
                    print(f"  Newton Backward   : tidak bisa ({e})")

                if tanya_tampilkan_grafik():
                    try:
                        def func(xi):
                            return newton_forward(x_points, y_points, xi)[0]
                        plot_interpolation(x_points, y_points, func, f"Data dari {os.path.basename(filepath)}")
                    except Exception:
                        pass

            except ImportError:
                print("  ✖ pandas belum terinstall. Jalankan: pip install pandas")
            except Exception as e:
                print(f"  ✖ Gagal membaca file: {e}")

        # ── 8. Contoh Kasus Nyata ─────────────────────────────────────────────
        elif choice == 8:
            """
            Menu Kasus Nyata
            ─────────────────
            Interpolasi bukan sekadar latihan akademik. Berikut adalah kasus-kasus
            riil di mana interpolasi digunakan untuk membuat keputusan berdasarkan data.
            """
            print("\n── Contoh Kasus Nyata ──")
            print("  A. Prediksi Suhu Harian (Meteorologi)")
            print("  B. Prediksi Penjualan Bulanan (Bisnis)")
            print("  C. Kecepatan Benda Jatuh (Fisika / Mekanika)")
            print("  D. Kembali ke menu utama")
            print("-" * 45)

            sub = input("  Pilih kasus [A/B/C/D]: ").strip().upper()

            # ── Kasus A: Suhu Harian ──────────────────────────────────────────
            if sub == "A":
                """
                Kasus: Prediksi Suhu Harian
                ────────────────────────────
                Data suhu tercatat setiap hari (x = hari ke-n, y = suhu °C).
                Kita ingin memprediksi suhu pada hari yang tidak diukur, misalnya hari 2.5.

                Dalam meteorologi, data seperti ini diinterpolasi untuk mengisi
                gap pengukuran (misal sensor rusak di hari tertentu).

                Data: hasil observasi suhu di kota X selama 5 hari.
                Metode: Newton Forward — karena kita mencari nilai di awal/tengah data.
                """
                print("\n── Kasus A: Prediksi Suhu Harian ──")
                print("[Metode: Newton Forward]")
                print("  ℹ  Data suhu harian dicatat selama 5 hari.")
                print("  ℹ  Kita ingin memprediksi suhu pada hari ke-2.5 (siang hari).")

                # Data observasi suhu: hari (x) vs suhu °C (y)
                x_points = [1, 2, 3, 4, 5]       # hari ke-1 s/d ke-5
                y_points = [28.0, 30.5, 33.0, 31.5, 29.0]  # suhu dalam °C

                print(f"\n  Hari  : {x_points}")
                print(f"  Suhu  : {y_points} °C")

                x = input_x_target()

                try:
                    result, table = newton_forward(x_points, y_points, x, verbose=False)
                    print(f"\n  Tabel Selisih Maju:")
                    print(table.to_string(index=False))
                    print(f"\n  ✔ Prediksi suhu hari ke-{x} = {result:.2f}°C")
                    print(f"  (Rentang data: hari {min(x_points)} – {max(x_points)})")

                    if tanya_tampilkan_grafik():
                        def func(xi):
                            return newton_forward(x_points, y_points, xi)[0]
                        plot_interpolation(x_points, y_points, func, "Prediksi Suhu Harian (Newton Forward)")
                except ValueError as e:
                    print(f"  ✖ Error: {e}")

            # ── Kasus B: Penjualan Bulanan ────────────────────────────────────
            elif sub == "B":
                """
                Kasus: Prediksi Penjualan Bulanan
                ─────────────────────────────────
                Data penjualan produk (dalam juta rupiah) dicatat tiap bulan.
                Kita ingin memprediksi penjualan pada bulan yang datanya belum ada,
                misalnya bulan 5.5 (pertengahan antara Mei dan Juni).

                Dalam bisnis, ini digunakan untuk:
                  - Proyeksi stok barang
                  - Perencanaan anggaran
                  - Target penjualan tim

                Data: rekap penjualan 6 bulan pertama tahun ini.
                Metode: Newton Backward — kita mencari nilai di ujung akhir data.
                """
                print("\n── Kasus B: Prediksi Penjualan Bulanan ──")
                print("[Metode: Newton Backward]")
                print("  ℹ  Data penjualan (juta rupiah) tiap bulan selama 6 bulan.")
                print("  ℹ  Gunakan interpolasi untuk estimasi penjualan di antara bulan.")

                # Data penjualan: bulan (x) vs penjualan dalam juta rupiah (y)
                x_points = [1, 2, 3, 4, 5, 6]          # Januari s/d Juni
                y_points = [120.0, 135.0, 150.0, 162.0, 158.0, 175.0]  # juta rupiah

                bulan = ["", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun"]
                print(f"\n  {'Bulan':<8} {'Penjualan':>12}")
                print(f"  {'-'*22}")
                for i, (xv, yv) in enumerate(zip(x_points, y_points)):
                    print(f"  {bulan[int(xv)]:<8} {yv:>10.1f} jt")

                x = input_x_target()

                try:
                    result = newton_backward(x_points, y_points, x, verbose=False)
                    print(f"\n  ✔ Prediksi penjualan bulan ke-{x} = Rp {result:.2f} juta")
                    print(f"  (Rentang data: bulan {min(x_points)} – {max(x_points)})")

                    if tanya_tampilkan_grafik():
                        def func(xi):
                            return newton_backward(x_points, y_points, xi)
                        plot_interpolation(x_points, y_points, func, "Prediksi Penjualan Bulanan (Newton Backward)")
                except ValueError as e:
                    print(f"  ✖ Error: {e}")

            # ── Kasus C: Kecepatan Benda Jatuh ───────────────────────────────
            elif sub == "C":
                """
                Kasus: Kecepatan Benda Jatuh Bebas (dengan hambatan udara)
                ─────────────────────────────────────────────────────────
                Sebuah benda dijatuhkan dari ketinggian tertentu. Kecepatan dicatat
                pada beberapa waktu tertentu (dalam detik).

                Dalam fisika/mekanika, kita sering perlu interpolasi karena:
                  - Sensor hanya mencatat pada interval tertentu
                  - Kita butuh kecepatan di waktu yang tidak tercatat

                Data: pengukuran kecepatan (m/s) benda jatuh pada detik ke-0 s/d 4.
                Metode: Kubik — karena kurva kecepatan benda jatuh cenderung nonlinear
                         (pengaruh gravitasi + hambatan udara membentuk kurva derajat tinggi).
                """
                print("\n── Kasus C: Kecepatan Benda Jatuh Bebas ──")
                print("[Metode: Interpolasi Kubik]")
                print("  ℹ  Kecepatan benda jatuh diukur pada beberapa titik waktu.")
                print("  ℹ  Kurva kecepatan tidak linier (ada hambatan udara).")

                # Data fisika: waktu (detik) vs kecepatan (m/s)
                # Nilai realistis dengan hambatan udara (terminal velocity ~50 m/s)
                x_points = [0.0, 1.0, 2.0, 3.0]       # detik
                y_points = [0.0, 9.2, 17.5, 24.8]      # m/s

                print(f"\n  {'Waktu (s)':<12} {'Kecepatan (m/s)':>16}")
                print(f"  {'-'*30}")
                for xv, yv in zip(x_points, y_points):
                    print(f"  {xv:<12.1f} {yv:>16.2f}")

                x = input_x_target()

                try:
                    result = cubic_interpolation(x_points, y_points, x)
                    print(f"\n  ✔ Prediksi kecepatan pada t = {x} detik = {result:.4f} m/s")
                    print(f"  (Rentang data: t = {min(x_points)} s – {max(x_points)} s)")

                    if tanya_tampilkan_grafik():
                        def func(xi):
                            return cubic_interpolation(x_points, y_points, xi)
                        plot_interpolation(x_points, y_points, func, "Kecepatan Benda Jatuh (Kubik)")
                except ValueError as e:
                    print(f"  ✖ Error: {e}")

            elif sub == "D":
                continue
            else:
                print("  ✖ Pilihan tidak valid.")

        # ── 0. Keluar ──────────────────────────────────────────────────────────
        elif choice == 0:
            print("\n  Sampai jumpa!\n")
            break

        else:
            print("  ✖ Pilihan tidak valid.")


if __name__ == "__main__":
    main()