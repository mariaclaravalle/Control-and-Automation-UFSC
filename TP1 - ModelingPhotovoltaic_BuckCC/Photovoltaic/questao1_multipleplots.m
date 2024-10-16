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
T = [273 298 333]; %[K] temperatura da célula

tol = 0.001;
lambda = 0.3;
In = 0;

corrente = [];
potencia = [];
V = 0:0.01:0.8; %[V] Tensão na célula

figure
title('Célula fotovoltaica com irradiação G = 1000 W/m^2')
xlabel('tensão [V]','interpreter','latex')
ylabel('potência [W]')
ylim([0 1.2])
grid on
hold on

%potencia variando temp
for c = 1:length(T)
    corrente = [];
    potencia = [];
    Vt = (k*T(c))/q;

    for s = 1:length(V)
        var = 10*tol;
        iter = 0;
        while (abs(var) > tol && iter <= 1000)
        
            Ia = In;
            
            Ipv = (G/Gn)*(Isen+Ki*(T(c)-Tn));
           
            Id = Is*(exp((V(s)+Rs*Ia)/(Vt*A))-1);
          
            Ip = (V(s)+(Rs*Ia))/Rp;
            
            In = Ipv - Id - Ip;
            In = lambda*In + (1-lambda)*Ia;
            
            var = In-Ia;
            iter = iter +1;
            
        end
    
    P = V(s)*In;
    corrente = [corrente, In];
    potencia = [potencia, P];
    end


plot(V, potencia);
legend('0◦C','25◦C', '60◦C')

end




%corrente variando temp---------------------------------------------------
figure
title('Célula fotovoltaica com irradiação G = 1000 W/m^2')
xlabel('tensão [V]','interpreter','latex')
ylabel('corrente [A]')
ylim tight
grid on
hold on


for c = 1:length(T)
    corrente = [];
    potencia = [];
    Vt = (k*T(c))/q;

    for s = 1:length(V)
        var = 10*tol;
        iter = 0;
        while (abs(var) > tol && iter <= 1000)
        
            Ia = In;
            
            Ipv = (G/Gn)*(Isen+Ki*(T(c)-Tn));
           
            Id = Is*(exp((V(s)+Rs*Ia)/(Vt*A))-1);
          
            Ip = (V(s)+(Rs*Ia))/Rp;
            
            In = Ipv - Id - Ip;
            In = lambda*In + (1-lambda)*Ia;
            
            var = In-Ia;
            iter = iter +1;
            
        end
    
    P = V(s)*In;
    corrente = [corrente, In];
    potencia = [potencia, P];
    end


plot(V, corrente);
legend('0◦C','25◦C', '60◦C')

end

%corrente variando irradiação---------------------------------------------------
T = Tn;
G = [200 500 1000];




figure
title('Célula fotovoltaica com temperatura T = 25 °C')
xlabel('tensão [V]','interpreter','latex')
ylabel('corrente [A]')
ylim tight
grid on
hold on 


for c = 1:length(G)
    corrente = [];
    potencia = [];
    Vt = (k*T)/q;

    for s = 1:length(V)
        var = 10*tol;
        iter = 0;
        while (abs(var) > tol && iter <= 1000)
        
            Ia = In;
            
            Ipv = (G(c)/Gn)*(Isen+Ki*(T-Tn));
           
            Id = Is*(exp((V(s)+Rs*Ia)/(Vt*A))-1);
          
            Ip = (V(s)+(Rs*Ia))/Rp;
            
            In = Ipv - Id - Ip;
            In = lambda*In + (1-lambda)*Ia;
            
            var = In-Ia;
            iter = iter +1;
            
        end
    
    P = V(s)*In;
    corrente = [corrente, In];
    potencia = [potencia, P];
    end


plot(V, corrente);
legend('200 W/m^2','500 W/m^2', '1000 W/m^2')

end


%potencia variando irradiação---------------------------------------------------
T = Tn;
G = [200 500 1000];




figure
title('Célula fotovoltaica com temperatura T = 25 °C')
xlabel('tensão [V]','interpreter','latex')
ylabel('potência [W]')
ylim([0 1])
grid on
hold on


for c = 1:length(G)
    corrente = [];
    potencia = [];
    Vt = (k*T)/q;

    for s = 1:length(V)
        var = 10*tol;
        iter = 0;
        while (abs(var) > tol && iter <= 1000)
        
            Ia = In;
            
            Ipv = (G(c)/Gn)*(Isen+Ki*(T-Tn));
           
            Id = Is*(exp((V(s)+Rs*Ia)/(Vt*A))-1);
          
            Ip = (V(s)+(Rs*Ia))/Rp;
            
            In = Ipv - Id - Ip;
            In = lambda*In + (1-lambda)*Ia;
            
            var = In-Ia;
            iter = iter +1;
            
        end
    
    P = V(s)*In;
    corrente = [corrente, In];
    potencia = [potencia, P];
    end


plot(V, potencia);
legend('200 W/m^2','500 W/m^2', '1000 W/m^2')

end


%cuidar com título do gráfico e eixos


