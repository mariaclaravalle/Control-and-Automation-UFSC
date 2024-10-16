function ret = minFun(x, Ta, Ti, Te, Tc, s, w, tau)

Rai = x(1);
Rei = x(2);
Rec = x(3);
Rcp = x(4);
Ci = x(5);
Ce = x(6);
Cc = x(7);
gamma = x(8);


ret = 0; % erro quadrático total

% saídas estimadas
Ti_em = zeros(size(Ti));
Te_em = zeros(size(Te));
Tc_em = zeros(size(Tc));

% condições iniciais
Ti_em(1) = Ti(1);
Te_em(1) = Te(1);
Tc_em(1) = Tc(1);

beta_i = 25;
beta_e = 3;
beta_c = 2;

for k=1:(length(Ta)-1)
   Ti_em(k+1) = (tau/(Ci*Rai))*Ta(k) - ((tau/(Ci*Rai))+(tau/(Ci*Rei)))*Ti_em(k) + (tau/(Ci*Rei))*Te_em(k) + Ti_em(k);
    
   Te_em(k+1) = (tau/(Ce*Rei))*Ti_em(k) - (tau/(Ce*Rei))*Te_em(k) - (tau/(Ce*Rec))*s(k)*Te_em(k) - (tau/(Ce*Rec))*s(k)*Tc_em(k) + Te_em(k);

   Tc_em(k+1) = (tau*gamma/(Cc*Rcp))*s(k)*w(k) - (tau/(Cc*Rcp))*s(k)*Tc_em(k) + (tau/(Cc*Rec))*s(k)*(Te_em(k)-Tc_em(k)) + Tc_em(k);

    ret = ret + beta_i*(Ti(k) - Ti_em(k))^2 + beta_e*(Te(k) - Te_em(k))^2 + beta_c*(Tc(k) - Tc_em(k))^2;
end

