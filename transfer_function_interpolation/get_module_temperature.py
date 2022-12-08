import os.path
import pandas as pd
import numpy as np

# Extracts raw FDT data and feeds to intepolator function in main_caller script
def get_module_temperature(filepath):

    # Open file in read mode
    data = pd.read_csv(filepath, sep="\t", skiprows=45, names=["Index", "Temperature"])
    data_code = data["Temperature"]
    mean_code = np.mean(data_code.to_numpy())

    V_T = 0.9 * 1000 - (mean_code - 1024) * 1.72 / (3.87)
    T = 30 + (5.506 - np.sqrt((-5.506) ** 2 + 4 * 0.00172 * (870.6 - V_T))) / (2 * (-0.00172))

    return [np.round(T, 1)]
