// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from costom_interface:msg/ViconInfo.idl
// generated code does not contain a copyright notice

#ifndef COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "costom_interface/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "costom_interface/msg/detail/vicon_info__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace costom_interface
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_costom_interface
cdr_serialize(
  const costom_interface::msg::ViconInfo & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_costom_interface
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  costom_interface::msg::ViconInfo & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_costom_interface
get_serialized_size(
  const costom_interface::msg::ViconInfo & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_costom_interface
max_serialized_size_ViconInfo(
  bool & full_bounded,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace costom_interface

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_costom_interface
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, costom_interface, msg, ViconInfo)();

#ifdef __cplusplus
}
#endif

#endif  // COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
