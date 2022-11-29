import sys
from interpolator import *
from fdt_formulas import tanh_5_params as t5
from fdt_formulas import tanh_8_params as t8
from fdt_formulas import tanh_9_params as t9
from get_long_fdt import *
from get_raw_fdt import *
from get_module_temperature import *

ch_number = 1
tau = 0

# [dac_inj, ch_data] = get_raw_fdt(
#     r"transfer_function_interpolation\input\raw_modules\MODULE_Napoli\1\data\TransferFunction.dat",
#     ch_number,
#     tau,
# )

[temperature] = get_module_temperature(
    r"transfer_function_interpolation\input\raw_modules\MODULE_496\1\data\HK_Temperature.dat"
)

print(temperature)
