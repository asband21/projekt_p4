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

new_ids = list(current_data_dict.keys())
new_transforms = list(current_data_dict.values())

new_data = (new_ids, new_transforms)

with open("/home/ubuntu/tests/turtleTest/world_targets.pkl", 'wb') as f:
    pickle.dump(new_data, f)


# Print the data
print(data)

# Print the type of the data
print(type(data))



