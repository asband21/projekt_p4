// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from costom_interface:srv/Velocities.idl
// generated code does not contain a copyright notice

#ifndef COSTOM_INTERFACE__SRV__DETAIL__VELOCITIES__BUILDER_HPP_
#define COSTOM_INTERFACE__SRV__DETAIL__VELOCITIES__BUILDER_HPP_

#include "costom_interface/srv/detail/velocities__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace costom_interface
{

namespace srv
{

namespace builder
{

class Init_Velocities_Request_position
{
public:
  explicit Init_Velocities_Request_position(::costom_interface::srv::Velocities_Request & msg)
  : msg_(msg)
  {}
  ::costom_interface::srv::Velocities_Request position(::costom_interface::srv::Velocities_Request::_position_type arg)
  {
    msg_.position = std::move(arg);
    return std::move(msg_);
  }

private:
  ::costom_interface::srv::Velocities_Request msg_;
};

class Init_Velocities_Request_velocity
{
public:
  Init_Velocities_Request_velocity()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Velocities_Request_position velocity(::costom_interface::srv::Velocities_Request::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return Init_Velocities_Request_position(msg_);
  }

private:
  ::costom_interface::srv::Velocities_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::costom_interface::srv::Velocities_Request>()
{
  return costom_interface::srv::builder::Init_Velocities_Request_velocity();
}

}  // namespace costom_interface


namespace costom_interface
{

namespace srv
{

namespace builder
{

class Init_Velocities_Response_error_position
{
public:
  explicit Init_Velocities_Response_error_position(::costom_interface::srv::Velocities_Response & msg)
  : msg_(msg)
  {}
  ::costom_interface::srv::Velocities_Response error_position(::costom_interface::srv::Velocities_Response::_error_position_type arg)
  {
    msg_.error_position = std::move(arg);
    return std::move(msg_);
  }

private:
  ::costom_interface::srv::Velocities_Response msg_;
};

class Init_Velocities_Response_error_velocity
{
public:
  Init_Velocities_Response_error_velocity()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Velocities_Response_error_position error_velocity(::costom_interface::srv::Velocities_Response::_error_velocity_type arg)
  {
    msg_.error_velocity = std::move(arg);
    return Init_Velocities_Response_error_position(msg_);
  }

private:
  ::costom_interface::srv::Velocities_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::costom_interface::srv::Velocities_Response>()
{
  return costom_interface::srv::builder::Init_Velocities_Response_error_velocity();
}

}  // namespace costom_interface

#endif  // COSTOM_INTERFACE__SRV__DETAIL__VELOCITIES__BUILDER_HPP_
