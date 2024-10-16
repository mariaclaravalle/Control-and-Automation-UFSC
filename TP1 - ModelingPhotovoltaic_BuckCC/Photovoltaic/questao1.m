% Questao 1, letra a)

Gn = 1; %[kW/m^2] irradiação solar nominal
G = Gn; %[kW/m^2] irradiação solar
Isen = 3.1656; %[A] corrente de curto-circuito nominal
Ki = 1.8*10^-3; %[A/◦C] coef. de temperatura da corrente de curto-circuito
Tn = 25; %[◦C] temp. nominal da célula fotovoltaica
Rp = 38.17; %[Ω] resistência paralela (shunt)
A = 1.7538; %fator de idealidade do diodo
Rs = 61.3*10^-3; %[Ω] resistência série
Is = 5.68*10^-6; %[A] corrente de saturação do diodo (valor nominal) 


k = 1.38*10^-23; %[J/K] constante de Boltzmann
q = 1.602*10^-19; %[C] carga do elétron
T = 0; %[◦C] temperatura da célula
Vt = (k*T)/q;


tol = 0.2;
lambda = 0.8;
In = 0;
Ia = 0;

corrente = [];
potencia = [];
V = 0:20:100;

for s = 1:length(V)
    var = 1.1;
while var > tol

    Ia = In;
    
    Ipv = (G/Gn)*(Isen+Ki*(T-Tn));
    Id = 0; %Is*exp((V(s)+Rs*Ia)/Vt*A)-1;
    Ip = (V(s)+Rs*Ia)/Rp;
    
    In = Ipv - Ip;
    In = lambda*In + (1-lambda)*Ia;
    
    var = In-Ia;
    
end

P = V(s)*In;
corrente = [corrente, In];
potencia = [potencia, P];
end

figure
plot(V, corrente)
hold on
plot(V, potencia)
grid on
legend('curva corrente','curva potencia')