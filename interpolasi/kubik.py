"""
interpolasi/kubik.py — Interpolasi Kubik
=========================================
Mata Kuliah: Komputasi Numerik

Interpolasi kubik menggunakan polinom derajat 3 yang melewati tepat 4 titik data.
Dengan 4 titik, kita dapat menentukan secara unik polinom berderajat 3:
    P(x) = a3*x³ + a2*x² + a1*x + a0

Metode yang digunakan: Newton's Divided Differences
──────────────────────────────────────────────────
Polinom Newton orde-3:
    P(x) = b0
         + b1*(x - x0)
         + b2*(x - x0)*(x - x1)
         + b3*(x - x0)*(x - x1)*(x - x2)

Tabel divided differences untuk 4 titik:
    orde 0: f[x0], f[x1], f[x2], f[x3]
    orde 1: f[x0,x1], f[x1,x2], f[x2,x3]
    orde 2: f[x0,x1,x2], f[x1,x2,x3]
    orde 3: f[x0,x1,x2,x3]  ← ini b3

Keunggulan:
    - Akurasi lebih tinggi dari kuadratik untuk fungsi melengkung
    - Cukup fleksibel untuk menangkap S-curve atau inflection point

Kelemahan:
    - Runge's phenomenon: polinom derajat tinggi bisa berosilasi
      di luar rentang data (extrapolation)
"""


def cubic_interpolation(x_points, y_points, x):
    """
    Hitung nilai interpolasi kubik P(x) menggunakan 4 titik data.

    Parameter:
        x_points : list of float — [x0, x1, x2, x3]
        y_points : list of float — [y0, y1, y2, y3]
        x        : float — nilai x yang ingin dicari P(x)-nya

    Return:
        float — nilai P(x)

    Raises:
        ValueError — jika jumlah titik bukan 4
    """
    if len(x_points) != 4:
        raise ValueError("Butuh tepat 4 titik untuk interpolasi kubik")

    x0, x1, x2, x3 = x_points
    y0, y1, y2, y3 = y_points

    # ── Hitung Divided Differences secara bertahap ───────────────────────────

    # b0: orde 0 — nilai fungsi di x0
    b0 = y0

    # b1: orde 1 — f[x0, x1]
    b1 = (y1 - y0) / (x1 - x0)

    # Selisih terbagi orde 1 antara pasangan lain (untuk menghitung orde 2)
    f01 = b1                              # f[x0, x1]
    f12 = (y2 - y1) / (x2 - x1)          # f[x1, x2]
    f23 = (y3 - y2) / (x3 - x2)          # f[x2, x3]

    # b2: orde 2 — f[x0, x1, x2]
    # Dihitung dari selisih dua orde-1 dibagi jarak x terluar
    b2 = (f12 - f01) / (x2 - x0)

    # Selisih orde 2 lainnya (untuk menghitung orde 3)
    f012 = b2                             # f[x0, x1, x2]
    f123 = (f23 - f12) / (x3 - x1)       # f[x1, x2, x3]

    # b3: orde 3 — f[x0, x1, x2, x3]
    # Koefisien kubik terakhir
    b3 = (f123 - f012) / (x3 - x0)

    # ── Evaluasi Polinom Newton ──────────────────────────────────────────────
    # P(x) = b0 + b1*(x-x0) + b2*(x-x0)*(x-x1) + b3*(x-x0)*(x-x1)*(x-x2)
    y = (
        b0
        + b1 * (x - x0)
        + b2 * (x - x0) * (x - x1)
        + b3 * (x - x0) * (x - x1) * (x - x2)
    )

    return y