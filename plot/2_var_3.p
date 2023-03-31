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
f(x,y) = (x * y * 541.9) - 173276.7195*x + 1.538237311*x*y + 6.922067901*y + 2118408
set table 'data_3.txt'
splot f(x,y)
unset table

# Plot the data as a contour map
set view map
splot 'data_3.txt' with pm3d

