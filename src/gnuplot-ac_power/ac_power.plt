set term pdfcairo lw 2 font "Times New Roman,8"
set output "ac_power.pdf"
Um = 1.8
Im = 1.3
w = 1
fi = 0.8

u(t) = Um * sin(w*t + fi)
i(t) = Im * sin(w*t)
p(t) = u(t) * i(t)

set xrange[-fi-0.3:8]
set xtics ("0" 0, "-fi" -fi, "pi/2" pi/2, "pi" pi, "3pi/2" 3*pi/2, "2pi" 2*pi, "5pi/2" 5*pi/2)
set ytics ("Um" Um, "Im" Im, "0" 0, "-Um" -Um, "-Im" -Im)
set xzeroaxis
set yzeroaxis
set key bottom right

plot u(x) t "u(t)", i(x) t "i(t)", p(x) t "p(t)"
