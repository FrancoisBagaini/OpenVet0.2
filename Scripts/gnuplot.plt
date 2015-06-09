set term gif medium size 640,480
set output "poids.gif"
set style line 1 lt rgb "red" lw 3 pt 6
set style line 2 lt rgb "green" lw 3 pt 6
set style line 3 lt rgb "blue" lw 3 pt 6
set xlabel "Age (an)"
set ylabel "Poids (Kg)"
set ytics nomirror
set yrange [0:6]
plot "poids.dat" using 1:2 linetype 1 smooth csplines title 'Poids' w lines axes x1y1
set print 'values.txt'
print GPVAL_X_MIN
print GPVAL_X_MAX
print GPVAL_Y_MIN
print GPVAL_Y_MAX
print GPVAL_TERM_XMIN
print GPVAL_TERM_XMAX
print GPVAL_TERM_YMIN
print GPVAL_TERM_YMAX
set output