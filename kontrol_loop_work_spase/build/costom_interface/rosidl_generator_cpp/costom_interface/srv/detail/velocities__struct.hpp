// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from costom_interface:srv/Velocities.idl
// generated code does not contain a copyright notice

#ifndef COSTOM_INTERFACE__SRV__DETAIL__VELOCITIES__STRUCT_HPP_
#define COSTOM_INTERFACE__SRV__DETAIL__VELOCITIES__STRUCT_HPP_

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
# define DEPRECATED__costom_interface__srv__Velocities_Request __attribute__((deprecated))
#else
# define DEPRECATED__costom_interface__srv__Velocities_Request __declspec(deprecated)
#endif

namespace costom_interface
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Velocities_Request_
{
  using Type = Velocities_Request_<ContainerAllocator>;

  explicit Velocities_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : velocity(_init),
    position(_init)
  {
    (void)_init;
  }

  explicit Velocities_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    costom_interface::srv::Velocities_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const costom_interface::srv::Velocities_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<costom_interface::srv::Velocities_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<costom_interface::srv::Velocities_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      costom_interface::srv::Velocities_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<costom_interface::srv::Velocities_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      costom_interface::srv::Velocities_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<costom_interface::srv::Velocities_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<costom_interface::srv::Velocities_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<costom_interface::srv::Velocities_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__costom_interface__srv__Velocities_Request
    std::shared_ptr<costom_interface::srv::Velocities_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__costom_interface__srv__Velocities_Request
    std::shared_ptr<costom_interface::srv::Velocities_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Velocities_Request_ & other) const
  {
    if (this->velocity != other.velocity) {
      return false;
    }
    if (this->position != other.position) {
      return false;
    }
    return true;
  }
  bool operator!=(const Velocities_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Velocities_Request_

// alias to use template instance with default allocator
using Velocities_Request =
  costom_interface::srv::Velocities_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace costom_interface


// Include directives for member types
// Member 'error_velocity'
// Member 'error_position'
// already included above
// #include "geometry_msgs/msg/detail/twist__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__costom_interface__srv__Velocities_Response __attribute__((deprecated))
#else
# define DEPRECATED__costom_interface__srv__Velocities_Response __declspec(deprecated)
#endif

namespace costom_interface
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Velocities_Response_
{
  using Type = Velocities_Response_<ContainerAllocator>;

  explicit Velocities_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : error_velocity(_init),
    error_position(_init)
  {
    (void)_init;
  }

  explicit Velocities_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : error_velocity(_alloc, _init),
    error_position(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _error_velocity_type =
    geometry_msgs::msg::Twist_<ContainerAllocator>;
  _error_velocity_type error_velocity;
  using _error_position_type =
    geometry_msgs::msg::Twist_<ContainerAllocator>;
  _error_position_type error_position;

  // setters for named parameter idiom
  Type & set__error_velocity(
    const geometry_msgs::msg::Twist_<ContainerAllocator> & _arg)
  {
    this->error_velocity = _arg;
    return *this;
  }
  Type & set__error_position(
    const geometry_msgs::msg::Twist_<ContainerAllocator> & _arg)
  {
    this->error_position = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    costom_interface::srv::Velocities_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const costom_interface::srv::Velocities_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<costom_interface::srv::Velocities_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<costom_interface::srv::Velocities_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      costom_interface::srv::Velocities_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<costom_interface::srv::Velocities_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      costom_interface::srv::Velocities_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<costom_interface::srv::Velocities_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<costom_interface::srv::Velocities_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<costom_interface::srv::Velocities_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__costom_interface__srv__Velocities_Response
    std::shared_ptr<costom_interface::srv::Velocities_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__costom_interface__srv__Velocities_Response
    std::shared_ptr<costom_interface::srv::Velocities_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Velocities_Response_ & other) const
  {
    if (this->error_velocity != other.error_velocity) {
      return false;
    }
    if (this->error_position != other.error_position) {
      return false;
    }
    return true;
  }
  bool operator!=(const Velocities_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Velocities_Response_

// alias to use template instance with default allocator
using Velocities_Response =
  costom_interface::srv::Velocities_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace costom_interface

namespace costom_interface
{

namespace srv
{

struct Velocities
{
  using Request = costom_interface::srv::Velocities_Request;
  using Response = costom_interface::srv::Velocities_Response;
};

}  // namespace srv

}  // namespace costom_interface

#endif  // COSTOM_INTERFACE__SRV__DETAIL__VELOCITIES__STRUCT_HPP_
