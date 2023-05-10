// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from costom_interface:msg/WantedVelocities.idl
// generated code does not contain a copyright notice
#include "costom_interface/msg/detail/wanted_velocities__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `name`
#include "rosidl_runtime_c/string_functions.h"
// Member `coordinates`
#include "geometry_msgs/msg/detail/point__functions.h"

bool
costom_interface__msg__WantedVelocities__init(costom_interface__msg__WantedVelocities * msg)
{
  if (!msg) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__init(&msg->name)) {
    costom_interface__msg__WantedVelocities__fini(msg);
    return false;
  }
  // coordinates
  if (!geometry_msgs__msg__Point__init(&msg->coordinates)) {
    costom_interface__msg__WantedVelocities__fini(msg);
    return false;
  }
  return true;
}

void
costom_interface__msg__WantedVelocities__fini(costom_interface__msg__WantedVelocities * msg)
{
  if (!msg) {
    return;
  }
  // name
  rosidl_runtime_c__String__fini(&msg->name);
  // coordinates
  geometry_msgs__msg__Point__fini(&msg->coordinates);
}

bool
costom_interface__msg__WantedVelocities__are_equal(const costom_interface__msg__WantedVelocities * lhs, const costom_interface__msg__WantedVelocities * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->name), &(rhs->name)))
  {
    return false;
  }
  // coordinates
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->coordinates), &(rhs->coordinates)))
  {
    return false;
  }
  return true;
}

bool
costom_interface__msg__WantedVelocities__copy(
  const costom_interface__msg__WantedVelocities * input,
  costom_interface__msg__WantedVelocities * output)
{
  if (!input || !output) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__copy(
      &(input->name), &(output->name)))
  {
    return false;
  }
  // coordinates
  if (!geometry_msgs__msg__Point__copy(
      &(input->coordinates), &(output->coordinates)))
  {
    return false;
  }
  return true;
}

costom_interface__msg__WantedVelocities *
costom_interface__msg__WantedVelocities__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  costom_interface__msg__WantedVelocities * msg = (costom_interface__msg__WantedVelocities *)allocator.allocate(sizeof(costom_interface__msg__WantedVelocities), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(costom_interface__msg__WantedVelocities));
  bool success = costom_interface__msg__WantedVelocities__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
costom_interface__msg__WantedVelocities__destroy(costom_interface__msg__WantedVelocities * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    costom_interface__msg__WantedVelocities__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
costom_interface__msg__WantedVelocities__Sequence__init(costom_interface__msg__WantedVelocities__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  costom_interface__msg__WantedVelocities * data = NULL;

  if (size) {
    data = (costom_interface__msg__WantedVelocities *)allocator.zero_allocate(size, sizeof(costom_interface__msg__WantedVelocities), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = costom_interface__msg__WantedVelocities__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        costom_interface__msg__WantedVelocities__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
costom_interface__msg__WantedVelocities__Sequence__fini(costom_interface__msg__WantedVelocities__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      costom_interface__msg__WantedVelocities__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

costom_interface__msg__WantedVelocities__Sequence *
costom_interface__msg__WantedVelocities__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  costom_interface__msg__WantedVelocities__Sequence * array = (costom_interface__msg__WantedVelocities__Sequence *)allocator.allocate(sizeof(costom_interface__msg__WantedVelocities__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = costom_interface__msg__WantedVelocities__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
costom_interface__msg__WantedVelocities__Sequence__destroy(costom_interface__msg__WantedVelocities__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    costom_interface__msg__WantedVelocities__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
costom_interface__msg__WantedVelocities__Sequence__are_equal(const costom_interface__msg__WantedVelocities__Sequence * lhs, const costom_interface__msg__WantedVelocities__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!costom_interface__msg__WantedVelocities__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
costom_interface__msg__WantedVelocities__Sequence__copy(
  const costom_interface__msg__WantedVelocities__Sequence * input,
  costom_interface__msg__WantedVelocities__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(costom_interface__msg__WantedVelocities);
    costom_interface__msg__WantedVelocities * data =
      (costom_interface__msg__WantedVelocities *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!costom_interface__msg__WantedVelocities__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          costom_interface__msg__WantedVelocities__fini(&data[i]);
        }
        free(data);
        return false;
      }
    }
    output->data = data;
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!costom_interface__msg__WantedVelocities__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
