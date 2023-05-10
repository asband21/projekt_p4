// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from costom_interface:msg/ViconInfo.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "costom_interface/msg/detail/vicon_info__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace costom_interface
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void ViconInfo_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) costom_interface::msg::ViconInfo(_init);
}

void ViconInfo_fini_function(void * message_memory)
{
  auto typed_message = static_cast<costom_interface::msg::ViconInfo *>(message_memory);
  typed_message->~ViconInfo();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ViconInfo_message_member_array[2] = {
  {
    "velocity",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Twist>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(costom_interface::msg::ViconInfo, velocity),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "position",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::Twist>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(costom_interface::msg::ViconInfo, position),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ViconInfo_message_members = {
  "costom_interface::msg",  // message namespace
  "ViconInfo",  // message name
  2,  // number of fields
  sizeof(costom_interface::msg::ViconInfo),
  ViconInfo_message_member_array,  // message members
  ViconInfo_init_function,  // function to initialize message memory (memory has to be allocated)
  ViconInfo_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ViconInfo_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ViconInfo_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace costom_interface


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<costom_interface::msg::ViconInfo>()
{
  return &::costom_interface::msg::rosidl_typesupport_introspection_cpp::ViconInfo_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, costom_interface, msg, ViconInfo)() {
  return &::costom_interface::msg::rosidl_typesupport_introspection_cpp::ViconInfo_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
