%% This script changes all interpreters from tex to latex.
list_factory = fieldnames(get(groot,'factory'));
index_interpreter = find(contains(list_factory,'Interpreter'));
for i = 1:length(index_interpreter)
    default_name = strrep(list_factory{index_interpreter(i)},'factory','default');
    set(groot, default_name,'latex');
end


%% Acquire FDT data at different temperatures

data_sample = readtable("C:\Users\ghisl\Documents\GitHub\GAPS-FDT_temperature_model\fdt_data_temp\TransferFunction0C.dat");
dac_inj_values = unique(data_sample.CAL_V);
channels = [0:31]; % Chosen by user
temperatures = [[-40:2:-30] [-20:10:30]];
peaking_times = [0:7];

% Acquire FDT data for all temperatures at every peaking time for every
% channel
for temp = temperatures
    data_raw_table = readtable("C:\Users\ghisl\Documents\GitHub\GAPS-FDT_temperature_model\fdt_data_temp\TransferFunction" + string(temp) + "C.dat");
    for pt = peaking_times
        
    end
end


