"""
interpolasi/newton_mundur.py — Interpolasi Newton Backward (Selisih Mundur)
============================================================================
Mata Kuliah: Komputasi Numerik

Newton Backward Interpolation menggunakan tabel selisih mundur (backward difference table).
Metode ini cocok ketika titik x yang dicari terletak di dekat AKHIR data (x ≈ xn).

Rumus Newton-Gregory Backward:
    P(x) = yn + u*∇yn + [u(u+1)/2!]*∇²yn + [u(u+1)(u+2)/3!]*∇³yn + ...

di mana:
    u  = (x - xn) / h        ← bernilai negatif jika x < xn
    h  = jarak antar titik x ← harus konstan (equal spacing)
    ∇^k yn = selisih mundur orde ke-k pada titik TERAKHIR

Tabel Selisih Mundur:
    ∇y_i  = y_i - y_{i-1}
    ∇²y_i = ∇y_i - ∇y_{i-1}
    ... dst

Perbedaan dengan Newton Forward:
    Forward  → pakai Δ (selisih maju), ambil elemen PERTAMA tiap orde
    Backward → pakai ∇ (selisih mundur), ambil elemen TERAKHIR tiap orde
"""


def newton_backward(x, y, xp, verbose=False):
    """
    Hitung nilai interpolasi Newton Backward P(xp).

    Parameter:
        x       : list of float — titik-titik x (harus equal spacing, sudah terurut)
        y       : list of float — nilai fungsi di titik-titik x
        xp      : float — nilai x yang ingin dicari P(xp)-nya
        verbose : bool — jika True, cetak langkah perhitungan detail

    Return:
        float — nilai P(xp)

    Raises:
        ValueError — jika jarak antar x tidak sama
    """
    n = len(x)

    # ── Validasi Equal Spacing ───────────────────────────────────────────────
    # Toleransi 1e-9 untuk menangani floating-point rounding error.
    h = x[1] - x[0]
    for i in range(1, n - 1):
        if abs((x[i + 1] - x[i]) - h) > 1e-9:
            raise ValueError("x harus berjarak sama (equal spacing)")

    # ── Bangun Tabel Selisih Mundur ──────────────────────────────────────────
    # table[0] = salinan y asli (orde 0)
    # table[k] = list selisih mundur orde ke-k, panjang = n - k
    #
    # Rumus: ∇^k y[j] = ∇^(k-1) y[j] - ∇^(k-1) y[j-1]
    # j berjalan dari 1 s/d len(prev)-1 (butuh elemen j dan j-1).
    #
    # Contoh untuk n=3, y=[6,5,4]:
    #   table[0] = [6, 5, 4]
    #   table[1] = [5-6, 4-5] = [-1, -1]
    #   table[2] = [-1-(-1)]  = [0]

    table = [list(y)]
    for k in range(1, n):
        prev = table[k - 1]
        col  = [prev[j] - prev[j - 1] for j in range(1, len(prev))]
        table.append(col)

    # ── Hitung Parameter u ───────────────────────────────────────────────────
    # u diukur dari titik TERAKHIR (xn).
    # u negatif jika xp berada sebelum xn.
    u = (xp - x[-1]) / h

    # ── Evaluasi Polinom Newton Backward ─────────────────────────────────────
    result = y[-1]   # mulai dari yn
    u_term = 1       # akumulator produk u*(u+1)*(u+2)*...
    fact   = 1       # akumulator faktorial k!

    if verbose:
        print("\n" + "=" * 45)
        print("  LANGKAH PERHITUNGAN - Newton Backward")
        print("=" * 45)
        print(f"  h     = {h}  <- jarak antar titik x")
        print(f"  u     = (xp - xn) / h = ({xp} - {x[-1]}) / {h} = {u:.6f}")
        print(f"  yn    = {y[-1]}  <- nilai f(xn)")
        print("-" * 45)

    for k in range(1, n):
        # Suku ke-k: [u(u+1)...(u+k-1) / k!] * nabla^k yn
        # Tanda PLUS pada (u + k - 1) — berbeda dari Forward yang MINUS

        u_term *= (u + (k - 1))
        fact   *= k

        # nabla^k yn = elemen TERAKHIR dari table[k]
        delta   = table[k][-1]
        contrib = (u_term * delta) / fact
        result += contrib

        if verbose:
            print(f"  Iterasi {k}:")
            print(f"    u_term     = {u_term:.6f}")
            print(f"    nabla^{k}yn = {delta:.6f}")
            print(f"    {k}!         = {fact}")
            print(f"    Kontribusi = {contrib:.6f}")
            print(f"    Akumulasi  = {result:.6f}")
            print()

    if verbose:
        print("=" * 45)
        print(f"  HASIL AKHIR: P({xp}) = {result:.6f}")
        print("=" * 45)

    return result