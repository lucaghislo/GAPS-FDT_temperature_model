import os.path

# Extracts long FDT data and feeds to intepolator function in main_caller script
def get_long_fdt(filepath, ch_number, tau):

    data_filepath = os.path.join(filepath, "fdt_allch_pt" + str(tau) + ".dat")

    # Open file in read mode
    f_data = open(data_filepath, "r")
    data_lines = f_data.readlines()
    data = []

    # Extract data
    for x in data_lines[1 : len(data_lines)]:
        data.append(float(x.split("\t")[ch_number]))

    f_data.close()

    dac_inj_filepath = os.path.join(filepath, "dac_values.dat")

    # Import DAC_inj_code steps
    f_dac_inj = open(dac_inj_filepath, "r")
    dac_inj_lines = f_dac_inj.readlines()
    dac_inj = []

    # Extract data
    for x in dac_inj_lines[1 : len(dac_inj_lines)]:
        dac_inj.append(float(x.split("\t")[0]))

    f_dac_inj.close()

    return dac_inj, data
