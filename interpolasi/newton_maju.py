from utils.tabel_perbedaan import forward_difference_table

def newton_forward(x, y, xp, verbose=False):
    n = len(x)
    h = x[1] - x[0]

    # cek jarak sama
    for i in range(1, n - 1):
        if abs((x[i + 1] - x[i]) - h) > 1e-9:
            raise ValueError("x harus berjarak sama (equal spacing)")

    df, table = forward_difference_table(x, y)

    u = (xp - x[0]) / h
    result = y[0]
    u_term = 1
    fact = 1

    if verbose:
        print("\n" + "=" * 45)
        print("  LANGKAH PERHITUNGAN - Newton Forward")
        print("=" * 45)
        print(f"  h     = {h}")
        print(f"  u     = (x - x0) / h = ({xp} - {x[0]}) / {h} = {u:.6f}")
        print(f"  y0    = {y[0]}")
        print("-" * 45)

    for i in range(1, n):
        u_term *= (u - (i - 1))
        fact *= i
        delta = table[i][0]
        contrib = (u_term * delta) / fact
        result += contrib

        if verbose:
            print(f"  Iterasi {i}:")
            print(f"    u_term = {u_term:.6f}")
            print(f"    Δ^{i}y  = {delta:.6f}")
            print(f"    {i}!    = {fact}")
            print(f"    Kontribusi = {contrib:.6f}")
            print(f"    Hasil sementara = {result:.6f}")
            print()

    if verbose:
        print("=" * 45)
        print(f"  HASIL AKHIR: {result:.6f}")
        print("=" * 45)

    return result, df