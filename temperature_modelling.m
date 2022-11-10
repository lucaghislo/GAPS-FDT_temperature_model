%% This script changes all interpreters from tex to latex.
list_factory = fieldnames(get(groot,'factory'));
index_interpreter = find(contains(list_factory,'Interpreter'));
for i = 1:length(index_interpreter)
    default_name = strrep(list_factory{index_interpreter(i)},'factory','default');
    set(groot, default_name,'latex');
end


%% Acquire FDT data at different temperatures

data_sample = readtable("fdt_data_raw\TransferFunction0C.dat");
dac_inj_values = unique(data_sample.CAL_V);
channels = [0:31]; % Chosen by user
temperatures = [[-40:2:-30] [-20:10:30]];
peaking_times = [0:7];

% Acquire FDT data for all temperatures at every peaking time for every
% channel
for temp = temperatures
    data_raw_table = readtable("fdt_data_raw\TransferFunction" + string(temp) + "C.dat");
    allch_pt_fdt_means = nan(length(dac_inj_values), length(channels));
    allch_pt_fdt_stds = nan(length(dac_inj_values), length(channels));
    for pt = peaking_times
        for ch = channels
            data_raw_table_pt_ch_mean = data_raw_table.mean(data_raw_table.pt == pt & data_raw_table.ch == ch);
            data_raw_table_pt_ch_std = data_raw_table.std(data_raw_table.pt == pt & data_raw_table.ch == ch);
            allch_pt_fdt_means(:, ch+1) = data_raw_table_pt_ch_mean;
            allch_pt_fdt_stds(:, ch+1) = data_raw_table_pt_ch_std;
        end 
        % One file for every combination of peaking time and temperature
        % DAC_inj on rows, channel on columns
        writetable(array2table(allch_pt_fdt_means), "fdt_data_computed\means\fdt_allch_means_pt" + string(pt) + "_" + string(temp) + "C.dat", "Delimiter", "\t");
        writetable(array2table(allch_pt_fdt_stds), "fdt_data_computed\stds\fdt_allch_stds_pt" + string(pt) + "_" + string(temp) + "C.dat", "Delimiter", "\t");
    end
end

