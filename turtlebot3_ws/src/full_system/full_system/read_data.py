import pickle
import os

# Read data from pickle file and print it



# Get the path of the current directory
dir_path = os.path.dirname(os.path.realpath("test1.pkl"))


# Open the pickle file
with open("/home/ubuntu/tests/turtleTest/run1/data/test1.pkl", 'rb') as f:
    data = pickle.load(f)

# Print the data
print(data)

# Print the type of the data
print(type(data))
