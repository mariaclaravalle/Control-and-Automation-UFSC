function diLdt = corrente_indutor(Vi, L, D, Vo, x)

diL2dt = (D*Vi/L) - Vo/L;

diLdt = [diL2dt];

end