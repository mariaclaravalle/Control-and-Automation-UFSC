% Questao 1, letra a)

clc
clear all
close all

Gn = 1000; %[W/m^2] irradiação solar nominal
G = Gn; %[W/m^2] irradiação solar
Isen = 3.1656; %[A] corrente de curto-circuito nominal
Ki = 1.8*10^-3; %[A/◦C] coef. de temperatura da corrente de curto-circuito
Tn = 298; %[K] temp. nominal da célula fotovoltaica
Rp = 38.17; %[Ω] resistência paralela (shunt)
A = 1.7538; %fator de idealidade do diodo
Rs = 61.3*10^-3; %[Ω] resistência série
Is = 5.68*10^-6; %[A] corrente de saturação do diodo (valor nominal) 


k = 1.38*10^-23; %[J/K] constante de Boltzmann
q = 1.602*10^-19; %[C] carga do elétron
T = 333; %[K] temperatura da célula

tol = 0.01;
lambda = [0.1 0.5];



%potencia = [];

V = 0.6; %[V] Tensão na célula
Vt = (k*T)/q;

figure
title('Velocidade de converência do método iterativo de subrelaxamento')
xlabel('número_de_iterações','interpreter','latex')
ylabel('corrente In (A)')

ylim tight
grid on
hold on


for s = 1:length(lambda)
    %zerando parâmetros
    corrente = [];
    iteracao = [];
    var = 10*tol; 
    contador = 0;
    In = 0;
    iter = 0;

    while (abs(var) > tol && iter<=20) %visualar para ponto de tensão 0.7V onde na questão 1 os valores começam a oscilar (ver que aqui nunca converge tb)
        contador = contador +1;
        Ia = In;
        
        Ipv = (G/Gn)*(Isen+Ki*(T-Tn));
       
        Id = Is*(exp((V+Rs*Ia)/(Vt*A))-1);
      
        Ip = (V+(Rs*Ia))/Rp;
        
        In = Ipv - Id - Ip;
        In = lambda(s)*In + (1-lambda(s))*Ia;


        corrente = [corrente, In];
        iteracao = [iteracao, contador];
        
        var = In-Ia;
        iter = iter +1;
        
        
    end

plot(iteracao, corrente);

legend('lambda = 0.1', 'lambda = 0.5')


end




