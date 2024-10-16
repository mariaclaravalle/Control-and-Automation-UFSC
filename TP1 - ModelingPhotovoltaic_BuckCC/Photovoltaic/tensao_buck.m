function dVodt = tensao_buck (C, R, iL, Vo, x)

tensao = x(1);
tensao_d = x(2);

dVo1dt = tensao_d;

dVo2dt = (iL/C - tensao/R*C);

dVodt = [dVo1dt; dVo2dt];

end