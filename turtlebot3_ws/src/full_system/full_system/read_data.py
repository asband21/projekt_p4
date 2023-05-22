import pickle
import os

# Read data from pickle file and print it

input_num = input("Enter the number of the test to read: ")
num = input_num

# Get the path of the current directory
dir_path = os.path.dirname(os.path.realpath(f"test{num}.pkl"))


# Open the pickle file
with open(f"/home/ubuntu/tests/turtleTest/run{num}/data/test{num}.pkl", 'rb') as f:
    data = pickle.load(f)

# Print the data
print(data)

# Print the type of the data
print(type(data))
