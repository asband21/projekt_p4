#!/bin/bash
rm disherder.csv
rm error.csv
rm volosty.csv
colcon build --packages-select costom_interface && colcon build --packages-select vel_err && source install/setup.bash && echo "build = done" && ros2 launch vel_err drone_regulering.launch.py
