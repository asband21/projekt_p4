// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from costom_interface:msg/ViconInfo.idl
// generated code does not contain a copyright notice

#ifndef COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__BUILDER_HPP_
#define COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__BUILDER_HPP_

#include "costom_interface/msg/detail/vicon_info__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace costom_interface
{

namespace msg
{

namespace builder
{

class Init_ViconInfo_position
{
public:
  explicit Init_ViconInfo_position(::costom_interface::msg::ViconInfo & msg)
  : msg_(msg)
  {}
  ::costom_interface::msg::ViconInfo position(::costom_interface::msg::ViconInfo::_position_type arg)
  {
    msg_.position = std::move(arg);
    return std::move(msg_);
  }

private:
  ::costom_interface::msg::ViconInfo msg_;
};

class Init_ViconInfo_velocity
{
public:
  Init_ViconInfo_velocity()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ViconInfo_position velocity(::costom_interface::msg::ViconInfo::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return Init_ViconInfo_position(msg_);
  }

private:
  ::costom_interface::msg::ViconInfo msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::costom_interface::msg::ViconInfo>()
{
  return costom_interface::msg::builder::Init_ViconInfo_velocity();
}

}  // namespace costom_interface

#endif  // COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__BUILDER_HPP_
