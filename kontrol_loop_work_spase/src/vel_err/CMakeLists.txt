cmake_minimum_required(VERSION 3.5)
project(vel_err)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(custom_interface REQUIRED)

# Add the executable
add_executable(frame_listener vel_err/err.cpp)

# Specify the dependencies of the executable
ament_target_dependencies(frame_listener
  rclcpp
  std_msgs
  geometry_msgs
  tf2_msgs
  tf2_ros
  custom_interface)

# Install the executable
install(TARGETS frame_listener
  DESTINATION lib/${PROJECT_NAME})

# Install package.xml
ament_package()
