"""
utils/plot.py — Visualisasi Grafik Interpolasi
================================================
Mata Kuliah: Komputasi Numerik

Modul ini menyediakan fungsi untuk memvisualisasikan hasil interpolasi
menggunakan matplotlib. Grafik membantu kita melihat:
  - Seberapa mulus kurva interpolasi melewati titik-titik data
  - Apakah ada osilasi berlebihan (Runge's phenomenon) di luar rentang data
  - Perbandingan visual antar metode interpolasi
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_interpolation(x_points, y_points, func, title="Interpolasi"):
    """
    Tampilkan grafik hasil interpolasi beserta titik-titik data asli.

    Parameter:
        x_points : list of float — titik-titik x data asli
        y_points : list of float — titik-titik y data asli
        func     : callable — fungsi interpolasi f(x) yang sudah dibentuk
        title    : str — judul grafik

    Cara kerja:
        1. Buat 300 titik x rapat di antara min dan max data (np.linspace)
        2. Evaluasi func(x) di setiap titik → kurva halus
        3. Plot kurva + titik data asli
    """

    # Buat rentang x yang rapat untuk menggambar kurva halus.
    # np.linspace membagi interval [min, max] menjadi 300 titik sama jarak.
    # Semakin banyak titik → kurva semakin halus (tidak patah-patah).
    x_range = np.linspace(min(x_points), max(x_points), 300)

    # Evaluasi fungsi interpolasi di setiap titik x_range.
    # Hasilnya adalah kurva kontinu hasil interpolasi.
    y_range = []
    for xi in x_range:
        try:
            y_range.append(func(xi))
        except Exception:
            y_range.append(float('nan'))  # skip titik yang error (misal di luar domain)

    # ── Plot ─────────────────────────────────────────────────────────────────

    plt.figure(figsize=(8, 5))

    # Kurva interpolasi — garis biru kontinu
    plt.plot(x_range, y_range, color='steelblue', linewidth=2, label='Kurva Interpolasi')

    # Titik data asli — scatter merah agar mudah dibedakan dari kurva
    plt.scatter(x_points, y_points, color='crimson', zorder=5,
                s=80, label='Titik Data Asli')

    # Beri label pada setiap titik data (x, y)
    for xi, yi in zip(x_points, y_points):
        plt.annotate(f'({xi}, {yi})', xy=(xi, yi),
                     xytext=(5, 8), textcoords='offset points',
                     fontsize=8, color='darkred')

    plt.title(title, fontsize=13, fontweight='bold')
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()