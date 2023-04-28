# Set the plotting style to pm3d
#set pm3d
set pm3d map
set terminal png size 1100,600
set output 'test.png'

# Define the color palette for positive and negative values
#set palette defined (-20000 "black",-10000 "purple",-1 "red", 0 "white", 1 "blue" ,10000 "green" ,20000 "white")

# Set the x and y axis ranges and resolution
set xrange [0:100]
set xlabel "year"
set yrange [0:100]
set ylabel "m^2"
set samples 1000
set isosamples 1000

# Generate the data to plot
f(x,y) = x + y -10
set table 'test.txt'
splot f(x,y)
unset table

# Plot the data as a contour map
set view map
splot 'test.txt' with pm3d

