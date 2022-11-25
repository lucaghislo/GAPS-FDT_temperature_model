import sys
from interpolator import *
from fdt_formulas import tanh_5_params as t5
from fdt_formulas import tanh_8_params as t8
from fdt_formulas import tanh_9_params as t9
from get_long_fdt import *


for ch_number in range(0, 32):
    [dac_inj, ch_data] = get_long_fdt(
        "transfer_function_interpolation\input\module_long_fdts", ch_number
    )

    prefix = "ch_" + str(ch_number)
    folder_path = os.path.join(
        "transfer_function_interpolation\output\module_channels_analysis", prefix
    )

    ch_data = ch_data[1 : len(ch_data)]
    dac_inj = dac_inj[1 : len(dac_inj)]

    # Config
    fdt = t8.gaps_fdt_tanh_8_params
    guess = t8.weights_fdt_tanh_8_params
    n_params = 8

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
