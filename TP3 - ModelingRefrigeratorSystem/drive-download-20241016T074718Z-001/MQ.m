%% Defini��o dos dados pela planilha

CtoK = 273.15; %[K] 0°C (conversão para Kelvin)

tau = 5; %[s] período de amostragem

data = xlsread('dados_20_3600.xlsx');
%load('dados_20_3600.mat')

vecTa = data(:,3) + CtoK; %[K] temperatura ambiente
vecTi = data(:,4) + CtoK; %[K] temperatura do gabinete (interna)
vecTe = data(:,5) + CtoK; %[K] temperatura do evaporador
vecTc = data(:,6) + CtoK; %[K] temperatura do condensador
vecTime = 0:tau:(length(vecTa)-1)*tau; %[s] tempo decorrido
vecFreq = data(:,54)/60; %[Hz] velocidade/frequência do compressor
vecS = zeros(size(vecFreq)); %[-] compressor em funcionamento (bool)
N = length(vecS); % número de amostras
for i=1:N
    if vecFreq(i) > 0
        vecS(i) = 1;
    end
end

%% Algoritmo - Quest�o 4
Y = [];

phi = [];

for i=1:(N-1)
    ite_phi = zeros(13, 3);
    
    ite_phi(1, 1) = vecTa(i);
    ite_phi(2, 1) = vecTi(i);
    ite_phi(3, 1) = vecTe(i);
    ite_phi(4, 1) = vecS(i);
    ite_phi(5, 2) = vecTi(i);
    ite_phi(6, 2) = vecTe(i);
    ite_phi(7, 2) = vecS(i) * vecTc(i); 
    ite_phi(8, 2) = vecS(i) * vecTe(i);
    ite_phi(9, 3) = vecS(i) * vecFreq(i);
    ite_phi(10, 3) = vecS(i) * vecTc(i);
    ite_phi(11, 3) = vecS(i) * vecTe(i); 
    ite_phi(12, 3) = vecTa(i);
    ite_phi(13, 3) = vecTc(i); 
    
    phi = [phi; transpose(ite_phi)];
  
    
    ite_y = [vecTi(i+1); vecTe(i+1); vecTc(i+1)-vecTc(i);];
    
    Y = [Y; ite_y];
end

phi_t = transpose(phi);

theta_chapeu = (inv(phi_t*phi))*phi_t*Y;

%% Simula��o do modelo discretizado com Theta chap�u - Quest�o 5
vecTi_calc = [];
vecTe_calc = [];
vecTc_calc = [];

vecTi_calc(1) = vecTi(1);
vecTe_calc(1) = vecTe(1);
vecTc_calc(1) = vecTc(1);

phi_calc = [];
Y = [];

for i=1:(N-1)
    ite_phi_calc = zeros(13, 3);
    ite_y = zeros(3, 1);
    
    ite_phi(1, 1) = vecTa(i);
    ite_phi(2, 1) = vecTi_calc(i);
    ite_phi(3, 1) = vecTe_calc(i);
    ite_phi(4, 1) = vecS(i);
    ite_phi(5, 2) = vecTi_calc(i);
    ite_phi(6, 2) = vecTe_calc(i);
    ite_phi(7, 2) = vecS(i) * vecTc_calc(i); 
    ite_phi(8, 2) = vecS(i) * vecTe_calc(i);
    ite_phi(9, 3) = vecS(i) * vecFreq(i);
    ite_phi(10, 3) = vecS(i) * vecTc_calc(i);
    ite_phi(11, 3) = vecS(i) * vecTe_calc(i); 
    ite_phi(12, 3) = vecTa(i);
    ite_phi(13, 3) = vecTc_calc(i); 
    
    phi_calc = [phi_calc; transpose(ite_phi_calc)];

    ite_y = transpose(ite_phi)*theta_chapeu;
    
    Y = [Y; ite_y];
    
    vecTi_calc(i+1) = ite_y(1, :);
    vecTe_calc(i+1) = ite_y(2, :);
    vecTc_calc(i+1) = (ite_y(3, :) + vecTc_calc(i));
end

%% Gr�ficos - Quest�o 5

figure
set(gcf,'OuterPosition',[figWidth figHeight figWidth figHeight]);
set(gcf,'name','Gr�ficos sobrepostos')
plot(vecTime/3600,vecTa-CtoK)
grid on
hold on
plot(vecTime/3600,vecTi-CtoK)
plot(vecTime/3600,vecTe-CtoK)
plot(vecTime/3600,vecTc-CtoK)

plot(vecTime/3600,vecTi_calc-CtoK)
plot(vecTime/3600,vecTe_calc-CtoK)
plot(vecTime/3600,vecTc_calc-CtoK)

plot(vecTime/3600,vecS*1e1,'-.')
plot(vecTime/3600,vecFreq*60/(1e2))
xlabel('tempo [h]','interpreter','latex')
lh = legend('Amb. [�C]','Int. [�C]','Evap. [�C]','Cond. [�C]','Int. Calc. [�C]','Evap. Calc. [�C]','Cond. Calc. [�C]', 'Estado*10','Vel./100 [RPM]');
set(lh,'interpreter','latex','location','best')

%% Quest�o 5 - b - MSE
sum_ti = 0;
sum_te = 0;
sum_tc = 0;

for i=1:N
    dif_square_ti = (vecTi(i) - vecTi_calc(i))^2;
    sum_ti = sum_ti + dif_square_ti;
    
    dif_square_te = (vecTe(i) - vecTe_calc(i))^2;
    sum_te = sum_te + dif_square_te;
    
    dif_square_tc = (vecTc(i) - vecTc_calc(i))^2;
    sum_tc = sum_tc + dif_square_tc;
end

sum_ti = sum_ti / N;
sum_te = sum_te / N;
sum_tc = sum_tc / N;

%% Quest�o 5 - b - MAPE
sum_ti_mape = 0;
sum_te_mape = 0;
sum_tc_mape = 0;

for i=1:N
    dif_perc_ti = (vecTi(i) - vecTi_calc(i))/vecTi(i);
    sum_ti_mape = sum_ti_mape + dif_perc_ti;
    
    dif_perc_te = (vecTe(i) - vecTe_calc(i))/vecTe(i);
    sum_te_mape = sum_te_mape + dif_perc_te;
    
    dif_perc_tc = (vecTc(i) - vecTc_calc(i))/vecTc(i);
    sum_tc_mape = sum_tc_mape + dif_perc_tc;
end

sum_ti_mape = sum_ti_mape * 100 / N;
sum_te_mape = sum_te_mape * 100 / N;
sum_tc_mape = sum_tc_mape * 100 / N;

%% Quest�o 5 - b - R^2
sum_ti_err = 0;
sum_te_err = 0;
sum_tc_err = 0;

sum_ti_dev = 0;
sum_te_dev = 0;
sum_tc_dev = 0;

for i=1:N
    err_ti = (vecTi(i) - vecTi_calc(i))^2;
    sum_ti_err = sum_ti_err + err_ti;
    
    err_te = (vecTe(i) - vecTe_calc(i))^2;
    sum_te_err = sum_te_err + err_te;
    
    err_tc = (vecTc(i) - vecTc_calc(i))^2;
    sum_tc_err = sum_tc_err + err_tc;
    
    
    dev_ti = (vecTi(i) - mean(vecTi_calc))^2;
    sum_ti_dev = sum_ti_dev + dev_ti;
    
    dev_te = (vecTe(i) - mean(vecTe_calc))^2;
    sum_te_dev = sum_te_dev + dev_te;
    
    dev_tc = (vecTc(i) - mean(vecTc_calc))^2;
    sum_tc_dev = sum_tc_dev + dev_tc;
end

ti_Rsquare = 1-(sum_ti_err / sum_ti_dev);
te_Rsquare = 1-(sum_te_err / sum_te_dev);
tc_Rsquare = 1-(sum_tc_err / sum_tc_dev);

%% Quest�o 6
x0 = 1e1*ones(8,1);
lb = zeros(8,1); % limite inferior dos parâmetros
options = optimoptions(@fmincon,'MaxFunctionEvaluations',1e6);

x = fmincon(@(x) funMin(x,vecTi, vecTe, vecTc, vecTa, vecS, vecFreq, tau, 5, 4, 3),x0,[],[],[],[],lb,[],[],options);

%% Quest�o 6 - gr�ficos

vecTi_em = [];
vecTe_em = [];
vecTc_em = [];

vecTi_em(1) = vecTi(1);
vecTe_em(1) = vecTe(1);
vecTc_em(1) = vecTc(1);

phi_calc = [];
Y = [];

Rai = x(1);
Rei = x(2);
Rec = x(3);
Rcp = x(4);
Ci = x(5);
Ce = x(6);
Cc = x(7);
gamma = x(8);

theta = [];
theta(1, 1) = tau / (Ci * Rai);
theta(2, 1) = (1 - tau/(Rai*Ci) - tau/(Rei*Ci));
theta(3, 1) = tau/(Rei * Ci);
theta(4, 1) = tau/(Ce * Rei);
theta(5, 1) = (1 - tau/(Rei*Ce));
theta(6, 1) = - tau/(Rec * Ce);
theta(7, 1) = - tau/(Rec * Ce);
theta(8, 1) = 1;
theta(9, 1) = (tau*gamma)/(Cc * Rcp);
theta(10, 1) = - (tau/(Rcp*Cc) + tau/(Rec*Cc));
theta(11, 1) = tau/(Rec * Cc);

for i=1:(N-1)
    ite_phi = zeros(11, 3);
    ite_y = zeros(3, 1);
    
    ite_phi(1, 1) = vecTa(i);
    ite_phi(2, 1) = vecTi_em(i);
    ite_phi(3, 1) = vecTe_em(i);
    ite_phi(4, 2) = vecTi_em(i);
    ite_phi(5, 2) = vecTe_em(i);
    ite_phi(6, 2) = vecS(i) * vecTc_em(i); 
    ite_phi(7, 2) = vecS(i) * vecTe_em(i);
    ite_phi(8, 3) = vecTc_em(i);
    ite_phi(9, 3) = vecS(i) * vecFreq(i);
    ite_phi(10, 3) = vecS(i) * vecTc_em(i);
    ite_phi(11, 3) = vecS(i) * vecTe_em(i); 
    
    phi_calc = [phi_calc; transpose(ite_phi_calc)];

    ite_y = transpose(ite_phi)*theta;
    
    Y = [Y; ite_y];
    
    vecTi_em(i+1) = ite_y(1, :);
    vecTe_em(i+1) = ite_y(2, :);
    vecTc_em(i+1) = (ite_y(3, :) + vecTc_em(i));
end

figure
set(gcf,'OuterPosition',[figWidth figHeight figWidth figHeight]);
set(gcf,'name','Gr�ficos sobrepostos')
plot(vecTime/3600,vecTa-CtoK)
grid on
hold on
plot(vecTime/3600,vecTi-CtoK)
plot(vecTime/3600,vecTe-CtoK)
plot(vecTime/3600,vecTc-CtoK)

plot(vecTime/3600,vecTi_em-CtoK)
plot(vecTime/3600,vecTe_em-CtoK)
plot(vecTime/3600,vecTc_em-CtoK)

plot(vecTime/3600,vecS*1e1,'-.')
plot(vecTime/3600,vecFreq*60/(1e2))
xlabel('tempo [h]','interpreter','latex')
lh = legend('Amb. [�C]','Int. [�C]','Evap. [�C]','Cond. [�C]','Int. Calc. [�C]','Evap. Calc. [�C]','Cond. Calc. [�C]', 'Estado*10','Vel./100 [RPM]');
set(lh,'interpreter','latex','location','best')
