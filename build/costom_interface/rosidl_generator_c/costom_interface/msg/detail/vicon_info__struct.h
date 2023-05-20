// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from costom_interface:msg/ViconInfo.idl
// generated code does not contain a copyright notice

#ifndef COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__STRUCT_H_
#define COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'velocity'
// Member 'position'
#include "geometry_msgs/msg/detail/twist__struct.h"

// Struct defined in msg/ViconInfo in the package costom_interface.
typedef struct costom_interface__msg__ViconInfo
{
  geometry_msgs__msg__Twist velocity;
  geometry_msgs__msg__Twist position;
} costom_interface__msg__ViconInfo;

// Struct for a sequence of costom_interface__msg__ViconInfo.
typedef struct costom_interface__msg__ViconInfo__Sequence
{
  costom_interface__msg__ViconInfo * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} costom_interface__msg__ViconInfo__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__STRUCT_H_
