import sys
from interpolator import *
from fdt_formulas import tanh_5_params as t5
from fdt_formulas import tanh_8_params as t8
from fdt_formulas import tanh_9_params as t9
from get_long_fdt import *

# SCRIPT CONFIGURATION
# Peaking time
min_tau = 0  # Starting peaking time (min: 0)
max_tau = 0  # Finishing peaking time (max: 7)

# Channels
min_ch = 0  # Starting channel (min: 0)
max_ch = 0  # Finishing channel (max: 31)

# Model selection
n_params = 8  # Number of parameters (allowed: 5, 8, 9)

# Output folder path
main_path = "transfer_function_interpolation\output"

# Output folder name
folder_name = "all-ch_all-pts_long-fdt_module_238_-40C"

if n_params == 5:
    fdt = t5.gaps_fdt_tanh_5_params
    guess = t5.weights_fdt_tanh_5_params
elif n_params == 8:
    fdt = t8.gaps_fdt_tanh_8_params
    guess = t8.weights_fdt_tanh_8_params
else:
    fdt = t9.gaps_fdt_tanh_9_params
    guess = t9.weights_fdt_tanh_9_params

for tau in range(min_tau, max_tau + 1):
    for ch_number in range(min_ch, max_ch + 1):
        [dac_inj, ch_data] = get_long_fdt(
            "transfer_function_interpolation\input\module_long_fdts", ch_number, tau
        )

        prefix = "ch_" + str(ch_number) + "_tau_" + str(tau)
        folder_path = os.path.join(
            main_path,
            folder_name,
            prefix + "_" + str(n_params) + "_params",
        )

        ch_data = ch_data[1 : len(ch_data)]
        dac_inj = dac_inj[1 : len(dac_inj)]

        # Interpolator function call
        interpolate_fdt(
            ch_data,
            dac_inj,
            fdt,
            guess,
            n_params,
            folder_path,
            prefix,
        )
