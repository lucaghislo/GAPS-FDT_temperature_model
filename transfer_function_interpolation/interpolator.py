import math
import os
from cmath import cosh
import numpy as np
import sympy as sy
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from mpmath import *
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
from get_residual_metric import *
from matplotlib.patches import Rectangle


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
# folder_path: file path to main output folder
# prefix: file name prefix for all files
def interpolate_fdt(
    x_data,
    y_data,
    interpolating_function,
    initial_guess,
    num_parameters,
    folder_path,
    prefix,
    temperature,
    n_iteration,
    save_file_flag,
    weights_in=[],
    pedestal=[],
):

    temp_flag = True

    # Check temperature
    if temperature == None:
        temp_flag = False

    # Conversion DAC_inj_code to keV to fC
    y_data = [yi * coeff_DAC_inj_kev for yi in y_data]
    y_data = [yi * coeff_keV_fC for yi in y_data]

    # Conversion ADU to V
    # x_data = [xi - pedestal for xi in x_data]
    x_data = [xi * coeff_ADU_mV for xi in x_data]

    if len(weights_in) == 0:
        # Weigth definition (treated as **(-1))
        weights = [(1 / (xi ** 2)) ** (-1) for xi in x_data]
    else:
        weights = weights_in

    # Bounds definition
    bound_low = []
    bound_up = []

    # Set m5 parameter (pedestal) to measured pedestal for the channel at given tau
    # initial_guess[6] = pedestal * coeff_ADU_mV

    # General bounds
    h_count = 0
    for h in initial_guess:
        if h_count == 6:
            bound_low.append(h - abs(h) / 2)
            bound_up.append(h + abs(h) / 2)
        else:
            bound_low.append(h - abs(h) / 2)
            bound_up.append(h + abs(h) / 2)

        h_count = h_count + 1

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

    # Estimate y given x using estimated coefficients
    ans = interpolating_function(x_data, *popt)

    # R2
    r_squared = r2_score(y_data, ans)
    print(prefix + " iter " + str(n_iteration) + " -> R2: " + str(r_squared))

    # Make directory to store output files
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    iter_folder_path = os.path.join(folder_path, "iter_" + str(n_iteration))

    if not os.path.exists(iter_folder_path):
        os.mkdir(iter_folder_path)

    data_folder_path = os.path.join(iter_folder_path, "data")

    if not os.path.exists(data_folder_path):
        os.mkdir(data_folder_path)

    # Write estimated coefficients to file
    if save_file_flag:
        path_out = os.path.join(
            data_folder_path,
            prefix
            + "_estimated_coefficients_"
            + str(num_parameters)
            + "_params_iter"
            + str(n_iteration)
            + ".txt",
        )
        with open(path_out, "w") as fp:
            counter = 0
            for item in popt:
                fp.write(f"m{counter + 1}: {item}\n")
                counter = counter + 1

            fp.write(f"\nR2: {r_squared}\n")

    # Plot interpolated data [fC vs V]
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
    plt.xlabel("Channel Output [V]")
    plt.ylabel("Input Capacitance [fC]")
    if temp_flag:
        plt.title(
            "Input Capacitance vs Channel Output at T = " + str(temperature) + " °C",
            weight="bold",
        )
    else:
        plt.title(
            "Input Capacitance vs Channel Output",
            weight="bold",
        )
    plt.legend()
    plt.grid(True)
    path_out = os.path.join(
        iter_folder_path,
        prefix
        + "_interpolation_tanh_"
        + str(num_parameters)
        + "_params_fC_V_log-log_iter"
        + str(n_iteration)
        + ".pdf",
    )
    if save_file_flag:
        plt.savefig(path_out)

    # Linear scale
    plt.yscale("linear")
    plt.xscale("linear")
    plt.legend()
    plt.grid(True)
    path_out = os.path.join(
        iter_folder_path,
        prefix
        + "_interpolation_tanh_"
        + str(num_parameters)
        + "_params_fC_V_lin-lin_iter"
        + str(n_iteration)
        + ".pdf",
    )
    if save_file_flag:
        plt.savefig(path_out)

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
    if temp_flag:
        plt.title(
            "Incoming Energy vs Channel Output at T = " + str(temperature) + " °C",
            weight="bold",
        )
    else:
        plt.title(
            "Incoming Energy vs Channel Output",
            weight="bold",
        )
    plt.legend()
    plt.grid(True)
    path_out = os.path.join(
        iter_folder_path,
        prefix
        + "_interpolation_tanh_"
        + str(num_parameters)
        + "_params_keV_ADU_log-log_iter"
        + str(n_iteration)
        + ".pdf",
    )
    if save_file_flag:
        plt.savefig(path_out)

    # Linear scale
    plt.yscale("linear")
    plt.xscale("linear")
    plt.legend()
    plt.grid(True)
    path_out = os.path.join(
        iter_folder_path,
        prefix
        + "_interpolation_tanh_"
        + str(num_parameters)
        + "_params_keV_ADU_lin-lin_iter"
        + str(n_iteration)
        + ".pdf",
    )
    if save_file_flag:
        plt.savefig(path_out)

    # Residual evaluation and comparison with transfer function resolution
    resolution = []
    residuals = []
    resolution_data = []
    residuals_percent = []
    for i in range(0, len(x_data) - 1):
        den = x_data[i + 1] - x_data[i]
        if den == 0:
            den = 10 ** -10
        resolution_data.append((y_data[i + 1] - y_data[i]) / den)
        resolution.append((ans[i + 1] - ans[i]) / den)
        res = abs(y_data[i] - ans[i])
        residuals.append(res)
        residuals_percent.append((res / ans[i]) * 100)

    # resolution = np.gradient(ans, edge_order=2)
    # resolution_data = np.gradient(y_data, edge_order=2)

    resolution_data.append(resolution_data[len(resolution_data) - 1] * 1.1)
    resolution.append(resolution[len(resolution) - 1] * 1.1)
    residuals.append(residuals[len(residuals) - 1] * 1.1)
    residuals_percent.append(residuals_percent[len(residuals_percent) - 1] * 1.1)

    # Write residuals to file
    if save_file_flag:
        path_out_res = os.path.join(
            data_folder_path,
            prefix
            + "_residuals_"
            + str(num_parameters)
            + "_params_iter"
            + str(n_iteration)
            + ".txt",
        )
        with open(path_out_res, "w") as fp:
            for item in residuals:
                fp.write(f"{item}\n")

    # Write weights to file
    if save_file_flag:
        path_out_weights = os.path.join(
            iter_folder_path,
            prefix
            + "_weights_"
            + str(num_parameters)
            + "_params_iter"
            + str(n_iteration)
            + ".txt",
        )
        with open(path_out_weights, "w") as fp:
            for item in weights:
                fp.write(f"{item}\n")

    # Plot residuals compared to transfer function resolution
    plt.clf()
    plt.plot(
        y_data,
        resolution_data,
        label="Resolution",
        color="green",
        marker="o",
        markersize=1.5,
    )
    plt.plot(
        y_data,
        residuals,
        label="Residuals",
        color="blue",
        marker="o",
        markersize=1.5,
    )
    plt.xlabel("Incoming Energy [keV]")
    plt.ylabel("Resolution [keV/ADU]")
    if temp_flag:
        plt.title(
            "Resolution and Residuals vs Incoming Energy at T = "
            + str(temperature)
            + " °C",
            weight="bold",
        )
    else:
        plt.title(
            "Resolution and Residuals vs Incoming Energy",
            weight="bold",
        )
    plt.legend()
    plt.grid(True)
    path_out = os.path.join(
        iter_folder_path,
        prefix
        + "_residuals_tanh_"
        + str(num_parameters)
        + "_params_lin-lin_iter"
        + str(n_iteration)
        + ".pdf",
    )

    if save_file_flag:
        plt.savefig(path_out)

    # Log scale
    plt.yscale("log")
    plt.xscale("log")
    plt.legend()
    plt.grid(True)
    path_out = os.path.join(
        iter_folder_path,
        prefix
        + "_residuals_tanh_"
        + str(num_parameters)
        + "_params_log-log_iter"
        + str(n_iteration)
        + ".pdf",
    )
    if save_file_flag:
        plt.savefig(path_out)

    # Plot residuals as percentage
    plt.clf()
    plt.plot(
        y_data,
        residuals_percent,
        label="Residuals",
        color="blue",
        marker="o",
        markersize=1.5,
    )
    plt.xlabel("Incoming Energy [keV]")
    plt.ylabel("Residuals [%]")
    if temp_flag:
        plt.title(
            "Residuals vs Incoming Energy at T = " + str(temperature) + " °C",
            weight="bold",
        )
    else:
        plt.title(
            "Residuals vs Incoming Energy",
            weight="bold",
        )
    plt.yscale("log")
    plt.xscale("log")
    plt.legend()
    plt.grid(True)
    path_out = os.path.join(
        iter_folder_path,
        prefix
        + "_residuals_tanh_"
        + str(num_parameters)
        + "_params_percent_iter"
        + str(n_iteration)
        + ".pdf",
    )
    if save_file_flag:
        plt.savefig(path_out)

    weights_folder_path = os.path.join(iter_folder_path, "weights")

    if not os.path.exists(weights_folder_path):
        os.mkdir(weights_folder_path)

    # Plot weights
    plt.clf()
    plt.plot(
        x_data,
        weights,
        marker="o",
        markersize=1.5,
    )
    plt.xlabel("Channel Output [ADU]")
    plt.ylabel("Weight")
    if temp_flag:
        plt.title(
            "Weights vs Channel Output at T = " + str(temperature) + " °C",
            weight="bold",
        )
    else:
        plt.title(
            "Weights vs Channel Output",
            weight="bold",
        )
    plt.grid(True)
    path_out = os.path.join(
        weights_folder_path,
        prefix
        + "_weights_tanh_"
        + str(num_parameters)
        + "_params_lin-lin_iter"
        + str(n_iteration)
        + ".pdf",
    )

    if save_file_flag:
        plt.savefig(path_out)

    # Plot error histogram
    plt.clf()
    [sum, array] = residual_metric(resolution_data, residuals)
    counts, bins, bars = plt.hist(array, bins=[0, 1, 2, 3], edgecolor="black")
    # set colors
    cmap = plt.get_cmap("jet")
    low = cmap(0.5)
    medium = cmap(0.25)
    high = cmap(0.8)
    bars[0].set_facecolor(low)
    bars[1].set_facecolor(medium)
    bars[2].set_facecolor(high)

    # create legend
    handles = [Rectangle((0, 0), 1, 1, color=c, ec="k") for c in [low, medium, high]]
    percentages = []
    for i in range(0, 3):
        perc = counts[i] / np.sum(counts)
        perc = perc * 100
        percentages.append(np.round(perc, 2))

    labels = [
        str(percentages[0]) + " %",
        str(percentages[1]) + " %",
        str(percentages[2]) + " %",
    ]
    plt.legend(handles, labels)

    plt.ylabel("Count")
    plt.xlabel("Error [ADU]")
    if temp_flag:
        plt.title(
            "Errors at T = " + str(temperature) + " °C",
            weight="bold",
        )
    else:
        plt.title(
            "Errors",
            weight="bold",
        )
    path_out = os.path.join(
        iter_folder_path,
        prefix
        + "_errors_tanh_"
        + str(num_parameters)
        + "_params_lin-lin_iter"
        + str(n_iteration)
        + ".pdf",
    )

    if save_file_flag:
        plt.savefig(path_out)

    return (
        x_data,
        y_data,
        ans,
        popt,
        resolution,
        resolution_data,
        residuals,
        residuals_percent,
        r_squared,
        weights,
    )
