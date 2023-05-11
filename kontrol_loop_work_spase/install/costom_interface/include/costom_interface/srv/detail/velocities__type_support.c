// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from costom_interface:srv/Velocities.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "costom_interface/srv/detail/velocities__rosidl_typesupport_introspection_c.h"
#include "costom_interface/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "costom_interface/srv/detail/velocities__functions.h"
#include "costom_interface/srv/detail/velocities__struct.h"


// Include directives for member types
// Member `velocity`
// Member `position`
#include "geometry_msgs/msg/twist.h"
// Member `velocity`
// Member `position`
#include "geometry_msgs/msg/detail/twist__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void Velocities_Request__rosidl_typesupport_introspection_c__Velocities_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  costom_interface__srv__Velocities_Request__init(message_memory);
}

void Velocities_Request__rosidl_typesupport_introspection_c__Velocities_Request_fini_function(void * message_memory)
{
  costom_interface__srv__Velocities_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember Velocities_Request__rosidl_typesupport_introspection_c__Velocities_Request_message_member_array[2] = {
  {
    "velocity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(costom_interface__srv__Velocities_Request, velocity),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(costom_interface__srv__Velocities_Request, position),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers Velocities_Request__rosidl_typesupport_introspection_c__Velocities_Request_message_members = {
  "costom_interface__srv",  // message namespace
  "Velocities_Request",  // message name
  2,  // number of fields
  sizeof(costom_interface__srv__Velocities_Request),
  Velocities_Request__rosidl_typesupport_introspection_c__Velocities_Request_message_member_array,  // message members
  Velocities_Request__rosidl_typesupport_introspection_c__Velocities_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  Velocities_Request__rosidl_typesupport_introspection_c__Velocities_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t Velocities_Request__rosidl_typesupport_introspection_c__Velocities_Request_message_type_support_handle = {
  0,
  &Velocities_Request__rosidl_typesupport_introspection_c__Velocities_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_costom_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, costom_interface, srv, Velocities_Request)() {
  Velocities_Request__rosidl_typesupport_introspection_c__Velocities_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Twist)();
  Velocities_Request__rosidl_typesupport_introspection_c__Velocities_Request_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Twist)();
  if (!Velocities_Request__rosidl_typesupport_introspection_c__Velocities_Request_message_type_support_handle.typesupport_identifier) {
    Velocities_Request__rosidl_typesupport_introspection_c__Velocities_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &Velocities_Request__rosidl_typesupport_introspection_c__Velocities_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "costom_interface/srv/detail/velocities__rosidl_typesupport_introspection_c.h"
// already included above
// #include "costom_interface/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "costom_interface/srv/detail/velocities__functions.h"
// already included above
// #include "costom_interface/srv/detail/velocities__struct.h"


// Include directives for member types
// Member `error_velocity`
// Member `error_position`
// already included above
// #include "geometry_msgs/msg/twist.h"
// Member `error_velocity`
// Member `error_position`
// already included above
// #include "geometry_msgs/msg/detail/twist__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void Velocities_Response__rosidl_typesupport_introspection_c__Velocities_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  costom_interface__srv__Velocities_Response__init(message_memory);
}

void Velocities_Response__rosidl_typesupport_introspection_c__Velocities_Response_fini_function(void * message_memory)
{
  costom_interface__srv__Velocities_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember Velocities_Response__rosidl_typesupport_introspection_c__Velocities_Response_message_member_array[2] = {
  {
    "error_velocity",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(costom_interface__srv__Velocities_Response, error_velocity),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "error_position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(costom_interface__srv__Velocities_Response, error_position),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers Velocities_Response__rosidl_typesupport_introspection_c__Velocities_Response_message_members = {
  "costom_interface__srv",  // message namespace
  "Velocities_Response",  // message name
  2,  // number of fields
  sizeof(costom_interface__srv__Velocities_Response),
  Velocities_Response__rosidl_typesupport_introspection_c__Velocities_Response_message_member_array,  // message members
  Velocities_Response__rosidl_typesupport_introspection_c__Velocities_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  Velocities_Response__rosidl_typesupport_introspection_c__Velocities_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t Velocities_Response__rosidl_typesupport_introspection_c__Velocities_Response_message_type_support_handle = {
  0,
  &Velocities_Response__rosidl_typesupport_introspection_c__Velocities_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_costom_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, costom_interface, srv, Velocities_Response)() {
  Velocities_Response__rosidl_typesupport_introspection_c__Velocities_Response_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Twist)();
  Velocities_Response__rosidl_typesupport_introspection_c__Velocities_Response_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Twist)();
  if (!Velocities_Response__rosidl_typesupport_introspection_c__Velocities_Response_message_type_support_handle.typesupport_identifier) {
    Velocities_Response__rosidl_typesupport_introspection_c__Velocities_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &Velocities_Response__rosidl_typesupport_introspection_c__Velocities_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "costom_interface/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "costom_interface/srv/detail/velocities__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers costom_interface__srv__detail__velocities__rosidl_typesupport_introspection_c__Velocities_service_members = {
  "costom_interface__srv",  // service namespace
  "Velocities",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // costom_interface__srv__detail__velocities__rosidl_typesupport_introspection_c__Velocities_Request_message_type_support_handle,
  NULL  // response message
  // costom_interface__srv__detail__velocities__rosidl_typesupport_introspection_c__Velocities_Response_message_type_support_handle
};

static rosidl_service_type_support_t costom_interface__srv__detail__velocities__rosidl_typesupport_introspection_c__Velocities_service_type_support_handle = {
  0,
  &costom_interface__srv__detail__velocities__rosidl_typesupport_introspection_c__Velocities_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, costom_interface, srv, Velocities_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, costom_interface, srv, Velocities_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_costom_interface
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, costom_interface, srv, Velocities)() {
  if (!costom_interface__srv__detail__velocities__rosidl_typesupport_introspection_c__Velocities_service_type_support_handle.typesupport_identifier) {
    costom_interface__srv__detail__velocities__rosidl_typesupport_introspection_c__Velocities_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)costom_interface__srv__detail__velocities__rosidl_typesupport_introspection_c__Velocities_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, costom_interface, srv, Velocities_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, costom_interface, srv, Velocities_Response)()->data;
  }

  return &costom_interface__srv__detail__velocities__rosidl_typesupport_introspection_c__Velocities_service_type_support_handle;
}
