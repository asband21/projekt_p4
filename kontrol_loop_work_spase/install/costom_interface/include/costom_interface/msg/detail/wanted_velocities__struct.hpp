// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from costom_interface:msg/WantedVelocities.idl
// generated code does not contain a copyright notice

#ifndef COSTOM_INTERFACE__MSG__DETAIL__WANTED_VELOCITIES__STRUCT_HPP_
#define COSTOM_INTERFACE__MSG__DETAIL__WANTED_VELOCITIES__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


// Include directives for member types
// Member 'coordinates'
#include "geometry_msgs/msg/detail/point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__costom_interface__msg__WantedVelocities __attribute__((deprecated))
#else
# define DEPRECATED__costom_interface__msg__WantedVelocities __declspec(deprecated)
#endif

namespace costom_interface
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct WantedVelocities_
{
  using Type = WantedVelocities_<ContainerAllocator>;

  explicit WantedVelocities_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : coordinates(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->name = "";
    }
  }

  explicit WantedVelocities_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : name(_alloc),
    coordinates(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->name = "";
    }
  }

  // field types and members
  using _name_type =
    std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other>;
  _name_type name;
  using _coordinates_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _coordinates_type coordinates;

  // setters for named parameter idiom
  Type & set__name(
    const std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other> & _arg)
  {
    this->name = _arg;
    return *this;
  }
  Type & set__coordinates(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->coordinates = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    costom_interface::msg::WantedVelocities_<ContainerAllocator> *;
  using ConstRawPtr =
    const costom_interface::msg::WantedVelocities_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<costom_interface::msg::WantedVelocities_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<costom_interface::msg::WantedVelocities_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      costom_interface::msg::WantedVelocities_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<costom_interface::msg::WantedVelocities_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      costom_interface::msg::WantedVelocities_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<costom_interface::msg::WantedVelocities_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<costom_interface::msg::WantedVelocities_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<costom_interface::msg::WantedVelocities_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__costom_interface__msg__WantedVelocities
    std::shared_ptr<costom_interface::msg::WantedVelocities_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__costom_interface__msg__WantedVelocities
    std::shared_ptr<costom_interface::msg::WantedVelocities_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const WantedVelocities_ & other) const
  {
    if (this->name != other.name) {
      return false;
    }
    if (this->coordinates != other.coordinates) {
      return false;
    }
    return true;
  }
  bool operator!=(const WantedVelocities_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct WantedVelocities_

// alias to use template instance with default allocator
using WantedVelocities =
  costom_interface::msg::WantedVelocities_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace costom_interface

#endif  // COSTOM_INTERFACE__MSG__DETAIL__WANTED_VELOCITIES__STRUCT_HPP_
