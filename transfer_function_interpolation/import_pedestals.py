import os.path
import pandas as pd
import numpy as np


def import_pedestals(filepath, ch_number, tau):

    # Open file in read mode
    data = pd.read_csv(
        filepath,
        sep="\t",
    )

    # Get Y
    ch_data_all = data[(data["ch"] == ch_number) & (data["pt"] == tau)]
    ch_data = ch_data_all["mean"]
    ch_data = ch_data.to_numpy()

    return ch_data
