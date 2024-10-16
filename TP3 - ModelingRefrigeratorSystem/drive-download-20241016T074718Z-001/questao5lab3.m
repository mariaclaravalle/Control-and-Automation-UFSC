clc
clear all
close all

%Questão 5

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
lb = [0; 0; 0; 0; 0; 0; 0; 0; 0];
x0 = [10; 10; 10; 10; 10; 10; 10; 10; 10];
options = optimoptions(@fmincon,'MaxFunctionEvaluations',1e6); %O argumento "'MaxFunctionEvaluations'" especifica o limite máximo de avaliações de função permitidas durante a execução do algoritmo de otimização. O valor definido é 1e6, que representa 1 milhão de avaliações de função.


We = 11.5;
tau = 5;

fun = @(x) minFun(x, Ta, Ti, Te, Tc, s, w, We, tau);

x = fmincon(fun, x0, [], [], [], [], lb, [], [], options);

Rai = x(1);
Rei = x(2);
Rec = x(3);
Rcp = x(4);
Ci = x(5);
Ce = x(6);
Cc = x(7);
gamma = x(8);
Rca = x(9);

% saídas estimadas
Ti_em = zeros(size(Ti));
Te_em = zeros(size(Te));
Tc_em = zeros(size(Tc));

% condições iniciais
Ti_em(1) = Ti(1);
Te_em(1) = Te(1);
Tc_em(1) = Tc(1);

for k=1:(length(Ta)-1)
   Ti_em(k+1) = (tau/(Ci*Rai))*Ta(k) - ((tau/(Ci*Rai))+(tau/(Ci*Rei)))*Ti_em(k) + (tau/(Ci*Rei))*Te_em(k) + (We*tau/Ci)*s(k) + Ti_em(k);
    
   Te_em(k+1) = (tau/(Ce*Rei))*Ti_em(k) - (tau/(Ce*Rei))*Te_em(k) - (tau/(Ce*Rec))*s(k)*Te_em(k) - (tau/(Ce*Rec))*s(k)*Tc_em(k) + Te_em(k);

   Tc_em(k+1) = (tau*gamma/(Cc*Rcp))*s(k)*w(k) - (tau/(Cc*Rcp))*s(k)*Tc_em(k) + (tau/(Cc*Rec))*s(k)*(Te_em(k)-Tc_em(k)) + (tau/(Cc*Rca))*(Ta(k) - Tc_em(k)) + Tc_em(k);
end

figure;

plot(tempo, Ti);
hold on
plot(tempo, Ti_em)
grid on;
title('Temperatura Interna')
legend('Real','Estimado')

figure;

plot(tempo, Te);
hold on
plot(tempo, Te_em)
grid on;
title('Temperatura Evaporador')
legend('Real','Estimado')

figure;

plot(tempo, Tc);
hold on
plot(tempo, Tc_em)
grid on;
title('Temperatura Condensador')
legend('Real','Estimado')

N = height(tempo);
aux_Ti = 0;
aux_Te = 0;
aux_Tc = 0;

for k = 1:N
    aux_Ti = aux_Ti + (Ti(k) - Ti_em(k))^2;
    aux_Te = aux_Te + (Te(k) - Te_em(k))^2;
    aux_Tc = aux_Tc + (Tc(k) - Tc_em(k))^2;
end

MSE_Ti = aux_Ti/N;
MSE_Te = aux_Te/N;
MSE_Tc = aux_Tc/N;

MAPE_Ti = 0;
MAPE_Te = 0;
MAPE_Tc = 0;

for k = 1:N
    MAPE_Ti = MAPE_Ti + abs(Ti(k) - Ti_em(k))/abs(Ti(k));
    MAPE_Te = MAPE_Te + abs(Te(k) - Te_em(k))/abs(Te(k));
    MAPE_Tc = MAPE_Tc + abs(Tc(k) - Tc_em(k))/abs(Tc(k));
end

MAPE_Ti = MAPE_Ti/N;
MAPE_Te = MAPE_Te/N;
MAPE_Tc = MAPE_Tc/N;

R2_Ti = 0;
R2_Te = 0;
R2_Tc = 0;

for k = 1:N
    R2_Ti = R2_Ti + (Ti(k) - mean(Ti_em))^2;
    R2_Te = R2_Te + (Te(k) - mean(Te_em))^2;
    R2_Tc = R2_Tc + (Tc(k) - mean(Tc_em))^2;
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