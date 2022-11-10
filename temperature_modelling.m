%% This script changes all interpreters from tex to latex.
clear; clc;

list_factory = fieldnames(get(groot,'factory'));
index_interpreter = find(contains(list_factory,'Interpreter'));
for i = 1:length(index_interpreter)
    default_name = strrep(list_factory{index_interpreter(i)},'factory','default');
    set(groot, default_name,'latex');
end


%% Acquire FDT data at different temperatures
clear; clc;

data_sample = readtable("fdt_data_raw\TransferFunction0C.dat");
dac_inj_values = unique(data_sample.CAL_V);
channels = [0:31];
temperatures = [[-40:2:-30] [-20:10:30]];
peaking_times = [0:7];
conv_factor = 0.841;
fontsize = 12;
save config_values.mat dac_inj_values channels temperatures peaking_times conv_factor fontsize;

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


%% Plot FDTs at different temperatures and peaking times
clear; clc;
load("config_values.mat")
plots_dir_path = "plots\";

% All channels at each peaking time and temperature
if length(channels) > 1
    channels_subfolder_path = plots_dir_path + "channels_" + string(channels(1)) + "-" + string(channels(end)) + "\";
else
    channels_subfolder_path = plots_dir_path + "channel_" + string(channels(1)) + "\";
end
if ~exist(channels_subfolder_path, 'dir')
    mkdir(channels_subfolder_path);
end
for temp = temperatures
    temperatures_subfolder_path = channels_subfolder_path + string(temp)  + "C\";
    if ~exist(temperatures_subfolder_path, 'dir')
        mkdir(temperatures_subfolder_path);
    end
    for pt = peaking_times
        data_raw_table = readtable("fdt_data_computed\means\fdt_allch_means_pt" + string(pt) + "_" + string(temp) + "C.dat");
        data_raw = table2array(data_raw_table);
        f = figure("Visible", "off");
        hold on
        for ch = channels
            plot(dac_inj_values.*conv_factor, data_raw(:, ch+1));
        end
        hold off
        box on
        grid on
        xlabel('\textbf{Incoming energy [MeV]}');
        ylabel('\textbf{Channel Output [ADU]}');
        ylim([0 2000])
        xlim([0, 53824]);
        xticks([0:10000:50000])
        xticklabels([0:10:50])
        yticks([0:200:2000])
        set(gcf, 'Color', 'w');
        if length(channels) > 1
            filename = "fdt_plot_ch" + string(channels(1)) + "-" + string(channels(end)) + "_pt" + string(pt) +  "_" + string(temp) + "C.pdf";
            title("\textbf{Transfer function of channels " + string(channels(1)) + " - " + string(channels(end)) + " at \boldmath$" + string(temp) + "^{\circ}$C and \boldmath$\tau_{p} = $ " + string(pt) + "}");
        else
            filename = "fdt_plot_ch" + string(channels(1)) + "_pt" + string(pt) +  "_" + string(temp) + "C.pdf";
            title("\textbf{Transfer function of channel " + string(channels(1)) + " at \boldmath$" + string(temp) + "^{\circ}$C and \boldmath$\tau_{p} = $ " + string(pt) + "}");
        end
        ax = gca; 
        ax.XAxis.FontSize = fontsize; 
        ax.YAxis.FontSize = fontsize;
        ax.Title.FontSize = fontsize + 4;
        f.Position = [0 0 1200 800];
        
        exportgraphics(gcf, temperatures_subfolder_path + filename);
        disp("SAVED: " + filename);
    end
end


%% Analisi della variazione dell'uscita del canale
% Analisi del valore dell'uscita del canale in funzione della temperatura
% mantenendo fisso il canale, il valore dell'energia in ingresso ed il
% tempo di picco

clear; clc;
load("config_values.mat")
colors = distinguishable_colors(length(dac_inj_values), 'w');

ch = 13;
pt = 6;
DAC_inj = 400;

channel_output = nan(length(temperatures), length(dac_inj_values));
temp_counter = 0;
for temp = temperatures
    data_raw_table = readtable("fdt_data_computed\means\fdt_allch_means_pt" + string(pt) + "_" + string(temp) + "C.dat");
    data_raw = table2array(data_raw_table);
    dac_inj_counter = 0;
    for dac_inj = dac_inj_values'
        channel_output(temp_counter+1, dac_inj_counter+1) = data_raw(find(dac_inj_values == dac_inj), ch+1); %#ok<FNDSB> 
        dac_inj_counter = dac_inj_counter + 1;
    end
    temp_counter = temp_counter + 1;
end

f = figure("Visible", "on");
colororder([colors(:, 1), colors(:, 2), colors(:, 3)]);
plot(temperatures, channel_output);
legend(string(dac_inj_values), "Location", "eastoutside", "NumColumns", 2);
