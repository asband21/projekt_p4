// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from costom_interface:msg/ViconInfo.idl
// generated code does not contain a copyright notice

#ifndef COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__FUNCTIONS_H_
#define COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "costom_interface/msg/rosidl_generator_c__visibility_control.h"

#include "costom_interface/msg/detail/vicon_info__struct.h"

/// Initialize msg/ViconInfo message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * costom_interface__msg__ViconInfo
 * )) before or use
 * costom_interface__msg__ViconInfo__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_costom_interface
bool
costom_interface__msg__ViconInfo__init(costom_interface__msg__ViconInfo * msg);

/// Finalize msg/ViconInfo message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_costom_interface
void
costom_interface__msg__ViconInfo__fini(costom_interface__msg__ViconInfo * msg);

/// Create msg/ViconInfo message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * costom_interface__msg__ViconInfo__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_costom_interface
costom_interface__msg__ViconInfo *
costom_interface__msg__ViconInfo__create();

/// Destroy msg/ViconInfo message.
/**
 * It calls
 * costom_interface__msg__ViconInfo__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_costom_interface
void
costom_interface__msg__ViconInfo__destroy(costom_interface__msg__ViconInfo * msg);

/// Check for msg/ViconInfo message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_costom_interface
bool
costom_interface__msg__ViconInfo__are_equal(const costom_interface__msg__ViconInfo * lhs, const costom_interface__msg__ViconInfo * rhs);

/// Copy a msg/ViconInfo message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_costom_interface
bool
costom_interface__msg__ViconInfo__copy(
  const costom_interface__msg__ViconInfo * input,
  costom_interface__msg__ViconInfo * output);

/// Initialize array of msg/ViconInfo messages.
/**
 * It allocates the memory for the number of elements and calls
 * costom_interface__msg__ViconInfo__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_costom_interface
bool
costom_interface__msg__ViconInfo__Sequence__init(costom_interface__msg__ViconInfo__Sequence * array, size_t size);

/// Finalize array of msg/ViconInfo messages.
/**
 * It calls
 * costom_interface__msg__ViconInfo__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_costom_interface
void
costom_interface__msg__ViconInfo__Sequence__fini(costom_interface__msg__ViconInfo__Sequence * array);

/// Create array of msg/ViconInfo messages.
/**
 * It allocates the memory for the array and calls
 * costom_interface__msg__ViconInfo__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_costom_interface
costom_interface__msg__ViconInfo__Sequence *
costom_interface__msg__ViconInfo__Sequence__create(size_t size);

/// Destroy array of msg/ViconInfo messages.
/**
 * It calls
 * costom_interface__msg__ViconInfo__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_costom_interface
void
costom_interface__msg__ViconInfo__Sequence__destroy(costom_interface__msg__ViconInfo__Sequence * array);

/// Check for msg/ViconInfo message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_costom_interface
bool
costom_interface__msg__ViconInfo__Sequence__are_equal(const costom_interface__msg__ViconInfo__Sequence * lhs, const costom_interface__msg__ViconInfo__Sequence * rhs);

/// Copy an array of msg/ViconInfo messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_costom_interface
bool
costom_interface__msg__ViconInfo__Sequence__copy(
  const costom_interface__msg__ViconInfo__Sequence * input,
  costom_interface__msg__ViconInfo__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // COSTOM_INTERFACE__MSG__DETAIL__VICON_INFO__FUNCTIONS_H_
