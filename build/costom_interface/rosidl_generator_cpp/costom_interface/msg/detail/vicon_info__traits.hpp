// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from costom_interface:msg/ViconInfo.idl
// generated code does not contain a copyright notice

#ifndef COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__TRAITS_HPP_
#define COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__TRAITS_HPP_

#include "costom_interface/msg/detail/vicon_info__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

// Include directives for member types
// Member 'velocity'
// Member 'position'
#include "geometry_msgs/msg/detail/twist__traits.hpp"

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<costom_interface::msg::ViconInfo>()
{
  return "costom_interface::msg::ViconInfo";
}

template<>
inline const char * name<costom_interface::msg::ViconInfo>()
{
  return "costom_interface/msg/ViconInfo";
}

template<>
struct has_fixed_size<costom_interface::msg::ViconInfo>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Twist>::value> {};

template<>
struct has_bounded_size<costom_interface::msg::ViconInfo>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Twist>::value> {};

template<>
struct is_message<costom_interface::msg::ViconInfo>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__TRAITS_HPP_
