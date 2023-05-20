// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from costom_interface:msg/WantedVelocities.idl
// generated code does not contain a copyright notice

#ifndef COSTOM_INTERFACE__MSG__DETAIL__WANTED_VELOCITIES__STRUCT_H_
#define COSTOM_INTERFACE__MSG__DETAIL__WANTED_VELOCITIES__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'name'
#include "rosidl_runtime_c/string.h"
// Member 'coordinates'
#include "geometry_msgs/msg/detail/point__struct.h"

// Struct defined in msg/WantedVelocities in the package costom_interface.
typedef struct costom_interface__msg__WantedVelocities
{
  rosidl_runtime_c__String name;
  geometry_msgs__msg__Point coordinates;
} costom_interface__msg__WantedVelocities;

// Struct for a sequence of costom_interface__msg__WantedVelocities.
typedef struct costom_interface__msg__WantedVelocities__Sequence
{
  costom_interface__msg__WantedVelocities * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} costom_interface__msg__WantedVelocities__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // COSTOM_INTERFACE__MSG__DETAIL__WANTED_VELOCITIES__STRUCT_H_
