from cmath import cosh
from mpmath import log


def gaps_fdt_tanh_8_params(x, m1, m2, m3, m4, m5, m6, m7, m8):
    output = []
    for i in x:
        val = 0.5 * (
            m1 * (i - m5) + (m2 / m3) * log(cosh(m3 * (i - m5 - m4)) / cosh(m3 * m4))
        ) + (m6 / m7) * log(cosh(m7 * (i - m5 - m8)) / cosh(m7 * m8))

        output.append(float(val))

    return output


weights_fdt_tanh_8_params = [
    2398.2,
    1071.2,
    2.712,
    1.2462,
    0.30821,
    644.83,
    1.7682,
    1.7392,
]
