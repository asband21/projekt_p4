// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from costom_interface:srv/Velocities.idl
// generated code does not contain a copyright notice

#ifndef COSTOM_INTERFACE__SRV__DETAIL__VELOCITIES__TRAITS_HPP_
#define COSTOM_INTERFACE__SRV__DETAIL__VELOCITIES__TRAITS_HPP_

#include "costom_interface/srv/detail/velocities__struct.hpp"
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
inline const char * data_type<costom_interface::srv::Velocities_Request>()
{
  return "costom_interface::srv::Velocities_Request";
}

template<>
inline const char * name<costom_interface::srv::Velocities_Request>()
{
  return "costom_interface/srv/Velocities_Request";
}

template<>
struct has_fixed_size<costom_interface::srv::Velocities_Request>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Twist>::value> {};

template<>
struct has_bounded_size<costom_interface::srv::Velocities_Request>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Twist>::value> {};

template<>
struct is_message<costom_interface::srv::Velocities_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'error_velocity'
// Member 'error_position'
// already included above
// #include "geometry_msgs/msg/detail/twist__traits.hpp"

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<costom_interface::srv::Velocities_Response>()
{
  return "costom_interface::srv::Velocities_Response";
}

template<>
inline const char * name<costom_interface::srv::Velocities_Response>()
{
  return "costom_interface/srv/Velocities_Response";
}

template<>
struct has_fixed_size<costom_interface::srv::Velocities_Response>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Twist>::value> {};

template<>
struct has_bounded_size<costom_interface::srv::Velocities_Response>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Twist>::value> {};

template<>
struct is_message<costom_interface::srv::Velocities_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<costom_interface::srv::Velocities>()
{
  return "costom_interface::srv::Velocities";
}

template<>
inline const char * name<costom_interface::srv::Velocities>()
{
  return "costom_interface/srv/Velocities";
}

template<>
struct has_fixed_size<costom_interface::srv::Velocities>
  : std::integral_constant<
    bool,
    has_fixed_size<costom_interface::srv::Velocities_Request>::value &&
    has_fixed_size<costom_interface::srv::Velocities_Response>::value
  >
{
};

template<>
struct has_bounded_size<costom_interface::srv::Velocities>
  : std::integral_constant<
    bool,
    has_bounded_size<costom_interface::srv::Velocities_Request>::value &&
    has_bounded_size<costom_interface::srv::Velocities_Response>::value
  >
{
};

template<>
struct is_service<costom_interface::srv::Velocities>
  : std::true_type
{
};

template<>
struct is_service_request<costom_interface::srv::Velocities_Request>
  : std::true_type
{
};

template<>
struct is_service_response<costom_interface::srv::Velocities_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // COSTOM_INTERFACE__SRV__DETAIL__VELOCITIES__TRAITS_HPP_
