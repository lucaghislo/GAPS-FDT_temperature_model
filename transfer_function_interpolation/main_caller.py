import sys
from interpolator import *
from fdt_formulas import tanh_5_params as t5
from fdt_formulas import tanh_8_params as t8
from fdt_formulas import tanh_9_params as t9
from get_long_fdt import *

# Config
tau = 6  # Peaking time
fdt = t9.gaps_fdt_tanh_9_params  # Transfer function
guess = t9.weights_fdt_tanh_9_params  # Initial values for parameter estimation
n_params = 9  # Number of parameters for transfer function model

for ch_number in range(0, 32):
    [dac_inj, ch_data] = get_long_fdt(
        "transfer_function_interpolation\input\module_long_fdts", ch_number, tau
    )

    prefix = "ch_" + str(ch_number) + "_tau_" + str(tau)
    folder_name = "all-ch_all-pts_long-fdt_module_238_-40C"
    folder_path = os.path.join(
        "transfer_function_interpolation\output", folder_name, prefix
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
