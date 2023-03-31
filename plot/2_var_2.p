# Set the plotting style to pm3d
set pm3d

# Define the color palette for positive and negative values
set palette defined (-10000 "blue",-1 "blue", 0 "white", 1 "red" ,10000 "red")

# Set the x and y axis ranges and resolution
set xrange [0:10]
set xlabel "yer"
set yrange [0:1000000]
set ylabel "m^2"
set samples 1000
set isosamples 1000

# Generate the data to plot
f(x,y) = (x*y*541.9) - (57276.23171*x + 0.2563443073*x*y + 1.153549383*y + 216000 ) 
set table 'data_2.txt'
splot f(x,y)
unset table

# Plot the data as a contour map
set view map
splot 'data_2.txt' with pm3d

