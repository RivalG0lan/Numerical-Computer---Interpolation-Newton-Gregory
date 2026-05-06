import pandas as pd

def forward_difference_table(x, y):
    n = len(y)
    table = [y.copy()]

    for i in range(1, n):
        col = []
        for j in range(n - i):
            col.append(table[i-1][j+1] - table[i-1][j])
        table.append(col)

    df = pd.DataFrame({f"Δ^{i}": col + [None]*(n-len(col)) for i, col in enumerate(table)})
    df.insert(0, "x", x)

    return df, table