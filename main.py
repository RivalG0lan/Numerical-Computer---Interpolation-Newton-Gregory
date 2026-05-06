import os
from interpolasi.linear import linear_interpolation
from interpolasi.kuadratik import quadratic_interpolation
from interpolasi.kubik import cubic_interpolation
from interpolasi.newton_maju import newton_forward
from interpolasi.newton_mundur import newton_backward
from utils.plot import plot_interpolation


# ── helpers ────────────────────────────────────────────────────────────────────

def input_xy(min_points=None, exact=None):
    """Minta input x dan y dari user dengan validasi."""
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

            return x_points, y_points
        except ValueError:
            print("  ✖ Input tidak valid, coba lagi.\n")


def input_x_target():
    while True:
        try:
            return float(input("Masukkan x yang dicari: "))
        except ValueError:
            print("  ✖ Input tidak valid.\n")


def tanya_tampilkan_grafik():
    ans = input("Tampilkan grafik? (y/n): ").strip().lower()
    return ans == "y"


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
        print("  0. Keluar")
        print("-" * 45)

        try:
            choice = int(input("  Pilih metode [0-7]: "))
        except ValueError:
            print("  ✖ Masukkan angka!")
            continue

        # ── 1. Linear ──────────────────────────────────────────────────────────
        if choice == 1:
            print("\n── Interpolasi Linear ──")
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
            print("\n── Interpolasi Kuadratik (butuh 3 titik) ──")
            x_points, y_points = input_xy(exact=3)
            x = input_x_target()

            try:
                result, coef = quadratic_interpolation(x_points, y_points, x)
                b0, b1, b2 = coef
                print(f"\n  Koefisien:")
                print(f"    b0 = {b0:.6f}")
                print(f"    b1 = {b1:.6f}")
                print(f"    b2 = {b2:.6f}")
                print(f"\n  ✔ Hasil f({x}) = {result:.6f}")

                if tanya_tampilkan_grafik():
                    def func(xi):
                        return quadratic_interpolation(x_points, y_points, xi)[0]
                    plot_interpolation(x_points, y_points, func, "Interpolasi Kuadratik")

            except ValueError as e:
                print(f"  ✖ Error: {e}")

        # ── 3. Kubik ───────────────────────────────────────────────────────────
        elif choice == 3:
            print("\n── Interpolasi Kubik (butuh 4 titik) ──")
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
            print("\n── Newton Forward (x harus berjarak sama) ──")
            x_points, y_points = input_xy(min_points=2)
            x = input_x_target()

            try:
                result, table = newton_forward(x_points, y_points, x, verbose=True)

                print("\n  Tabel Selisih Maju:")
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
            print("\n── Newton Backward (x harus berjarak sama) ──")
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
            x_points, y_points = input_xy(min_points=2)
            x = input_x_target()

            print("\n" + "=" * 45)
            print("         HASIL PERBANDINGAN METODE")
            print("=" * 45)

            # Linear (gunakan 2 titik pertama)
            if len(x_points) >= 2:
                try:
                    r = linear_interpolation(x_points[0], y_points[0], x_points[1], y_points[1], x)
                    print(f"  Linear            : {r:.6f}")
                except Exception as e:
                    print(f"  Linear            : gagal ({e})")
            else:
                print("  Linear            : butuh >= 2 titik")

            # Kuadratik (gunakan 3 titik pertama)
            if len(x_points) >= 3:
                try:
                    r, _ = quadratic_interpolation(x_points[:3], y_points[:3], x)
                    print(f"  Kuadratik         : {r:.6f}")
                except Exception as e:
                    print(f"  Kuadratik         : gagal ({e})")
            else:
                print("  Kuadratik         : butuh >= 3 titik")

            # Kubik (gunakan 4 titik pertama)
            if len(x_points) >= 4:
                try:
                    r = cubic_interpolation(x_points[:4], y_points[:4], x)
                    print(f"  Kubik             : {r:.6f}")
                except Exception as e:
                    print(f"  Kubik             : gagal ({e})")
            else:
                print("  Kubik             : butuh >= 4 titik")

            # Newton Forward
            try:
                r, _ = newton_forward(x_points, y_points, x)
                print(f"  Newton Forward    : {r:.6f}")
            except Exception as e:
                print(f"  Newton Forward    : tidak bisa ({e})")

            # Newton Backward
            try:
                r = newton_backward(x_points, y_points, x)
                print(f"  Newton Backward   : {r:.6f}")
            except Exception as e:
                print(f"  Newton Backward   : tidak bisa ({e})")

            print("=" * 45)

            # Grafik: pakai Newton Forward kalau bisa, fallback Kuadratik
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
                print(f"\n  ✔ Loaded {len(x_points)} titik dari file.")
                print(f"  x: {x_points}")
                print(f"  y: {y_points}")

                x = input_x_target()

                # Langsung jalankan perbandingan
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

        # ── 0. Keluar ──────────────────────────────────────────────────────────
        elif choice == 0:
            print("\n  Sampai jumpa!\n")
            break

        else:
            print("  ✖ Pilihan tidak valid.")


if __name__ == "__main__":
    main()