function y = f(m1, m2, m3, m4, m5, m6, m7, m8, m9)
y = 0.5*(m1*(x+m5)+m2*ln(cosh(m3*((x+m5)-m4))/cosh(m3*m4)))+m6*ln(cosh(m7*((x-abs(m8))-m9))/cosh(m7*m9));