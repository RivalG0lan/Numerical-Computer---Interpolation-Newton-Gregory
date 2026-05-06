"""
interpolasi/linear.py — Interpolasi Linear
============================================
Mata Kuliah: Komputasi Numerik

Interpolasi linear adalah metode paling sederhana untuk mengestimasi nilai f(x)
di antara dua titik yang diketahui. Prinsipnya: tarik garis lurus antara (x0, y0)
dan (x1, y1), lalu ambil nilai y pada titik x yang ditanyakan.

Rumus:
    f(x) = y0 + [(x - x0) / (x1 - x0)] * (y1 - y0)

Atau dalam bentuk Lagrange:
    f(x) = y0 * L0(x) + y1 * L1(x)
    di mana:
        L0(x) = (x - x1) / (x0 - x1)
        L1(x) = (x - x0) / (x1 - x0)

Keunggulan:
    - Sederhana dan cepat
    - Cocok untuk data yang berubah hampir linear

Kelemahan:
    - Tidak akurat untuk fungsi nonlinear
    - Hanya menggunakan 2 titik data
"""


def linear_interpolation(x0, y0, x1, y1, x):
    """
    Hitung nilai interpolasi linear f(x) menggunakan dua titik (x0,y0) dan (x1,y1).

    Parameter:
        x0, y0 : float — titik pertama
        x1, y1 : float — titik kedua
        x      : float — nilai x yang ingin dicari f(x)-nya

    Return:
        float — nilai estimasi f(x)

    Raises:
        ValueError — jika x0 == x1 (kedua titik berimpit, pembagian nol)

    Contoh:
        >>> linear_interpolation(1, 10, 3, 30, 2)
        20.0
    """
    # Cek: x0 dan x1 tidak boleh sama, karena kita akan membagi dengan (x1 - x0)
    # Jika sama, fungsi tidak terdefinisi (gradient tak hingga)
    if x1 == x0:
        raise ValueError("x0 dan x1 tidak boleh sama (pembagian oleh nol)")

    # Rumus interpolasi linear:
    # y = y0 + (slope) * (x - x0)
    # di mana slope = (y1 - y0) / (x1 - x0)
    y = y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)

    return y