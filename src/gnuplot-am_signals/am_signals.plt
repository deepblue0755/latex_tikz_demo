# set the terminal
# set terminal svg size 800 600 dynamic enhanced
set term pdfcairo lw 3 font "Times New Roman,8"

# set the output file
# set output "am_signals.svg"
set output "am_signals.pdf"

# describe the formula (x indicates time)
f(x) = (1 + m*sin(2*pi*100*x))*sin(2*pi*10000*x)
u=1.0

# set the 'default' axes properties 
set xlabel " "
set ylabel "Amplitude"
set grid
unset key

# start multiplot
set multiplot

# 50% Modulation
set origin 0,0.66*u
set title "50% Modulation"
set size 1*u,0.33*u
plot m=0.5, f(x)

# 100% Modulation
set origin 0,0.33*u
set size 1*u,0.33*u
set title "100% Modulation"
plot m=1, f(x)

# 150% Modulation"
set origin 0,0
set size 1*u,0.33*u
set xlabel "time"
plot m=1.5, f(x)

# end plotting
unset multiplot
unset output
