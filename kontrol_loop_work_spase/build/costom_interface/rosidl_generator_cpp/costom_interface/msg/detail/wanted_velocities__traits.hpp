// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from costom_interface:msg/WantedVelocities.idl
// generated code does not contain a copyright notice

#ifndef COSTOM_INTERFACE__MSG__DETAIL__WANTED_VELOCITIES__TRAITS_HPP_
#define COSTOM_INTERFACE__MSG__DETAIL__WANTED_VELOCITIES__TRAITS_HPP_

#include "costom_interface/msg/detail/wanted_velocities__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

// Include directives for member types
// Member 'coordinates'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<costom_interface::msg::WantedVelocities>()
{
  return "costom_interface::msg::WantedVelocities";
}

template<>
inline const char * name<costom_interface::msg::WantedVelocities>()
{
  return "costom_interface/msg/WantedVelocities";
}

template<>
struct has_fixed_size<costom_interface::msg::WantedVelocities>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<costom_interface::msg::WantedVelocities>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<costom_interface::msg::WantedVelocities>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // COSTOM_INTERFACE__MSG__DETAIL__WANTED_VELOCITIES__TRAITS_HPP_
