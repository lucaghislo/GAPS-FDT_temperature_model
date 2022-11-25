import math
from cmath import cosh
import numpy as np
import sympy as sy
from mpmath import *


def gaps_fdt_tanh_5_params(x, m1, m2, m3, m4, m5):
    output = []
    for i in x:
        val = 0.5 * (
            m1 * (i + m5)
            + (m2 / m3) * log(cosh(m3 * (i - abs(m5) - m4)) / cosh(m3 * m4))
        )

        output.append(float(val))

    return output


weights_fdt_tanh_5_params = [2060.8, 2041, 2.3149, 1.38, -0.31057]
