import pickle
import os

# Read data from pickle file and print it

id_to_delete = 5


# Open the pickle file
with open("/home/ubuntu/tests/turtleTest/world_targets.pkl", 'rb') as f:
    data = pickle.load(f)

ids, transforms = data


current_data_dict = dict(zip(ids, transforms))


for id in ids:
    if id == id_to_delete:
        del current_data_dict[id]



print(current_data_dict)


# Print the data
print(data)

# Print the type of the data
print(type(data))



