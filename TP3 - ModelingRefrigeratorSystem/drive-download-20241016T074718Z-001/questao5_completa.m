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



%original

lb = [0; 0; 0; 0; 0; 0; 0; 0];
x0 = [10; 10; 10; 10; 10; 10; 10; 10];
options = optimoptions(@fmincon,'MaxFunctionEvaluations',1e6); %O argumento "'MaxFunctionEvaluations'" especifica o limite máximo de avaliações de função permitidas durante a execução do algoritmo de otimização. O valor definido é 1e6, que representa 1 milhão de avaliações de função.



tau = 5;

fun = @(x) minFun_original(x, Ta, Ti, Te, Tc, s, w, tau);

x = fmincon(fun, x0, [], [], [], [], lb, [], [], options);

Rai = x(1);
Rei = x(2);
Rec = x(3);
Rcp = x(4);
Ci = x(5);
Ce = x(6);
Cc = x(7);
gamma = x(8);

% saídas estimadas
Ti_em = zeros(size(Ti));
Te_em = zeros(size(Te));
Tc_em = zeros(size(Tc));

% condições iniciais
Ti_em(1) = Ti(1);
Te_em(1) = Te(1);
Tc_em(1) = Tc(1);

for k=1:(length(Ta)-1)
   Ti_em(k+1) = (tau/(Ci*Rai))*Ta(k) - ((tau/(Ci*Rai))+(tau/(Ci*Rei)))*Ti_em(k) + (tau/(Ci*Rei))*Te_em(k) + Ti_em(k);
    
   Te_em(k+1) = (tau/(Ce*Rei))*Ti_em(k) - (tau/(Ce*Rei))*Te_em(k) - (tau/(Ce*Rec))*s(k)*Te_em(k) - (tau/(Ce*Rec))*s(k)*Tc_em(k) + Te_em(k);

   Tc_em(k+1) = (tau*gamma/(Cc*Rcp))*s(k)*w(k) - (tau/(Cc*Rcp))*s(k)*Tc_em(k) + (tau/(Cc*Rec))*s(k)*(Te_em(k)-Tc_em(k)) + Tc_em(k);
end

%aperfeiçoado
lb_a = [0; 0; 0; 0; 0; 0; 0; 0; 0];
x0_a = [10; 10; 10; 10; 10; 10; 10; 10; 10];
options = optimoptions(@fmincon,'MaxFunctionEvaluations',1e6); %O argumento "'MaxFunctionEvaluations'" espeCi_afica o limite máximo de avaliações de função permitidas durante a execução do algoritmo de otimização. O valor definido é 1e6, que representa 1 milhão de avaliações de função.


We = 11.5;
tau = 5;

fun = @(x_a) minFun(x_a, Ta, Ti, Te, Tc, s, w, We, tau);

x_a = fmincon(fun, x0_a, [], [], [], [], lb_a, [], [], options);

Rai_a= x_a(1);
Rei_a = x_a(2);
Rec_a = x_a(3);
Rcp_a = x_a(4);
Ci_a= x_a(5);
Ce_a = x_a(6);
Cc_a = x_a(7);
gamma_a = x_a(8);
Rca_a= x_a(9);

% saídas estimadas
Ti_em_a = zeros(size(Ti));
Te_em_a = zeros(size(Te));
Tc_em_a = zeros(size(Tc));

% condições iniCi_aais
Ti_em_a(1) = Ti(1);
Te_em_a(1) = Te(1);
Tc_em_a(1) = Tc(1);

for k=1:(length(Ta)-1)
   Ti_em_a(k+1) = (tau/(Ci_a*Rai_a))*Ta(k) - ((tau/(Ci_a*Rai_a))+(tau/(Ci_a*Rei_a)))*Ti_em_a(k) + (tau/(Ci_a*Rei_a))*Te_em_a(k) + (We*tau/Ci_a)*s(k) + Ti_em_a(k);
    
   Te_em_a(k+1) = (tau/(Ce_a*Rei_a))*Ti_em_a(k) - (tau/(Ce_a*Rei_a))*Te_em_a(k) - (tau/(Ce_a*Rec_a))*s(k)*Te_em_a(k) - (tau/(Ce_a*Rec_a))*s(k)*Tc_em_a(k) + Te_em_a(k);

   Tc_em_a(k+1) = (tau*gamma_a/(Cc_a*Rcp_a))*s(k)*w(k) - (tau/(Cc_a*Rcp_a))*s(k)*Tc_em_a(k) + (tau/(Cc_a*Rec_a))*s(k)*(Te_em_a(k)-Tc_em_a(k)) + (tau/(Cc_a*Rca_a))*(Ta(k) - Tc_em_a(k)) + Tc_em_a(k);
end


















figure;

plot(tempo, Ti);
hold on
plot(tempo, Ti_em)
hold on
plot(tempo, Ti_em_a)
grid on;
title('Temperatura Interna')
legend('Real','Estimado', 'Aperfeiçoado')

figure;

plot(tempo, Te);
hold on
plot(tempo, Te_em)
hold on
plot(tempo, Te_em_a)
grid on;
title('Temperatura Evaporador')
legend('Real','Estimado', 'Aperfeiçoado')

figure;

plot(tempo, Tc);
hold on
plot(tempo, Tc_em)
hold on
plot(tempo, Tc_em_a)
grid on;
title('Temperatura Condensador')
legend('Real','Estimado', 'Aperfeiçoado')
