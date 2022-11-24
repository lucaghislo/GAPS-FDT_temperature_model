import math
from cmath import cosh
import numpy as np
import sympy as sy
from mpmath import *


def gaps_fdt_tanh_9_params(x, m1, m2, m3, m4, m5, m6, m7, m8, m9):
    output = []
    for i in x:
        val = 0.5 * (
            m1 * (i + m5) + m2 * log(cosh(m3 * ((i + m5) - m4)) / cosh(m3 * m4))
        ) + m6 * log(cosh(m7 * ((i - abs(m8)) - m9)) / cosh(m7 * m9))

        output.append(float(val))

    return output


weights_fdt_tanh_9_params = [
    2398.2,
    729.51,
    1.7682,
    1.721,
    -0.32629,
    197.43,
    2.7122,
    0.32706,
    1.2274,
]
