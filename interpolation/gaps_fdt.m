function y = gaps_fdt(x, m1, m2, m3, m4, m5, m6, m7, m8, m9)
    y = 0.5*(k(1)*(x+k(5))+k(2)*log(cosh(k(3)*((x+k(5))-k(4)))/cosh(k(3)*k(4))))+k(6)*log(cosh(k(7)*((x-abs(k(8)))-k(9)))/cosh(k(7)*k(9)))
end
