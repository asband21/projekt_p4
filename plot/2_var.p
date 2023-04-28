# Set the plotting style to pm3d
set pm3d
set terminal png size 1100,600
set output 'biglig_5.png'

# Define the color palette for positive and negative values
#set palette defined (-20000 "black",-10000 "purple",-1 "red", 0 "white", 1 "blue" ,10000 "green" ,20000 "white")
set palette defined (0 "black",0.1 "purple",0.150 "red", 0.1501 "blue" ,0.8 "green" ,1 "white")

# Set the x and y axis ranges and resolution
set xrange [0:10]
set xlabel "year"
set yrange [0:1000000]
set ylabel "m^2"
set samples 1000
set isosamples 1000

# Generate the data to plot
f(x,y) = (x*y*541.9) - (44997.39024*x + 0.01720393233*x*y + 0.07741769547*y + 14627)
set table 'data.txt'
splot f(x,y)
unset table

# Plot the data as a contour map
set view map
splot 'data.txt' with pm3d

