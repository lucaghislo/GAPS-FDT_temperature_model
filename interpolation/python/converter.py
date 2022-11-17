import math
from cmath import cosh

import numpy as np
import sympy as sy
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from mpmath import *

# curve_fit() function imported from scipy
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# Fattore di conversione DAC_inj_code to keV
coeff_DAC_inj_kev = 0.841


def gaps_fdt_tanh(k, m1, m2, m3, m4, m5, m6, m7, m8, m9):
    output = []
    for i in k:
        val = 0.5 * (
            m1 * (i + m5) + m2 * log(cosh(m3 * ((i + m5) - m4)) / cosh(m3 * m4))
        ) + m6 * log(cosh(m7 * ((i - abs(m8)) - m9)) / cosh(m7 * m9))

        output.append(float(val))

    return output


# open file in read mode
coeffs = []
with open("results_weights.txt", "r") as fp:
    for line in fp:
        riga = line[:-1]
        coeffs.append(float(riga))

inp = float(input("Channel output [ADU]: "))

ADU_to_convert = inp * (1.8 / 2 ** 11)
print(
    str(ADU_to_convert)
    + " V = "
    + str(
        abs(
            gaps_fdt_tanh(
                [ADU_to_convert],
                coeffs[0],
                coeffs[1],
                coeffs[2],
                coeffs[3],
                coeffs[4],
                coeffs[5],
                coeffs[6],
                coeffs[7],
                coeffs[8],
            )[0]
        )
    )
    + " fC"
)
