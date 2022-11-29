import math
from cmath import cosh
import numpy as np
import sympy as sy
from mpmath import *


def gaps_fdt_tanh_8_params(x, m1, m2, m3, m4, m5, m6, m7, m8):
    output = []
    for i in x:
        val = 0.5 * (
            m1 * (i - m5) + (m2 / m3) * log(cosh(m3 * (i - m5 - m4)) / cosh(m3 * m4))
        ) + (m6 / m7) * log(cosh(m7 * (i - m5 - m8)) / cosh(m7 * m8))

        output.append(float(val))

    return output


weights_fdt_tanh_8_params_old = [
    2398.2,
    1071.2,
    2.712,
    1.2462,
    0.30821,
    644.83,
    1.7682,
    1.7392,
]

weights_fdt_tanh_8_params = [
    2354.98768589752,
    1045.55111079868,
    2.62814603729687,
    1.19245024543125,
    0.249192601225,
    634.650330488431,
    1.96527106959062,
    1.658624334775,
]
