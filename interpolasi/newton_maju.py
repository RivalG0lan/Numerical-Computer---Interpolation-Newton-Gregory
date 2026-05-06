from utils.tabel_perbedaan import forward_difference_table

def newton_forward(x, y, xp):
    n = len(x)
    h = x[1] - x[0]

    # cek jarak sama
    for i in range(1, n-1):
        if (x[i+1] - x[i]) != h:
            raise ValueError("x harus berjarak sama")

    df, table = forward_difference_table(x, y)

    u = (xp - x[0]) / h
    result = y[0]

    u_term = 1
    fact = 1

    for i in range(1, n):
        u_term *= (u - (i - 1))
        fact *= i
        result += (u_term * table[i][0]) / fact

    return result, df