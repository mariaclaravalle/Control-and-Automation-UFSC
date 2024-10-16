clc
clear all
close all

data = readtable('C:\Users\maria\Downloads\dados_20_2400.xlsx');
data.Properties.VariableNames([16 19 30 35 42 52]) = {'Tempo' 'T_cond_mid' 'T_int_avg' 'T_evap_mid' 'T_abm_avg' 'RPM'};
tempo = data.('Tempo');
Tc = data.('T_cond_mid');
Ti = data.('T_int_avg');
Te = data.('T_evap_mid');
Ta = data.('T_abm_avg');
w = data.('RPM');
s = data.('RPM');

for m = 1:height(s)
    if s(m) ~= 0
        s(m) = 1;
    end
end

N = height(tempo);

y = [];
phi = [];

tau = 5;
for i = 2:N
    y = [y; 
        Ti(i) - Ti(i-1); 
        Te(i) - Te(i-1); 
        Tc(i) - Tc(i-1)];

    phi = [phi; 
           Ta(i), Ti(i), Te(i), 11.5*s(i),0, 0, 0, 0, 0, 0, 0, 0; 
           0, 0, 0, 0,  Ti(i), Te(i), s(i)*Te(i), s(i)*Tc(i), 0, 0, 0, 0; 
           0, 0, 0, 0, 0, 0, 0, 0, s(i)*w(i), Tc(i), s(i)*(Te(i)-Tc(i)), Ta(i)-Tc(i)];
end

theta = (inv(transpose(phi)*phi))*transpose(phi)*y;

Ti_e = zeros(size(Ti));
Te_e = zeros(size(Te));
Tc_e = zeros(size(Tc));

Ti_e(1) = Ti(1);
Te_e(1) = Te(1);
Tc_e(1) = Tc(1);
phi_e = [];

for i = 2:N

    Ti_e(i) = phi(1+3*(i-2),:)*theta + Ti_e(i-1);
    Te_e(i) = phi(2+3*(i-2),:)*theta + Te_e(i-1);
    Tc_e(i) = phi(3+3*(i-2),:)*theta + Tc_e(i-1);
end

figure;

plot(tempo, Ti);
hold on
plot(tempo, Ti_e)
grid on;
title('Temperatura Interna')
legend('Real','Estimado')

figure;

plot(tempo, Te);
hold on
plot(tempo, Te_e)
grid on;
title('Temperatura Evaporador')
legend('Real','Estimado')

figure;

plot(tempo, Tc);
hold on
plot(tempo, Tc_e)
grid on;
title('Temperatura Condensador')
legend('Real','Estimado')

aux_Ti = 0;
aux_Te = 0;
aux_Tc = 0;

for k = 1:N
    aux_Ti = aux_Ti + (Ti(k) - Ti_e(k))^2;
    aux_Te = aux_Te + (Te(k) - Te_e(k))^2;
    aux_Tc = aux_Tc + (Tc(k) - Tc_e(k))^2;
end

MSE_Ti = aux_Ti/N;
MSE_Te = aux_Te/N;
MSE_Tc = aux_Tc/N;

MAPE_Ti = 0;
MAPE_Te = 0;
MAPE_Tc = 0;

for k = 1:N
    MAPE_Ti = MAPE_Ti + abs(Ti(k) - Ti_e(k))/abs(Ti(k));
    MAPE_Te = MAPE_Te + abs(Te(k) - Te_e(k))/abs(Te(k));
    MAPE_Tc = MAPE_Tc + abs(Tc(k) - Tc_e(k))/abs(Tc(k));
end

MAPE_Ti = MAPE_Ti/N;
MAPE_Te = MAPE_Te/N;
MAPE_Tc = MAPE_Tc/N;

R2_Ti = 0;
R2_Te = 0;
R2_Tc = 0;

for k = 1:N
    R2_Ti = R2_Ti + (Ti(k) - mean(Ti_e))^2;
    R2_Te = R2_Te + (Te(k) - mean(Te_e))^2;
    R2_Tc = R2_Tc + (Tc(k) - mean(Tc_e))^2;
end

R2_Ti = 1 - aux_Ti/R2_Ti;
R2_Te = 1 - aux_Te/R2_Te;
R2_Tc = 1 - aux_Tc/R2_Tc;


fprintf('MSE_Ti is %4.3f\n', MSE_Ti)
fprintf('MSE_Te is %4.3f\n', MSE_Te)
fprintf('MSE_Tc is %4.3f\n', MSE_Tc)

fprintf('MAPE_Ti is %4.3f\n', MAPE_Ti)
fprintf('MAPE_Te is %4.3f\n', MAPE_Te)
fprintf('MAPE_Tc is %4.3f\n', MAPE_Tc)

fprintf('R2_Ti is %4.3f\n', R2_Ti)
fprintf('R2_Te is %4.3f\n', R2_Te)
fprintf('R2_Tc is %4.3f\n', R2_Tc)