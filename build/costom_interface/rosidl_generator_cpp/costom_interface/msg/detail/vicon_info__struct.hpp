// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from costom_interface:msg/ViconInfo.idl
// generated code does not contain a copyright notice

#ifndef COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__STRUCT_HPP_
#define COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


// Include directives for member types
// Member 'velocity'
// Member 'position'
#include "geometry_msgs/msg/detail/twist__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__costom_interface__msg__ViconInfo __attribute__((deprecated))
#else
# define DEPRECATED__costom_interface__msg__ViconInfo __declspec(deprecated)
#endif

namespace costom_interface
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ViconInfo_
{
  using Type = ViconInfo_<ContainerAllocator>;

  explicit ViconInfo_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : velocity(_init),
    position(_init)
  {
    (void)_init;
  }

  explicit ViconInfo_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : velocity(_alloc, _init),
    position(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _velocity_type =
    geometry_msgs::msg::Twist_<ContainerAllocator>;
  _velocity_type velocity;
  using _position_type =
    geometry_msgs::msg::Twist_<ContainerAllocator>;
  _position_type position;

  // setters for named parameter idiom
  Type & set__velocity(
    const geometry_msgs::msg::Twist_<ContainerAllocator> & _arg)
  {
    this->velocity = _arg;
    return *this;
  }
  Type & set__position(
    const geometry_msgs::msg::Twist_<ContainerAllocator> & _arg)
  {
    this->position = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    costom_interface::msg::ViconInfo_<ContainerAllocator> *;
  using ConstRawPtr =
    const costom_interface::msg::ViconInfo_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<costom_interface::msg::ViconInfo_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<costom_interface::msg::ViconInfo_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      costom_interface::msg::ViconInfo_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<costom_interface::msg::ViconInfo_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      costom_interface::msg::ViconInfo_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<costom_interface::msg::ViconInfo_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<costom_interface::msg::ViconInfo_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<costom_interface::msg::ViconInfo_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__costom_interface__msg__ViconInfo
    std::shared_ptr<costom_interface::msg::ViconInfo_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__costom_interface__msg__ViconInfo
    std::shared_ptr<costom_interface::msg::ViconInfo_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ViconInfo_ & other) const
  {
    if (this->velocity != other.velocity) {
      return false;
    }
    if (this->position != other.position) {
      return false;
    }
    return true;
  }
  bool operator!=(const ViconInfo_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ViconInfo_

// alias to use template instance with default allocator
using ViconInfo =
  costom_interface::msg::ViconInfo_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace costom_interface

#endif  // COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__STRUCT_HPP_
