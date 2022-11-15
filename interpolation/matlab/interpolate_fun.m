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

x_short = dac_inj_values;
y_short_raw = readtable("C:\Users\ghisl\Documents\GitHub\GAPS-FDT_temperature_model\fdt_data_computed\means\fdt_allch_means_pt0_0C.dat");
y_short_raw = table2array(y_short_raw);
y_short = y_short_raw(:, 1);

x_long_raw = readtable("fdt_data_raw\module_-40C\dac_values-long.dat");
x_long = table2array(x_long_raw);
y_long_raw = readtable("fdt_data_raw\module_-40C\fdt_allch_pt4.dat"); % PT 4
y_long_raw = table2array(y_long_raw);
y_long = y_long_raw(:, 1);



%% Calculate gain

dydx_short = gradient(y_short) ./ gradient(x_short);
dydx_long = gradient(y_long) ./ gradient(x_long);

f = figure("Visible", "on")
hold on
plot(x_short, 1/dydx_short)
plot(x_long, 1/dydx_long)
hold off
set(gca, 'YScale', 'log')
set(gca, 'XScale', 'log')


%% Interpolate function

fit_function = '0.5*(m1*(x+m5)+m2*log(cosh(m3*((x+m5)-m4))/cosh(m3*m4)))+m6*log(cosh(m7*((x-abs(m8))-m9))/cosh(m7*m9))';

fit_type = fittype(fit_function, 'dependent', {'y'}, 'independent', {'x'}, 'coefficients', {'m1','m2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9'})

my_fit = fit(x_short, y_short, fit_type);


%% Build dataset for non-linear interpolation

% Small sample
t = x_short;
y = sqrt(1./dydx_short)

f = figure("Visible", "on")
plot(t, y);
set(gca, 'YScale', 'log')
set(gca, 'XScale', 'log')

% Big sample
t = x_long;
y = sqrt(1./dydx_long)


%% Non-linear interpolation using nlinfit

beta0 = [0, 0, 0, 0, 0, 0, 0, 0, 0];

modelfun = @(k,x)0.5*(k(1)*(x+k(5))+k(2)*log(cosh(k(3)*((x+k(5))-k(4)))/cosh(k(3)*k(4))))+k(6)*log(cosh(k(7)*((x-abs(k(8)))-k(9)))/cosh(k(7)*k(9)))

beta = nlinfit(x_short, y_short, modelfun, beta0)


%% Non-linear interpolation using lsqcurvefit

x0 = [41339, 16961, 2.3, 1.3, -0.3, 10000, 5, 0.3, 1];

% 0.5*(m1*(m0+m5)+m2*ln(cosh(m3*((m0+m5)-m4))/cosh(m3*m4)))+m6*ln(cosh(m7*((m0-abs(m8))-m9))/cosh(m7*m9)); 
% m1 = 41339; m2 = 16961; m3=2.3; m4=1.3; m5=-0.3; m6=10000; m7=5; m8=0.3; m9=1; m10=1
F = @(x, xdata)0.5*(x(1)*(xdata+x(5))+x(2)*log(cosh(x(3)*((xdata+x(5)-x(4)))/cosh(x(3)*x(4)))))+x(6)*log(cosh(x(7)*((xdata-abs(x(8)))-x(9)))/cosh(x(7)*x(9)))
%F = @(x, xdata)0.5*(x(1)*(xdata+x(5))+x(2)*log(cosh(x(3)*((xdata+x(5)-x(4)))/cosh(x(3)*x(4)))))

t = t(1:end);
y = y(1:end);

[x,resnorm,~,exitflag,output] = lsqcurvefit(F, x0, t, y)


%% Prova con formula paper

x0 = [0, 0, 0, 0];

F = @(x, xdata)0.5*(x(1)+x(2))*xdata+(x(1)-x(2))/(2*x(3)*cosh(x(3)*x(4)))*log(cosh(x(3)*(xdata-x(4))))

t = t(10:end);
y = y(10:end);

[x,resnorm,~,exitflag,output] = lsqcurvefit(F, x0, t, y)


%% Plot fit result

% Valori ottenuti
x(1) = 41339;
x(2) = 16961;
x(3) = 2.3;
x(4) = 1.3;
x(5) = -0.3;
x(6) = 10000;
x(7) = 5;
x(8) = 0.3;
x(9) = 1;
x(10) = 1;

f = figure("Visible", "on");
hold on
plot(t, y)
plot(t, F(x, t))
hold off
set(gca, 'YScale', 'log')
set(gca, 'XScale', 'log')