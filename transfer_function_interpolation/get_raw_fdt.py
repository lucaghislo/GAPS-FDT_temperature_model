import os.path
import pandas as pd
import numpy as np

# Extracts raw FDT data and feeds to intepolator function in main_caller script
def get_raw_fdt(filepath, ch_number, tau):

    # Open file in read mode
    data = pd.read_csv(
        filepath,
        sep="\t",
    )

    # Get X
    dac_inj_codes = data["CAL_V"]
    dac_inj_codes = dac_inj_codes.to_numpy()
    dac_inj_codes = np.unique(dac_inj_codes)

    # Get Y
    ch_data_all = data[(data["ch"] == ch_number) & (data["pt"] == tau)]
    ch_data = ch_data_all["mean"]
    ch_data = ch_data.to_numpy()

    return dac_inj_codes, ch_data
