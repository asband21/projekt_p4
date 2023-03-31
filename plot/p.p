set pm3d
set palette defined (-10000 "blue",-1 "blue", 0 "white", 1 "red" ,10000 "red")

set xrange [0:10]
set xlabel "yer"
set yrange [0:1000000]
set ylabel "m^2"

set samples 1000
set isosamples 1000

f(x,y) = (x * y * 541.9) - (44997.39024*x + 0.05161179698*x*y + 0.2322530864*y + 14627)

splot f(x,y)
set view map
splot f(x,y) with pm3d
