import pickle
import os

# Read data from pickle file and print it



# Open the pickle file
with open("/home/ubuntu/tests/turtleTest/world_targets.pkl", 'rb') as f:
    data = pickle.load(f)

# Print the data
print(data)

# Print the type of the data
print(type(data))