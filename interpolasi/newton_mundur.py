def newton_backward(x, y, xp, verbose=False):
    n = len(x)
    h = x[1] - x[0]

    # cek jarak sama
    for i in range(1, n - 1):
        if abs((x[i + 1] - x[i]) - h) > 1e-9:
            raise ValueError("x harus berjarak sama (equal spacing)")

    # buat tabel backward
    table = [y.copy()]
    for i in range(1, n):
        col = []
        for j in range(i, n):
            col.append(table[i - 1][j] - table[i - 1][j - 1])
        table.append(col)

    u = (xp - x[-1]) / h
    result = y[-1]
    u_term = 1
    fact = 1

    if verbose:
        print("\n" + "=" * 45)
        print("  LANGKAH PERHITUNGAN - Newton Backward")
        print("=" * 45)
        print(f"  h     = {h}")
        print(f"  u     = (x - xn) / h = ({xp} - {x[-1]}) / {h} = {u:.6f}")
        print(f"  yn    = {y[-1]}")
        print("-" * 45)

    for i in range(1, n):
        u_term *= (u + (i - 1))
        fact *= i
        delta = table[i][-1]
        contrib = (u_term * delta) / fact
        result += contrib

        if verbose:
            print(f"  Iterasi {i}:")
            print(f"    u_term = {u_term:.6f}")
            print(f"    ∇^{i}y  = {delta:.6f}")
            print(f"    {i}!    = {fact}")
            print(f"    Kontribusi = {contrib:.6f}")
            print(f"    Hasil sementara = {result:.6f}")
            print()

    if verbose:
        print("=" * 45)
        print(f"  HASIL AKHIR: {result:.6f}")
        print("=" * 45)

    return result