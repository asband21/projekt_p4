// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from costom_interface:msg/WantedVelocities.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "costom_interface/msg/detail/wanted_velocities__rosidl_typesupport_introspection_c.h"
#include "costom_interface/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "costom_interface/msg/detail/wanted_velocities__functions.h"
#include "costom_interface/msg/detail/wanted_velocities__struct.h"


// Include directives for member types
// Member `name`
#include "rosidl_runtime_c/string_functions.h"
// Member `coordinates`
#include "geometry_msgs/msg/point.h"
// Member `coordinates`
#include "geometry_msgs/msg/detail/point__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void WantedVelocities__rosidl_typesupport_introspection_c__WantedVelocities_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  costom_interface__msg__WantedVelocities__init(message_memory);
}

void WantedVelocities__rosidl_typesupport_introspection_c__WantedVelocities_fini_function(void * message_memory)
{
  costom_interface__msg__WantedVelocities__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember WantedVelocities__rosidl_typesupport_introspection_c__WantedVelocities_message_member_array[2] = {
  {
    "name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(costom_interface__msg__WantedVelocities, name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "coordinates",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(costom_interface__msg__WantedVelocities, coordinates),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers WantedVelocities__rosidl_typesupport_introspection_c__WantedVelocities_message_members = {
  "costom_interface__msg",  // message namespace
  "WantedVelocities",  // message name
  2,  // number of fields
  sizeof(costom_interface__msg__WantedVelocities),
  WantedVelocities__rosidl_typesupport_introspection_c__WantedVelocities_message_member_array,  // message members
  WantedVelocities__rosidl_typesupport_introspection_c__WantedVelocities_init_function,  // function to initialize message memory (memory has to be allocated)
  WantedVelocities__rosidl_typesupport_introspection_c__WantedVelocities_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t WantedVelocities__rosidl_typesupport_introspection_c__WantedVelocities_message_type_support_handle = {
  0,
  &WantedVelocities__rosidl_typesupport_introspection_c__WantedVelocities_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_costom_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, costom_interface, msg, WantedVelocities)() {
  WantedVelocities__rosidl_typesupport_introspection_c__WantedVelocities_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Point)();
  if (!WantedVelocities__rosidl_typesupport_introspection_c__WantedVelocities_message_type_support_handle.typesupport_identifier) {
    WantedVelocities__rosidl_typesupport_introspection_c__WantedVelocities_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &WantedVelocities__rosidl_typesupport_introspection_c__WantedVelocities_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
