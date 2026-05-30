# Numerical Computing - Interpolation and Newton Gregory

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue" alt="Python">
  <img src="https://img.shields.io/badge/NumPy-Numerical%20Computing-orange" alt="NumPy">
  <img src="https://img.shields.io/badge/Pandas-Data%20Processing-green" alt="Pandas">
  <img src="https://img.shields.io/badge/Matplotlib-Visualization-red" alt="Matplotlib">
  <img src="https://img.shields.io/badge/Course-Numerical%20Computing-lightgrey" alt="Course">
</p>

## Overview

This repository contains a Python-based Numerical Interpolation application developed as part of the Numerical Computing course.

The project implements several interpolation techniques used to estimate unknown function values from known data points. In addition to performing interpolation calculations, the application provides graphical visualization, CSV file support, method comparison utilities, and real-world case studies to help students understand both the mathematical concepts and practical applications of interpolation.

---

## Table of Contents

* Overview
* Features
* Implemented Methods
* Project Structure
* Installation
* Running the Program
* CSV File Format
* Example Usage
* Data Validation
* Visualization
* Learning Objectives
* Technologies Used
* Future Improvements
* Authors
* License

---

## Features

| Feature                 | Description                                |
| ----------------------- | ------------------------------------------ |
| Linear Interpolation    | Estimate values using two known points     |
| Quadratic Interpolation | Polynomial interpolation of degree 2       |
| Cubic Interpolation     | Polynomial interpolation of degree 3       |
| Newton Forward          | Forward Difference Interpolation           |
| Newton Backward         | Backward Difference Interpolation          |
| Method Comparison       | Compare results from all available methods |
| Graph Visualization     | Plot interpolation curves and data points  |
| CSV Import              | Load datasets directly from CSV files      |
| Automatic Validation    | Validate input before computation          |
| Automatic Sorting       | Sort data points by x values               |
| Real-World Examples     | Temperature, Sales, and Physics datasets   |

---

## Implemented Methods

### Linear Interpolation

Uses two data points to construct a straight line and estimate intermediate values.

### Quadratic Interpolation

Uses three data points to construct a second-degree polynomial capable of representing simple curves.

### Cubic Interpolation

Uses four data points to construct a third-degree polynomial that can model more complex behavior.

### Newton Forward Interpolation

Uses a Forward Difference Table and is most suitable when the target value is located near the beginning of the dataset.

### Newton Backward Interpolation

Uses a Backward Difference Table and is most suitable when the target value is located near the end of the dataset.

---

## Project Structure

```text
.
├── main.py
├── interpolasi
│   ├── linear.py
│   ├── kuadratik.py
│   ├── kubik.py
│   ├── newton_maju.py
│   └── newton_mundur.py
├── utils
│   ├── plot.py
│   └── tabel_perbedaan.py
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/username/Numerical-Computer---Interpolation-Newton-Gregory.git
cd Numerical-Computer---Interpolation-Newton-Gregory
```

Install required dependencies:

```bash
pip install numpy pandas matplotlib
```

---

## Running the Program

Execute the main application:

```bash
python main.py
```

---

## CSV File Format

The program supports importing datasets from CSV files.

Example:

```csv
x,y
1,10
2,15
3,22
4,30
5,40
```

Required columns:

| Column | Description          |
| ------ | -------------------- |
| x      | Independent variable |
| y      | Function value       |

---

## Example Usage

Input Data:

```text
x = [1, 2, 3]
y = [2, 4, 8]
```

Target Value:

```text
x = 2.5
```

The program will compute the interpolated value using the selected method and optionally display the interpolation graph.

---

## Data Validation

Before performing calculations, the program validates:

* The number of x and y values must match
* Duplicate x values are not allowed
* Data points are automatically sorted
* Newton methods require equal spacing between x values

---

## Visualization

The application uses Matplotlib to generate graphical representations of interpolation results.

Visualization capabilities include:

* Plotting interpolation curves
* Displaying original data points
* Comparing interpolation behavior
* Supporting numerical analysis and interpretation

---

## Learning Objectives

This project was developed to:

* Understand numerical interpolation concepts
* Implement interpolation algorithms manually
* Study Newton Divided Differences
* Study Forward and Backward Difference Tables
* Practice numerical computing with Python
* Explore data visualization techniques
* Apply interpolation to practical case studies

---

## Technologies Used

| Technology | Purpose                          |
| ---------- | -------------------------------- |
| Python 3   | Main programming language        |
| NumPy      | Numerical operations             |
| Pandas     | Data processing and CSV handling |
| Matplotlib | Graph plotting and visualization |

---

## Future Improvements

Possible future enhancements include:

* Lagrange Interpolation
* Newton Divided Difference Table Visualization
* Spline Interpolation
* Export results to CSV or PDF
* Graphical User Interface (GUI)
* Error analysis and accuracy comparison

---

## Authors

Developed as a Numerical Computing course project.

Team Members:
* 241712003 - Sultan tri Ananda (Coders)
* 241712006 - Parida Lubis
* 241712009 - Maulia Revani Putri
* 241712012 - Ruth Angelia sihombing
* 241712015 - Auzan Taris
* 241712018 - Dimas Surya darma
* 241712021 - Ivana kristina
* 241712024 - Adeptri sagala
* 241712027 - M. Fikri ramadhan Sembiring (Coders)
* 241712030 - Habil Rizky Tazir
* 241712034 - Muhammad Ramadhan
* 241712037 - Syaikhah Az-Zahra Nasir
* 241712040 - Nadya putri Anggina siregar
* 241712043 - Rivaldo Nainggolan (Coders)

---

## License

This project is intended for educational and academic purposes.

Feel free to use, modify, and extend the source code for learning and research activities.
