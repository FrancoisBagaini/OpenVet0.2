f1(x) = a1*tanh(x/b1)
a1 = 5.88; b1 = 0.81
#fit f1(x) 'poids.dat' using 1:2 via a1, b1
set term gif medium size 640,480
set output "poids.gif"
set style line 1 lt rgb "red" lw 3 pt 6
set style line 2 lt rgb "green" lw 3 pt 6
set xlabel "Age (an)"
set ylabel "Poids (Kg)"
set y2label "Taille (cm)"
set ytics nomirror
set y2tics nomirror 5
set yrange [0:10]
set y2range [0:30]
plot "poids_old.dat" using 1:2 linetype 1 smooth csplines title 'Poids' w lines axes x1y1, "poids_old.dat" using 1:3 linetype 2 title 'Taille' w lines axes x1y2
set print 'values.txt'
print GPVAL_X_MIN
print GPVAL_X_MAX
print GPVAL_Y_MIN
print GPVAL_Y_MAX
print GPVAL_TERM_XMIN
print GPVAL_TERM_XMAX
print GPVAL_TERM_YMIN
print GPVAL_TERM_YMAX
print GPVAL_TERM_XSIZE
print GPVAL_TERM_YSIZE
set output
