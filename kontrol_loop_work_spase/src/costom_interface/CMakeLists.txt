cmake_minimum_required(VERSION 3.8)
project(costom_interface)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/WantedVelocities.msg"
  "msg/ViconInfo.msg"
  "srv/Velocities.srv"
  DEPENDENCIES geometry_msgs

)


ament_export_dependencies(rosidl_default_runtime)


ament_package()
