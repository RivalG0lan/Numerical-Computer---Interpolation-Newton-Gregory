"""
interpolasi/kuadratik.py — Interpolasi Kuadratik
==================================================
Mata Kuliah: Komputasi Numerik

Interpolasi kuadratik menggunakan polinom derajat 2 (parabola) yang melewati
tepat 3 titik data yang diberikan.

Metode yang digunakan: Newton's Divided Differences
──────────────────────────────────────────────────
Polinom Newton orde-2:
    P(x) = b0 + b1*(x - x0) + b2*(x - x0)*(x - x1)

Koefisien (divided differences):
    b0 = f[x0]          = y0
    b1 = f[x0, x1]      = (y1 - y0) / (x1 - x0)
    b2 = f[x0, x1, x2]  = (f[x1,x2] - f[x0,x1]) / (x2 - x0)

Keunggulan dibanding linear:
    - Dapat menangkap kurva (non-linearitas sederhana)
    - Masih relatif efisien secara komputasi

Kelemahan:
    - Hanya akurat jika fungsi mendekati parabola
    - Sensitif terhadap posisi titik data
"""


def quadratic_interpolation(x_points, y_points, x):
    """
    Hitung nilai interpolasi kuadratik P(x) menggunakan 3 titik data.

    Parameter:
        x_points : list of float — [x0, x1, x2], titik-titik x yang diketahui
        y_points : list of float — [y0, y1, y2], nilai fungsi di titik tersebut
        x        : float — nilai x yang ingin dicari P(x)-nya

    Return:
        (result, (b0, b1, b2)) — nilai P(x) dan koefisien divided differences

    Raises:
        ValueError — jika jumlah titik bukan 3
    """
    if len(x_points) != 3:
        raise ValueError("Butuh tepat 3 titik untuk interpolasi kuadratik")

    x0, x1, x2 = x_points
    y0, y1, y2 = y_points

    # ── Hitung Divided Differences ──────────────────────────────────────────
    # b0 = f[x0]: nilai fungsi di x0 (orde 0)
    b0 = y0

    # b1 = f[x0, x1]: selisih terbagi orde pertama
    # Mengukur "slope rata-rata" antara x0 dan x1
    b1 = (y1 - y0) / (x1 - x0)

    # Selisih terbagi orde pertama antara x1 dan x2
    f_x1_x2 = (y2 - y1) / (x2 - x1)

    # b2 = f[x0, x1, x2]: selisih terbagi orde kedua
    # Mengukur "kelengkungan" rata-rata polinom
    b2 = (f_x1_x2 - b1) / (x2 - x0)

    # ── Evaluasi Polinom Newton ──────────────────────────────────────────────
    # P(x) = b0 + b1*(x-x0) + b2*(x-x0)*(x-x1)
    # Ini adalah bentuk bersarang (nested form / Horner's form orde 2)
    y = b0 + b1 * (x - x0) + b2 * (x - x0) * (x - x1)

    return y, (b0, b1, b2)