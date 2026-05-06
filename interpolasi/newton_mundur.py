"""
interpolasi/newton_maju.py — Interpolasi Newton Forward (Selisih Maju)
=======================================================================
Mata Kuliah: Komputasi Numerik

Newton Forward Interpolation menggunakan tabel selisih maju (forward difference table)
untuk mengestimasi nilai fungsi. Metode ini cocok ketika titik x yang dicari
terletak di dekat awal data (x ≈ x0).

Rumus Newton-Gregory Forward:
    P(x) = y0 + u*Δy0 + [u(u-1)/2!]*Δ²y0 + [u(u-1)(u-2)/3!]*Δ³y0 + ...

di mana:
    u = (x - x0) / h         ← parameter tak-berdimensi
    h = jarak antar titik x  ← harus konstan (equal spacing)
    Δ^k y0 = selisih maju orde ke-k pada titik pertama

Tabel Selisih Maju:
    Δy_i   = y_{i+1} - y_i
    Δ²y_i  = Δy_{i+1} - Δy_i
    Δ³y_i  = Δ²y_{i+1} - Δ²y_i
    ... dst

Syarat: jarak antar x harus sama persis (equal spacing/equidistant nodes).

Keunggulan:
    - Efisien untuk data dengan jarak sama
    - Mudah diperluas ke orde lebih tinggi dengan menambah titik

Kelemahan:
    - Tidak bisa digunakan jika jarak x tidak sama
    - Akurasi turun jika x yang dicari jauh dari x0
"""

from utils.tabel_perbedaan import forward_difference_table


def newton_forward(x, y, xp, verbose=False):
    """
    Hitung nilai interpolasi Newton Forward P(xp).

    Parameter:
        x       : list of float — titik-titik x yang diketahui (harus equal spacing)
        y       : list of float — nilai fungsi di titik-titik x
        xp      : float — nilai x yang ingin dicari P(xp)-nya
        verbose : bool — jika True, cetak langkah perhitungan detail

    Return:
        (result, df) — nilai P(xp) dan DataFrame tabel selisih maju

    Raises:
        ValueError — jika jarak antar x tidak sama
    """
    n = len(x)

    # ── Validasi Equal Spacing ───────────────────────────────────────────────
    # Newton Forward hanya valid jika semua jarak h = x_{i+1} - x_i sama.
    # Toleransi 1e-9 untuk mengatasi floating-point rounding error.
    h = x[1] - x[0]
    for i in range(1, n - 1):
        if abs((x[i + 1] - x[i]) - h) > 1e-9:
            raise ValueError("x harus berjarak sama (equal spacing)")

    # ── Bangun Tabel Selisih Maju ────────────────────────────────────────────
    # Tabel ini berisi kolom Δ^0, Δ^1, Δ^2, ..., Δ^(n-1)
    # Kolom Δ^0 = y itu sendiri
    df, table = forward_difference_table(x, y)

    # ── Hitung Parameter u ───────────────────────────────────────────────────
    # u adalah "posisi relatif" xp terhadap x0, diskalakan dengan h
    # u = 0 berarti xp tepat di x0; u = 1 berarti xp di x1; dst.
    u = (xp - x[0]) / h

    # ── Evaluasi Polinom Newton Forward ─────────────────────────────────────
    result = y[0]          # suku pertama: y0
    u_term = 1             # akumulator produk: u * (u-1) * (u-2) * ...
    fact = 1               # akumulator faktorial: k!

    if verbose:
        print("\n" + "=" * 45)
        print("  LANGKAH PERHITUNGAN - Newton Forward")
        print("=" * 45)
        print(f"  h     = {h}  ← jarak antar titik x")
        print(f"  u     = (x - x0) / h = ({xp} - {x[0]}) / {h} = {u:.6f}")
        print(f"  y0    = {y[0]}  ← nilai awal f(x0)")
        print("-" * 45)

    for i in range(1, n):
        # Suku ke-i dari polinom Newton Forward:
        # u * (u-1) * ... * (u-(i-1)) / i! * Δ^i y0

        # Update u_term: kalikan dengan (u - (i-1))
        u_term *= (u - (i - 1))

        # Update faktorial: i!
        fact *= i

        # Ambil Δ^i y0 dari kolom ke-i tabel selisih maju (baris pertama = indeks 0)
        delta = table[i][0]

        # Kontribusi suku ke-i ke hasil interpolasi
        contrib = (u_term * delta) / fact
        result += contrib

        if verbose:
            print(f"  Iterasi {i}:")
            print(f"    u_term  = {u_term:.6f}  ← u(u-1)...(u-{i-1})")
            print(f"    Δ^{i}y0  = {delta:.6f}  ← dari tabel selisih maju")
            print(f"    {i}!      = {fact}")
            print(f"    Kontribusi = {contrib:.6f}")
            print(f"    Akumulasi  = {result:.6f}")
            print()

    if verbose:
        print("=" * 45)
        print(f"  HASIL AKHIR: P({xp}) = {result:.6f}")
        print("=" * 45)

    return result, df