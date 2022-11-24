import math
from cmath import cosh
import numpy as np
import sympy as sy
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from mpmath import *
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# Conversion factor DAC_inj_code to keV [keV/DAC_inj_code]
coeff_DAC_inj_kev = 0.841

# Conversion factor keV to fC [fC/keV]
coeff_keV_fC = 0.044

# Conversion factor ADU to mV [V/ADU]
coeff_ADU_mV = 1.76 * 10 ** (-3)

# INPUT PARAMETERS
# x_data: channel output (1D array) [ADU]
# y_data: simulated energy input (1D array) [DAC_inj_code]
# interpolating_function: function to interpolate (defined in file)
# initial_guess: initial values for parameter estimation (1D array)
# num_parameters: number of parameters to estimate (scalar)
def interpolate_fdt(
    x_data, y_data, interpolating_function, initial_guess, num_parameters
):

    # Conversion DAC_inj_code to keV to fC
    y_data = [yi * coeff_DAC_inj_kev for yi in y_data]
    y_data = [yi * coeff_keV_fC for yi in y_data]
    # Conversion ADU to V
    x_data = [xi * coeff_ADU_mV for xi in x_data]

    # Weigth definition (treated as **(-1))
    weights = [(1 / (xi ** 2)) ** (-1) for xi in x_data]

    # Bounds definition
    bound_low = []
    bound_up = []

    for h in initial_guess:
        bound_low.append(h - abs(h / 2))
        bound_up.append(h + abs(h / 2))

    # Fit della curva
    popt, pcov = curve_fit(
        interpolating_function,
        x_data,
        y_data,
        initial_guess,
        maxfev=1000000,
        bounds=[bound_low, bound_up],
        sigma=weights,
        absolute_sigma=True,
    )

    # write estimated coefficients to file
    with open(
        r"transfer_function_interpolation\output\estimated_coefficients_"
        + str(num_parameters)
        + r"_params.txt",
        "w",
    ) as fp:
        for item in popt:
            fp.write("%f\n" % item)

    # Estimate y given x using estimated coefficients
    ans = interpolating_function(x_data, *popt)

    # R2
    r_squared = r2_score(y_data, ans)
    print("R2: " + str(r_squared))

    # Plot interpolated data [fC vs V]
    plt.plot(x_data, y_data, color="red", label="Data")
    plt.plot(
        x_data,
        ans,
        color="blue",
        label="Fit",
        marker="o",
        linestyle="none",
        markersize=1.5,
    )
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel("Channel Output [V]")
    plt.ylabel("Input Capacitance [fC]")
    plt.title("Input Capacitance vs Channel Output", weight="bold")
    plt.legend()
    plt.savefig(
        "transfer_function_interpolation\output\interpolation_tanh_"
        + str(num_parameters)
        + "_params_fC_V_log-log.pdf"
    )
    plt.yscale("linear")
    plt.xscale("linear")
    plt.legend()
    plt.savefig(
        "transfer_function_interpolation\output\interpolation_tanh_"
        + str(num_parameters)
        + "_params_fC_V_lin-lin.pdf"
    )

    # Plot interpolated data [keV vs ADU]
    x_data = [xi / coeff_ADU_mV for xi in x_data]
    y_data = [yi / coeff_keV_fC for yi in y_data]
    ans = [ansi / coeff_keV_fC for ansi in ans]

    plt.clf()
    plt.plot(x_data, y_data, color="red", label="Data")
    plt.plot(
        x_data,
        ans,
        color="blue",
        label="Fit",
        marker="o",
        linestyle="none",
        markersize=1.5,
    )
    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel("Channel Output [ADU]")
    plt.ylabel("Incoming Energy [keV]")
    plt.title("Incoming Energy vs Channel Output", weight="bold")
    plt.legend()
    plt.savefig(
        "transfer_function_interpolation\output\interpolation_tanh_"
        + str(num_parameters)
        + "_params_keV_ADU_log-log.pdf"
    )
    plt.yscale("linear")
    plt.xscale("linear")
    plt.legend()
    plt.savefig(
        "transfer_function_interpolation\output\interpolation_tanh_"
        + str(num_parameters)
        + "_params_keV_ADU_lin-lin.pdf"
    )