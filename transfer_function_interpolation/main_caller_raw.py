import sys
from interpolator import *
from fdt_formulas import tanh_5_params as t5
from fdt_formulas import tanh_8_params as t8
from fdt_formulas import tanh_9_params as t9
from get_long_fdt import *
from get_raw_fdt import *
from get_module_temperature import *
from import_pedestals import *
from compute_weights import *
from get_residual_metric import *

# SCRIPT CONFIGURATION
# Peaking time
min_tau = 0  # Starting peaking time (min: 0)
max_tau = 0  # Finishing peaking time (max: 7)

# Channels
min_ch = 0  # Starting channel (min: 0)
max_ch = 0  # Finishing channel (max: 31)

# Model selection
n_params = 8  # Number of parameters (allowed: 5, 8, 9)

# Maximum number of optimization steps
n_iter = 300

# Input FDT file path
# input_fdt_path = r"transfer_function_interpolation\input\raw_modules\MODULE_496\1\data\TransferFunction.dat"
# input_fdt_path = r"transfer_function_interpolation\input\raw_modules\MODULE_Napoli\1\data\TransferFunction.dat"
input_fdt_path = r"transfer_function_interpolation\input\raw_modules\MODULE_Bergamo\data\TransferFunction.dat"

# Input temperature file path
# input_temp_path = r"transfer_function_interpolation\input\raw_modules\MODULE_496\1\data\HK_Temperature.dat"
# input_temp_path = r"transfer_function_interpolation\input\raw_modules\MODULE_Napoli\1\data\HK_Temperature.dat"
input_temp_path = r"transfer_function_interpolation\input\raw_modules\MODULE_Bergamo\data\HK_Temperature.dat"

# Input pedestals file path
# input_pedestal_path = (r"transfer_function_interpolation\input\raw_modules\MODULE_496\1\data\Pedestals.dat")
# input_pedestal_path = r"transfer_function_interpolation\input\raw_modules\MODULE_Napoli\1\data\Pedestals.dat"
# input_pedestal_path = r"transfer_function_interpolation\input\raw_modules\MODULE_Bergamo\data\Pedestals.dat"

# Output folder path
main_output_path = "transfer_function_interpolation\output"

# Output folder name
output_folder_name = "all-ch_all-pts_short-fdt_MODULE_496_Tamb"
# output_folder_name = "all-ch_all-pts_short-fdt_module_NAPOLI_-40C"
output_folder_name = "all-ch_all-pts_short-fdt_Module_Bergamo_-40C"

if n_params == 5:
    fdt = t5.gaps_fdt_tanh_5_params
    guess = t5.weights_fdt_tanh_5_params
elif n_params == 8:
    fdt = t8.gaps_fdt_tanh_8_params
    guess = t8.weights_fdt_tanh_8_params
else:
    fdt = t9.gaps_fdt_tanh_9_params
    guess = t9.weights_fdt_tanh_9_params

main_folder_path = os.path.join(main_output_path, output_folder_name)

all_x_data = []
xdata_flag = False

# Get module temperature (if provided)
temperature = None
if input_temp_path == "":
    print("\n Module temperature file not provided!\n")
else:
    temperature = get_module_temperature(input_temp_path)
    temperature = temperature[0]

for tau in range(min_tau, max_tau + 1):

    all_popt = []
    all_ans = []
    all_y = []
    all_resolution = []
    all_resolution_data = []
    all_residuals = []
    all_residuals_percent = []
    all_r_squared = []

    for ch_number in range(min_ch, max_ch + 1):

        # Configure path for data save
        prefix = "ch_" + str(ch_number) + "_tau_" + str(tau)
        folder_path = os.path.join(
            main_output_path,
            output_folder_name,
            prefix + "_" + str(n_params) + "_params",
        )

        # Obtain raw data from module FDT file
        # X and Y must be supplied as 1-D arrays
        [dac_inj, ch_data] = get_raw_fdt(
            input_fdt_path,
            ch_number,
            tau,
        )

        # Exclude channel output for 0 DAC_inj_code
        # Only when FDT starts from 0 DAC_inj_code
        ch_data = ch_data[1 : len(ch_data)]
        dac_inj = dac_inj[1 : len(dac_inj)]

        # Get pedestal data for given channel at tau
        # pedestal = import_pedestals(input_pedestal_path, ch_number, tau)
        # pedestal = pedestal[0]

        weights_computed = []

        [
            y_data,
            x_data,
            ans,
            popt,
            resolution,
            resolution_data,
            residuals,
            residuals_percent,
            r_squared,
            weights,
        ] = interpolate_fdt(
            ch_data,
            dac_inj,
            fdt,
            guess,
            n_params,
            folder_path,
            prefix,
            temperature,
            0,
            True,
        )

        res_metric = residual_metric(resolution, residuals)
        # print(res_metric[0])
        weights_computed = compute_weigths(weights, residuals, resolution_data)

        for k in range(1, n_iter + 2):
            [
                y_data_iter,
                x_data_iter,
                ans_iter,
                popt_iter,
                resolution_iter,
                resolution_data_iter,
                residuals_iter,
                residuals_percent_iter,
                r_squared_iter,
                weights_iter,
            ] = interpolate_fdt(
                ch_data,
                dac_inj,
                fdt,
                popt,
                n_params,
                folder_path,
                prefix,
                temperature,
                k,
                True,
                weights_computed,
            )

            res_metric_iter = residual_metric(resolution_iter, residuals_iter)
            # print(res_metric_iter[0])

            if (res_metric_iter[0] < res_metric[0]) and (k < n_iter + 1):
                res_metric = res_metric_iter
                weights_computed = compute_weigths(
                    weights_iter, residuals_iter, resolution_data_iter
                )
                ans = ans_iter
                popt = popt_iter
                resolution = resolution_iter
                resolution_data = resolution_data_iter
                residuals = residuals_iter
                residuals_percent = residuals_percent_iter
                r_squared = r_squared_iter
                weights = weights_iter
            else:
                print(
                    "\nIteration stopped! Best found at iteration " + str(k - 1) + "."
                )
                [
                    y_data_iter,
                    x_data_iter,
                    ans_iter,
                    popt_iter,
                    resolution_iter,
                    resolution_data_iter,
                    residuals_iter,
                    residuals_percent_iter,
                    r_squared_iter,
                    weights_iter,
                ] = interpolate_fdt(
                    ch_data,
                    dac_inj,
                    fdt,
                    popt,
                    n_params,
                    folder_path,
                    prefix,
                    temperature,
                    k - 1,
                    True,
                    weights,
                )
                ans = ans_iter
                popt = popt_iter
                resolution = resolution_iter
                resolution_data = resolution_data_iter
                residuals = residuals_iter
                residuals_percent = residuals_percent_iter
                r_squared = r_squared_iter
                weights = weights_iter
                print("\n")
                break

        # Save output data from function
        all_popt.append(popt)
        all_ans.append(ans)
        all_y.append(ans)
        all_resolution.append(resolution)
        all_resolution_data.append(resolution_data)
        all_residuals.append(residuals)
        all_residuals_percent.append(residuals_percent)
        all_r_squared.append(r_squared)

        if not xdata_flag:
            all_x_data.append(x_data)
            xdata_flag = True

    # Save estimated parameters
    # Column: parameter
    #    Row: channel
    mat_popt = np.matrix(all_popt)
    path_out_popt = os.path.join(
        main_folder_path,
        "all_popt_tau_" + str(tau) + "_" + str(n_params) + "_params.dat",
    )
    with open(path_out_popt, "wb") as f:
        for line in mat_popt:
            np.savetxt(f, line, fmt="%.10f")

    print("\nSAVED: " + path_out_popt)

    # Save all ans (Y) obtained for all X from interpolating function
    # Column: channel
    #    Row: interpolation output for given X
    mat_ans = np.matrix(all_ans).transpose()
    path_out_ans = os.path.join(
        main_folder_path,
        "all_ans_tau_" + str(tau) + "_" + str(n_params) + "_params.dat",
    )
    with open(path_out_ans, "wb") as f:
        for line in mat_ans:
            np.savetxt(f, line, fmt="%.10f")

    print("\nSAVED: " + path_out_ans)

    # Save all Y from the original transfer function data
    # Column: channel
    #    Row: raw transfer function value for given X
    mat_y = np.matrix(all_y).transpose()
    path_out_y = os.path.join(
        main_folder_path,
        "all_y_tau_" + str(tau) + "_" + str(n_params) + "_params.dat",
    )
    with open(path_out_y, "wb") as f:
        for line in mat_y:
            np.savetxt(f, line, fmt="%.10f")

    print("\nSAVED: " + path_out_y)

    # Save resolution from interpolation
    # Column: channel
    #    Row: resolution
    mat_resolution = np.matrix(all_resolution).transpose()
    path_out_resolution = os.path.join(
        main_folder_path,
        "all_resolution_tau_" + str(tau) + "_" + str(n_params) + "_params.dat",
    )
    with open(path_out_resolution, "wb") as f:
        for line in mat_resolution:
            np.savetxt(f, line, fmt="%.10f")

    print("\nSAVED: " + path_out_resolution)

    # Save data resolution
    # Column: channel
    #    Row: data resolution
    mat_resolution_data = np.matrix(all_resolution_data).transpose()
    path_out_resolution_data = os.path.join(
        main_folder_path,
        "all_resolution_data_tau_" + str(tau) + "_" + str(n_params) + "_params.dat",
    )
    with open(path_out_resolution_data, "wb") as f:
        for line in mat_resolution_data:
            np.savetxt(f, line, fmt="%.10f")

    print("\nSAVED: " + path_out_resolution_data)

    # Save data residuals from interpolation
    # Column: channel
    #    Row: fit residuals
    mat_residuals = np.matrix(all_residuals).transpose()
    path_out_residuals = os.path.join(
        main_folder_path,
        "all_residuals_tau_" + str(tau) + "_" + str(n_params) + "_params.dat",
    )
    with open(path_out_residuals, "wb") as f:
        for line in mat_residuals:
            np.savetxt(f, line, fmt="%.10f")

    print("\nSAVED: " + path_out_residuals)

    # Save data residuals percentage from interpolation
    # Column: channel
    #    Row: fit residuals percentage
    mat_residuals_percent = np.matrix(all_residuals_percent).transpose()
    path_out_residuals_percent = os.path.join(
        main_folder_path,
        "all_residuals_percent_tau_" + str(tau) + "_" + str(n_params) + "_params.dat",
    )
    with open(path_out_residuals_percent, "wb") as f:
        for line in mat_residuals_percent:
            np.savetxt(f, line, fmt="%.10f")

    print("\nSAVED: " + path_out_residuals_percent)

    # Save R2 from interpolation
    # Column: channel
    #    Row: R2
    mat_r_squared = np.matrix(all_r_squared).transpose()
    path_out_r_squared = os.path.join(
        main_folder_path,
        "all_r_squared_tau_" + str(tau) + "_" + str(n_params) + "_params.dat",
    )
    with open(path_out_r_squared, "wb") as f:
        for line in mat_r_squared:
            np.savetxt(f, line, fmt="%.16f")

    print("\nSAVED: " + path_out_r_squared + "\n")


# Save X data (real X data)
# Column: value
#    Row: injecteted energy [keV]
mat_x_data = np.matrix(all_x_data).transpose()
path_out_x_data = os.path.join(
    main_folder_path,
    "all_x_data.dat",
)
with open(path_out_x_data, "wb") as f:
    for line in mat_x_data:
        np.savetxt(f, line, fmt="%.10f")

print("SAVED: " + path_out_x_data)
