def newton_backward(x, y, xp):
    n = len(x)
    h = x[1] - x[0]

    # cek jarak sama
    for i in range(1, n-1):
        if (x[i+1] - x[i]) != h:
            raise ValueError("x harus berjarak sama")

    # buat tabel backward
    table = [y.copy()]
    for i in range(1, n):
        col = []
        for j in range(i, n):
            col.append(table[i-1][j] - table[i-1][j-1])
        table.append(col)

    u = (xp - x[-1]) / h
    result = y[-1]

    u_term = 1
    fact = 1

    for i in range(1, n):
        u_term *= (u + (i - 1))
        fact *= i
        result += (u_term * table[i][-1]) / fact

    return result