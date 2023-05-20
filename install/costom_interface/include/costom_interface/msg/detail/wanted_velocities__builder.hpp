// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from costom_interface:msg/WantedVelocities.idl
// generated code does not contain a copyright notice

#ifndef COSTOM_INTERFACE__MSG__DETAIL__WANTED_VELOCITIES__BUILDER_HPP_
#define COSTOM_INTERFACE__MSG__DETAIL__WANTED_VELOCITIES__BUILDER_HPP_

#include "costom_interface/msg/detail/wanted_velocities__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace costom_interface
{

namespace msg
{

namespace builder
{

class Init_WantedVelocities_coordinates
{
public:
  explicit Init_WantedVelocities_coordinates(::costom_interface::msg::WantedVelocities & msg)
  : msg_(msg)
  {}
  ::costom_interface::msg::WantedVelocities coordinates(::costom_interface::msg::WantedVelocities::_coordinates_type arg)
  {
    msg_.coordinates = std::move(arg);
    return std::move(msg_);
  }

private:
  ::costom_interface::msg::WantedVelocities msg_;
};

class Init_WantedVelocities_name
{
public:
  Init_WantedVelocities_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_WantedVelocities_coordinates name(::costom_interface::msg::WantedVelocities::_name_type arg)
  {
    msg_.name = std::move(arg);
    return Init_WantedVelocities_coordinates(msg_);
  }

private:
  ::costom_interface::msg::WantedVelocities msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::costom_interface::msg::WantedVelocities>()
{
  return costom_interface::msg::builder::Init_WantedVelocities_name();
}

}  // namespace costom_interface

#endif  // COSTOM_INTERFACE__MSG__DETAIL__WANTED_VELOCITIES__BUILDER_HPP_
