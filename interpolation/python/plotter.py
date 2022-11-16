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

# 326 dati
x_long = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    49,
    50,
    51,
    52,
    53,
    54,
    55,
    56,
    57,
    58,
    59,
    60,
    61,
    62,
    63,
    64,
    65,
    66,
    67,
    68,
    69,
    70,
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    80,
    81,
    82,
    83,
    84,
    85,
    86,
    87,
    88,
    89,
    90,
    91,
    92,
    93,
    94,
    95,
    96,
    97,
    98,
    99,
    100,
    110,
    120,
    130,
    140,
    150,
    160,
    170,
    180,
    190,
    200,
    210,
    220,
    230,
    240,
    250,
    260,
    270,
    280,
    290,
    300,
    310,
    320,
    330,
    340,
    350,
    360,
    370,
    380,
    390,
    400,
    410,
    420,
    430,
    440,
    450,
    460,
    470,
    480,
    490,
    500,
    510,
    520,
    530,
    540,
    550,
    560,
    570,
    580,
    590,
    600,
    610,
    620,
    630,
    640,
    650,
    660,
    670,
    680,
    690,
    700,
    710,
    720,
    730,
    740,
    750,
    760,
    770,
    780,
    790,
    800,
    810,
    820,
    830,
    840,
    850,
    860,
    870,
    880,
    890,
    900,
    910,
    920,
    930,
    940,
    950,
    960,
    970,
    980,
    990,
    1000,
    1010,
    1020,
    1030,
    1040,
    1050,
    1060,
    1070,
    1080,
    1090,
    1100,
    1110,
    1120,
    1130,
    1140,
    1150,
    1160,
    1170,
    1180,
    1190,
    1200,
    1210,
    1220,
    1230,
    1240,
    1250,
    1260,
    1270,
    1280,
    1290,
    1300,
    1310,
    1320,
    1330,
    1340,
    1350,
    1360,
    1370,
    1380,
    1390,
    1400,
    1410,
    1420,
    1430,
    1440,
    1450,
    1460,
    1470,
    1480,
    1490,
    1500,
    1600,
    1700,
    1800,
    1900,
    2000,
    2100,
    2200,
    2300,
    2400,
    2500,
    2600,
    2700,
    2800,
    2900,
    3000,
    3100,
    3200,
    3300,
    3400,
    3500,
    3600,
    3700,
    3800,
    3900,
    4000,
    5000,
    6000,
    7000,
    8000,
    9000,
    10000,
    11000,
    12000,
    13000,
    14000,
    15000,
    16000,
    17000,
    18000,
    19000,
    20000,
    21000,
    22000,
    23000,
    24000,
    25000,
    26000,
    27000,
    28000,
    29000,
    30000,
    31000,
    32000,
    33000,
    34000,
    35000,
    36000,
    37000,
    38000,
    39000,
    40000,
    41000,
    42000,
    43000,
    44000,
    45000,
    46000,
    47000,
    48000,
    49000,
    50000,
    51000,
    52000,
    53000,
    54000,
    55000,
    56000,
    57000,
    58000,
    59000,
    60000,
    61000,
    62000,
    63000,
    64000,
]
y_long = [
    177.87,
    165.35,
    166.04,
    167.06,
    167.87,
    168.92,
    169.46,
    170.39,
    171.24,
    171.82,
    172.42,
    173.57,
    173.68,
    175.17,
    175.65,
    176.99,
    177.61,
    178.34,
    179.19,
    179.37,
    179.8,
    181.55,
    181.55,
    182.6,
    183.4,
    184.14,
    185.81,
    185.79,
    186.52,
    187.86,
    188.3,
    189.54,
    190.25,
    190.78,
    191.95,
    192.92,
    193.07,
    194.14,
    195,
    196,
    196.38,
    196.77,
    198.24,
    198.05,
    198.93,
    200.29,
    200.46,
    201.84,
    202.05,
    203,
    203.86,
    204.21,
    204.71,
    205.89,
    205.97,
    206.99,
    208.22,
    208.61,
    209.43,
    209.97,
    210.49,
    211.34,
    212.19,
    213.19,
    213.59,
    214.29,
    215.13,
    216.17,
    216.94,
    217.82,
    218.16,
    218.76,
    219.71,
    220.5,
    220.79,
    221.62,
    221.94,
    223.61,
    223.58,
    224.54,
    225.43,
    225.79,
    227.09,
    227.18,
    228.17,
    229.44,
    229.53,
    230.25,
    230.67,
    232.13,
    232.99,
    233.26,
    234.25,
    234.74,
    235.45,
    235.97,
    236.87,
    237.39,
    238.66,
    239.19,
    239.67,
    246.59,
    254.54,
    261.67,
    269.01,
    276.07,
    282.46,
    289.21,
    296.04,
    302.74,
    309.8,
    316.34,
    322.41,
    328.58,
    334.66,
    340.28,
    346.56,
    352.76,
    358.47,
    364.4,
    369.25,
    374.84,
    381.63,
    386.4,
    391.83,
    396.73,
    401.56,
    406.31,
    411.05,
    415.06,
    420.35,
    424.86,
    429.37,
    433.75,
    437.55,
    442.54,
    446.14,
    450.27,
    453.74,
    457.97,
    462.16,
    464.86,
    468.58,
    473.13,
    475.46,
    479.4,
    482.79,
    486.33,
    489.69,
    492.66,
    495.32,
    498.92,
    502.64,
    504.73,
    507.34,
    510.99,
    514.18,
    517.13,
    519.45,
    522.73,
    524.95,
    528.24,
    530.01,
    532.1,
    535.31,
    537.74,
    539.66,
    541.68,
    543.49,
    545.84,
    549.1,
    550.72,
    552.85,
    554.87,
    557.08,
    559.16,
    560.34,
    563.45,
    565.38,
    567.72,
    568.76,
    570.86,
    573.11,
    575.15,
    577.11,
    579.14,
    579.83,
    582.14,
    584.52,
    585.48,
    587.37,
    589.12,
    590.98,
    591.92,
    593.3,
    595.18,
    596.27,
    598.89,
    600.29,
    601.34,
    603.02,
    604.44,
    607.08,
    608.09,
    608.97,
    610.52,
    612.94,
    613.17,
    614.52,
    616.28,
    617.88,
    619.18,
    620.76,
    621.07,
    623.17,
    625.18,
    625.34,
    626.61,
    628.02,
    629.36,
    630.76,
    632.8,
    632.03,
    634.13,
    636.02,
    636.72,
    637.96,
    639.6,
    640.68,
    642.22,
    643.74,
    643.22,
    644.42,
    646.97,
    647.59,
    648.57,
    649.24,
    650.01,
    650.44,
    652.9,
    653.78,
    663.26,
    673.26,
    683.37,
    691.35,
    699.47,
    706.74,
    714.05,
    720.64,
    727.76,
    734.37,
    739.85,
    745.31,
    751.55,
    756.78,
    762.57,
    767.22,
    772.26,
    777.06,
    782.76,
    786.2,
    790.88,
    796.11,
    799.05,
    802.88,
    806.97,
    842.58,
    872.81,
    898.48,
    922.26,
    942.91,
    963.18,
    981.7,
    999.27,
    1013.52,
    1033.96,
    1048.74,
    1062.6,
    1076.7,
    1091.2,
    1104.82,
    1117.71,
    1130.58,
    1142.09,
    1154.88,
    1167.78,
    1178.22,
    1189.75,
    1202.11,
    1212.97,
    1223.7,
    1234.99,
    1245.61,
    1256.1,
    1267.17,
    1277.35,
    1288.92,
    1299.65,
    1308.68,
    1319.16,
    1329.11,
    1339.6,
    1349.08,
    1359.03,
    1369.36,
    1378.73,
    1387.39,
    1397.17,
    1407.81,
    1417.23,
    1426.85,
    1436.33,
    1446.26,
    1456.05,
    1463.96,
    1472.55,
    1483.23,
    1491.75,
    1500.75,
    1510.27,
    1518.28,
    1528.04,
    1537.15,
    1547.12,
    1556.42,
    1564.84,
]

# 55 dati
x_short = [
    10,
    20,
    30,
    40,
    50,
    60,
    70,
    80,
    90,
    100,
    200,
    300,
    400,
    500,
    600,
    700,
    800,
    900,
    1000,
    1200,
    1400,
    1600,
    1800,
    2000,
    4000,
    6000,
    8000,
    10000,
    12000,
    14000,
    16000,
    18000,
    20000,
    22000,
    24000,
    26000,
    28000,
    30000,
    32000,
    34000,
    36000,
    38000,
    40000,
    42000,
    44000,
    46000,
    48000,
    50000,
    52000,
    54000,
    56000,
    58000,
    60000,
    62000,
    64000,
]
y_short = [
    120.43,
    128.84,
    136.25,
    141.54,
    155.14,
    165.33,
    172.12,
    180.2,
    195.09,
    199.43,
    294.57,
    386.16,
    469.71,
    544.62,
    605.51,
    663.66,
    705.65,
    741.17,
    771.24,
    814.68,
    845.72,
    867.61,
    885.02,
    909.52,
    1049.4,
    1142.11,
    1209.52,
    1261.94,
    1306.41,
    1348.56,
    1393.61,
    1426.96,
    1456.31,
    1491.08,
    1522.72,
    1554.57,
    1580.57,
    1607.41,
    1635.19,
    1665.88,
    1687.37,
    1715.02,
    1742.42,
    1765.61,
    1790.61,
    1809.74,
    1835.26,
    1860.41,
    1877.74,
    1898.33,
    1915,
    1937.87,
    1953.14,
    1967.4,
    1982.79,
]

# Scelta del dataset
y = x_short[1:55]
x = y_short[1:55]

y = [yi * 0.0044 for yi in y]
x = [xi * (1.8 / 2 ** 11) for xi in x]

# Funzione interpolante la funzione di trasferimento con tangente iperbolica
# 0.5*(m1*(m0+m5)+m2*ln(cosh(m3*((m0+m5)-m4))/cosh(m3*m4)))+m6*ln(cosh(m7*((m0-abs(m8))-m9))/cosh(m7*m9));
# m1 = 41339;  m2 = 16961; m3=2.3; m4=1.3; m5=-0.3; m6=10000; m7=5; m8=0.3; m9=1; m10=1
# Seconda versione
# 0.5*(m1*(m0+m5)+m2*ln(cosh(m3*((m0+m5)-m4))/cosh(m3*m4)))+m6*ln(cosh(m7*((m0-abs(m8))-m9))/cosh(m7*m9));
# m1 = 413; m2 = 1961; m3=2.3; m4=1.3; m5=-0.3; m6=1000; m7=5; m8=0.3; m9=1
def gaps_fdt_tanh(k, m1, m2, m3, m4, m5, m6, m7, m8, m9):
    output = []
    for i in k:
        val = 0.5 * (
            m1 * (i + m5) + m2 * log(cosh(m3 * ((i + m5) - m4)) / cosh(m3 * m4))
        ) + m6 * log(cosh(m7 * ((i - abs(m8)) - m9)) / cosh(m7 * m9))

        output.append(float(val))

    return output


# Funzione interpolante la funzione di trasferimento con sigmoide
# m1*(m0-m5)+(m2+m6)*m0+m2/m4*ln((1+m3*exp(-m4*(m0-abs(m5))))/(1+m3*exp(abs(m4*m5))))+m6/m8*ln((1+m7*exp(-m8*(m0-abs(m9))))/(1+m7*exp(abs(m8*m9))));
# m1=16; m2=912; m3=39; m4=3.29; m5=0.907; m6=583; m7=28; m8=5.7; m9=0.908
def gaps_fdt_sigmoide(x, m1, m2, m3, m4, m5, m6, m7, m8, m9):
    return (
        m1 * (x - m5)
        + (m2 + m6) * x
        + m2
        / m4
        * log((1 + m3 * exp(-m4 * (x - abs(m5)))) / (1 + m3 * exp(abs(m4 * m5))))
        + m6
        / m8
        * log((1 + m7 * exp(-m8 * (x - abs(m9)))) / (1 + m7 * exp(abs(m8 * m9))))
    )


# open file in read mode
guess = []
with open(r"interpolation\python\results_weights.txt", "r") as fp:
    for line in fp:
        riga = line[:-1]
        guess.append(float(riga))

print(guess)

# Valori iniziali dei parametri per il fit
guess_tanh = [2398.2, 729.51, 1.7682, 1.721, -0.32629, 197.43, 2.7122, 0.32706, 1.2274]
guess_sigmoide = [16, 912, 39, 3.29, 0.907, 583, 28, 5.7, 0.908]

bound_low = []
bound_up = []
for h in guess_tanh:
    bound_low.append(h - abs(h / 10000))
    bound_up.append(h + abs(h / 10000))

print(bound_low)
print(bound_up)

# Definizione dei pesi secondo funzione peso
weights = []
for i in range(0, len(x)):
    if i < 10:
        weights.append(1.5)
    else:
        weights.append(i)

weights = []
for i in range(0, len(x)):
    if i < 255:
        weights.append(x[i] * 0.1)
    else:
        weights.append(x[i])

    if i < 110:
        weights[i] = weights[i] * 0.1

weights = []
for i in range(0, len(x)):
    if i < 8:
        weights.append(x[i] * 0.00000001)
    elif i > 24:
        weights.append(x[i] * 0.00000001)
    elif i > 12:
        weights.append(x[i] * 0.0000001)
    else:
        weights.append(x[i])

derivata1 = np.gradient(y, x, edge_order=2)
derivata2 = np.gradient(derivata1, x, edge_order=2)
derivata3 = np.gradient(derivata2, x, edge_order=2)
derivata2 = [np.abs(devi) for devi in derivata2]
weights = derivata2
weights = x

# Fit della curva
popt, pcov = curve_fit(
    gaps_fdt_tanh,
    x,
    y,
    guess_tanh,
    maxfev=1000000,
    bounds=[bound_low, bound_up],
    # sigma=weights,
    absolute_sigma=True,
)

# open file in write mode
with open(r"interpolation\python\results_weights.txt", "w") as fp:
    for item in popt:
        fp.write("%f\n" % item)

print("\nPARAMETRI STIMATI:")
print(popt)
# print(pcov)

# Calcolo dei valori in ADU attraverso funzione con parametri stimati da interpolazione
ans = gaps_fdt_tanh(
    x, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7], popt[8]
)

# Calcolo R^2
r_squared = r2_score(y, ans)
print("R2: " + str(r_squared))

# Conversione DAC_inj -> keV
y = [yi * coeff_DAC_inj_kev for yi in y]
ans = [ansi * coeff_DAC_inj_kev for ansi in ans]

# Calcolo risoluzione FDT e residui interpolazione
resolution_fdt = []
resolution_fit = []
residuals = []
for i in range(0, len(x)):
    # resolution_fdt.append((y[i + 1] - y[i]) / (x[i + 1] - x[i]))
    # resolution_fit.append((ans[i + 1] - ans[i]) / (x[i + 1] - x[i]))
    residuals.append(abs(y[i] - ans[i]))

print("Somma residui: " + str(sum(residuals)))

# Plot dei residui confrontati con la risoluzione
# plt.plot(y, resolution_fdt, color="red", marker="o", markersize=1, linestyle="none")
# plt.plot(y, resolution_fit, color="green", marker="o", markersize=1, linestyle="none")
# plt.plot(x, residuals, color="blue", marker="o", linestyle="none")
# plt.show()

# figure(figsize=(800, 600))
plt.plot(x, y, color="red", label="Data")
plt.plot(
    x, ans, color="blue", label="Fit", marker="o", linestyle="none", markersize=1.5
)
plt.yscale("log")
plt.xscale("log")
plt.xlabel("Channel Output [ADU]")
plt.ylabel("Incoming Energy [keV]")
# plt.ylim([1, 10e4])
plt.title("Incoming Energy vs Channel Output", weight="bold")
# plt.text(
#     550,
#     1,
#     "m1: "
#     + str(popt[0])
#     + "\nm2: "
#     + str(popt[1])
#     + "\nm3: "
#     + str(popt[2])
#     + "\nm4: "
#     + str(popt[3])
#     + "\nm5: "
#     + str(popt[4])
#     + "\nm6: "
#     + str(popt[5])
#     + "\nm7: "
#     + str(popt[6])
#     + "\nm8: "
#     + str(popt[7])
#     + "\nm9: "
#     + str(popt[8]),
#     bbox=dict(facecolor="white", alpha=0.5),
# )
plt.legend()
# plt.show()
plt.savefig("interpolation\python\interpolation_residuals.pdf")

# ADU_to_convert = 60
# print(
#     "Conversione: "
#     + str(ADU_to_convert)
#     + " ADU = "
#     + str(
#         abs(
#             gaps_fdt_tanh(
#                 [ADU_to_convert],
#                 popt[0],
#                 popt[1],
#                 popt[2],
#                 popt[3],
#                 popt[4],
#                 popt[5],
#                 popt[6],
#                 popt[7],
#                 popt[8],
#             )[0]
#             * coeff_DAC_inj_kev
#         )
#     )
#     + " keV"
# )
