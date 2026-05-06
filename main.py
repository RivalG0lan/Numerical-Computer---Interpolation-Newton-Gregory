from interpolasi.linear import linear_interpolation
from interpolasi.kuadratik import quadratic_interpolation
from interpolasi.kubik import cubic_interpolation
from interpolasi.newton_maju import newton_forward
from interpolasi.newton_mundur import newton_backward
from utils.plot import plot_interpolation

def main():
    print("=== PROGRAM INTERPOLASI ===")
    print("1. Linear")
    print("2. Kuadratik")
    print("3. Kubik")
    print("4. Newton Forward")
    print("5. Newton Backward")

    choice = int(input("Pilih metode: "))

    if choice == 1:
        x0 = float(input("x0: "))
        y0 = float(input("y0: "))
        x1 = float(input("x1: "))
        y1 = float(input("y1: "))
        x = float(input("x yang dicari: "))

        print("Hasil:", linear_interpolation(x0, y0, x1, y1, x))

    elif choice == 2:
        x_points = list(map(float, input("Masukkan 3 x: ").split()))
        y_points = list(map(float, input("Masukkan 3 y: ").split()))
        x = float(input("x yang dicari: "))

        result, coef = quadratic_interpolation(x_points, y_points, x)
        print("Hasil:", result)
        print("Koefisien:", coef)

    elif choice == 3:
        x_points = list(map(float, input("Masukkan 4 x: ").split()))
        y_points = list(map(float, input("Masukkan 4 y: ").split()))
        x = float(input("x yang dicari: "))

        print("Hasil:", cubic_interpolation(x_points, y_points, x))

    elif choice == 4:
        x_points = list(map(float, input("Masukkan x: ").split()))
        y_points = list(map(float, input("Masukkan y: ").split()))
        x = float(input("x yang dicari: "))

        result, table = newton_forward(x_points, y_points, x)
        print("Hasil:", result)
        print("\nTabel Selisih:")
        print(table)

    elif choice == 5:
        x_points = list(map(float, input("Masukkan x: ").split()))
        y_points = list(map(float, input("Masukkan y: ").split()))
        x = float(input("x yang dicari: "))

        print("Hasil:", newton_backward(x_points, y_points, x))

if __name__ == "__main__":
    main()