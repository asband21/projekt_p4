import numpy as np
import matplotlib.pyplot as plt 

# Generate some random data
x = np.linspace(0, 0.1, 10) 
y = np.linspace(0, 100, 100000)                                                                             
x = x.reshape(1, -1)  # Reshape x to have shape (1, 10)
y = y.reshape(-1, 1)  # Reshape y to have shape (10000, 1)
X, Y = np.meshgrid(x, y)
Z = (x * y * 541.9) - (44997.39024*x + 0.05161179698*x*y + 0.2322530864*y + 14627) 

# Set up the colormap
cmap = plt.cm.get_cmap('RdBu')
norm = plt.Normalize(-1, 1)

# Plot the data with the colormap
plt.pcolormesh(X, Y, Z, cmap=cmap, norm=norm)

# Set the colorbar
plt.colorbar()

# Show the plot
plt.show()
