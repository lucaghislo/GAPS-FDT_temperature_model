%% This script changes all interpreters from tex to latex.
clear; clc;

list_factory = fieldnames(get(groot,'factory'));
index_interpreter = find(contains(list_factory,'Interpreter'));
for i = 1:length(index_interpreter)
    default_name = strrep(list_factory{index_interpreter(i)},'factory','default');
    set(groot, default_name,'latex');
end


%% Upload data

clear; clc;
load config_values.mat

x = dac_inj_values;
data_raw = readtable("C:\Users\ghisl\Documents\GitHub\GAPS-FDT_temperature_model\fdt_data_computed\means\fdt_allch_means_pt0_0C.dat");
data_raw = table2array(data_raw);
y = data_raw(:, 1);

%% Define system

syms x m1 m2 m3 m4 m5 m6 m7 m8 m9
vpasolve(f, m1, m2, m3, m4, m5, m6, m7, m8, m9)

