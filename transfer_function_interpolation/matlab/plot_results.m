%% This script changes all interpreters from tex to latex.
clear; clc;

list_factory = fieldnames(get(groot,'factory'));
index_interpreter = find(contains(list_factory,'Interpreter'));
for i = 1:length(index_interpreter)
    default_name = strrep(list_factory{index_interpreter(i)},'factory','default');
    set(groot, default_name,'latex');
end

%% Load data

clear; clc;

tau = 6;
data_folder = "C:\Users\ghisl\Documents\GitHub\GAPS-FDT_temperature_model\transfer_function_interpolation\output\all-ch_all-pts_long-fdt_module_238_-40C";
residuals = readtable(data_folder + "\all_residuals_tau_" + string(tau) + "_8_params.dat", "ReadVariableNames", false);
resolution = readtable(data_folder + "\all_resolution_tau_" + string(tau) + "_8_params.dat", "ReadVariableNames", false);

residuals = table2array(residuals);
resolution = table2array(resolution);

residuals = residuals(:);
resolution = resolution(:);

f = figure("Visible", "on")
scatter(resolution, residuals, "filled", "o")
grid on
box on
xlabel("Resolution [keV]")
ylabel("Residuals [keV]")
title("\textbf{Residuals vs Resolution}")

% set(gca, 'YScale', 'log')
% set(gca, 'XScale', 'log')

ax = gca; 
fontsize = 12;
ax.XAxis.FontSize = fontsize; 
ax.YAxis.FontSize = fontsize;
ax.Title.FontSize = fontsize + 4;
f.Position = [0 0 1200 800];

exportgraphics(gcf, "C:\Users\ghisl\Documents\GitHub\GAPS-FDT_temperature_model\transfer_function_interpolation\matlab\" + ...
    "result_plots\residuals_vs_resolution_lin.pdf");