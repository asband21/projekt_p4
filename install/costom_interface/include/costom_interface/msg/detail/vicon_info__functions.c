// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from costom_interface:msg/ViconInfo.idl
// generated code does not contain a copyright notice
#include "costom_interface/msg/detail/vicon_info__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `velocity`
// Member `position`
#include "geometry_msgs/msg/detail/twist__functions.h"

bool
costom_interface__msg__ViconInfo__init(costom_interface__msg__ViconInfo * msg)
{
  if (!msg) {
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Twist__init(&msg->velocity)) {
    costom_interface__msg__ViconInfo__fini(msg);
    return false;
  }
  // position
  if (!geometry_msgs__msg__Twist__init(&msg->position)) {
    costom_interface__msg__ViconInfo__fini(msg);
    return false;
  }
  return true;
}

void
costom_interface__msg__ViconInfo__fini(costom_interface__msg__ViconInfo * msg)
{
  if (!msg) {
    return;
  }
  // velocity
  geometry_msgs__msg__Twist__fini(&msg->velocity);
  // position
  geometry_msgs__msg__Twist__fini(&msg->position);
}

bool
costom_interface__msg__ViconInfo__are_equal(const costom_interface__msg__ViconInfo * lhs, const costom_interface__msg__ViconInfo * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Twist__are_equal(
      &(lhs->velocity), &(rhs->velocity)))
  {
    return false;
  }
  // position
  if (!geometry_msgs__msg__Twist__are_equal(
      &(lhs->position), &(rhs->position)))
  {
    return false;
  }
  return true;
}

bool
costom_interface__msg__ViconInfo__copy(
  const costom_interface__msg__ViconInfo * input,
  costom_interface__msg__ViconInfo * output)
{
  if (!input || !output) {
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Twist__copy(
      &(input->velocity), &(output->velocity)))
  {
    return false;
  }
  // position
  if (!geometry_msgs__msg__Twist__copy(
      &(input->position), &(output->position)))
  {
    return false;
  }
  return true;
}

costom_interface__msg__ViconInfo *
costom_interface__msg__ViconInfo__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  costom_interface__msg__ViconInfo * msg = (costom_interface__msg__ViconInfo *)allocator.allocate(sizeof(costom_interface__msg__ViconInfo), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(costom_interface__msg__ViconInfo));
  bool success = costom_interface__msg__ViconInfo__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
costom_interface__msg__ViconInfo__destroy(costom_interface__msg__ViconInfo * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    costom_interface__msg__ViconInfo__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
costom_interface__msg__ViconInfo__Sequence__init(costom_interface__msg__ViconInfo__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  costom_interface__msg__ViconInfo * data = NULL;

  if (size) {
    data = (costom_interface__msg__ViconInfo *)allocator.zero_allocate(size, sizeof(costom_interface__msg__ViconInfo), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = costom_interface__msg__ViconInfo__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        costom_interface__msg__ViconInfo__fini(&data[i - 1]);
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
costom_interface__msg__ViconInfo__Sequence__fini(costom_interface__msg__ViconInfo__Sequence * array)
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
      costom_interface__msg__ViconInfo__fini(&array->data[i]);
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

costom_interface__msg__ViconInfo__Sequence *
costom_interface__msg__ViconInfo__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  costom_interface__msg__ViconInfo__Sequence * array = (costom_interface__msg__ViconInfo__Sequence *)allocator.allocate(sizeof(costom_interface__msg__ViconInfo__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = costom_interface__msg__ViconInfo__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
costom_interface__msg__ViconInfo__Sequence__destroy(costom_interface__msg__ViconInfo__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    costom_interface__msg__ViconInfo__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
costom_interface__msg__ViconInfo__Sequence__are_equal(const costom_interface__msg__ViconInfo__Sequence * lhs, const costom_interface__msg__ViconInfo__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!costom_interface__msg__ViconInfo__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
costom_interface__msg__ViconInfo__Sequence__copy(
  const costom_interface__msg__ViconInfo__Sequence * input,
  costom_interface__msg__ViconInfo__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(costom_interface__msg__ViconInfo);
    costom_interface__msg__ViconInfo * data =
      (costom_interface__msg__ViconInfo *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!costom_interface__msg__ViconInfo__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          costom_interface__msg__ViconInfo__fini(&data[i]);
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
    if (!costom_interface__msg__ViconInfo__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
