// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from costom_interface:srv/Velocities.idl
// generated code does not contain a copyright notice
#include "costom_interface/srv/detail/velocities__functions.h"

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
costom_interface__srv__Velocities_Request__init(costom_interface__srv__Velocities_Request * msg)
{
  if (!msg) {
    return false;
  }
  // velocity
  if (!geometry_msgs__msg__Twist__init(&msg->velocity)) {
    costom_interface__srv__Velocities_Request__fini(msg);
    return false;
  }
  // position
  if (!geometry_msgs__msg__Twist__init(&msg->position)) {
    costom_interface__srv__Velocities_Request__fini(msg);
    return false;
  }
  return true;
}

void
costom_interface__srv__Velocities_Request__fini(costom_interface__srv__Velocities_Request * msg)
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
costom_interface__srv__Velocities_Request__are_equal(const costom_interface__srv__Velocities_Request * lhs, const costom_interface__srv__Velocities_Request * rhs)
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
costom_interface__srv__Velocities_Request__copy(
  const costom_interface__srv__Velocities_Request * input,
  costom_interface__srv__Velocities_Request * output)
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

costom_interface__srv__Velocities_Request *
costom_interface__srv__Velocities_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  costom_interface__srv__Velocities_Request * msg = (costom_interface__srv__Velocities_Request *)allocator.allocate(sizeof(costom_interface__srv__Velocities_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(costom_interface__srv__Velocities_Request));
  bool success = costom_interface__srv__Velocities_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
costom_interface__srv__Velocities_Request__destroy(costom_interface__srv__Velocities_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    costom_interface__srv__Velocities_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
costom_interface__srv__Velocities_Request__Sequence__init(costom_interface__srv__Velocities_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  costom_interface__srv__Velocities_Request * data = NULL;

  if (size) {
    data = (costom_interface__srv__Velocities_Request *)allocator.zero_allocate(size, sizeof(costom_interface__srv__Velocities_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = costom_interface__srv__Velocities_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        costom_interface__srv__Velocities_Request__fini(&data[i - 1]);
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
costom_interface__srv__Velocities_Request__Sequence__fini(costom_interface__srv__Velocities_Request__Sequence * array)
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
      costom_interface__srv__Velocities_Request__fini(&array->data[i]);
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

costom_interface__srv__Velocities_Request__Sequence *
costom_interface__srv__Velocities_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  costom_interface__srv__Velocities_Request__Sequence * array = (costom_interface__srv__Velocities_Request__Sequence *)allocator.allocate(sizeof(costom_interface__srv__Velocities_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = costom_interface__srv__Velocities_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
costom_interface__srv__Velocities_Request__Sequence__destroy(costom_interface__srv__Velocities_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    costom_interface__srv__Velocities_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
costom_interface__srv__Velocities_Request__Sequence__are_equal(const costom_interface__srv__Velocities_Request__Sequence * lhs, const costom_interface__srv__Velocities_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!costom_interface__srv__Velocities_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
costom_interface__srv__Velocities_Request__Sequence__copy(
  const costom_interface__srv__Velocities_Request__Sequence * input,
  costom_interface__srv__Velocities_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(costom_interface__srv__Velocities_Request);
    costom_interface__srv__Velocities_Request * data =
      (costom_interface__srv__Velocities_Request *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!costom_interface__srv__Velocities_Request__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          costom_interface__srv__Velocities_Request__fini(&data[i]);
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
    if (!costom_interface__srv__Velocities_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `error_velocity`
// Member `error_position`
// already included above
// #include "geometry_msgs/msg/detail/twist__functions.h"

bool
costom_interface__srv__Velocities_Response__init(costom_interface__srv__Velocities_Response * msg)
{
  if (!msg) {
    return false;
  }
  // error_velocity
  if (!geometry_msgs__msg__Twist__init(&msg->error_velocity)) {
    costom_interface__srv__Velocities_Response__fini(msg);
    return false;
  }
  // error_position
  if (!geometry_msgs__msg__Twist__init(&msg->error_position)) {
    costom_interface__srv__Velocities_Response__fini(msg);
    return false;
  }
  return true;
}

void
costom_interface__srv__Velocities_Response__fini(costom_interface__srv__Velocities_Response * msg)
{
  if (!msg) {
    return;
  }
  // error_velocity
  geometry_msgs__msg__Twist__fini(&msg->error_velocity);
  // error_position
  geometry_msgs__msg__Twist__fini(&msg->error_position);
}

bool
costom_interface__srv__Velocities_Response__are_equal(const costom_interface__srv__Velocities_Response * lhs, const costom_interface__srv__Velocities_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // error_velocity
  if (!geometry_msgs__msg__Twist__are_equal(
      &(lhs->error_velocity), &(rhs->error_velocity)))
  {
    return false;
  }
  // error_position
  if (!geometry_msgs__msg__Twist__are_equal(
      &(lhs->error_position), &(rhs->error_position)))
  {
    return false;
  }
  return true;
}

bool
costom_interface__srv__Velocities_Response__copy(
  const costom_interface__srv__Velocities_Response * input,
  costom_interface__srv__Velocities_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // error_velocity
  if (!geometry_msgs__msg__Twist__copy(
      &(input->error_velocity), &(output->error_velocity)))
  {
    return false;
  }
  // error_position
  if (!geometry_msgs__msg__Twist__copy(
      &(input->error_position), &(output->error_position)))
  {
    return false;
  }
  return true;
}

costom_interface__srv__Velocities_Response *
costom_interface__srv__Velocities_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  costom_interface__srv__Velocities_Response * msg = (costom_interface__srv__Velocities_Response *)allocator.allocate(sizeof(costom_interface__srv__Velocities_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(costom_interface__srv__Velocities_Response));
  bool success = costom_interface__srv__Velocities_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
costom_interface__srv__Velocities_Response__destroy(costom_interface__srv__Velocities_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    costom_interface__srv__Velocities_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
costom_interface__srv__Velocities_Response__Sequence__init(costom_interface__srv__Velocities_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  costom_interface__srv__Velocities_Response * data = NULL;

  if (size) {
    data = (costom_interface__srv__Velocities_Response *)allocator.zero_allocate(size, sizeof(costom_interface__srv__Velocities_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = costom_interface__srv__Velocities_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        costom_interface__srv__Velocities_Response__fini(&data[i - 1]);
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
costom_interface__srv__Velocities_Response__Sequence__fini(costom_interface__srv__Velocities_Response__Sequence * array)
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
      costom_interface__srv__Velocities_Response__fini(&array->data[i]);
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

costom_interface__srv__Velocities_Response__Sequence *
costom_interface__srv__Velocities_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  costom_interface__srv__Velocities_Response__Sequence * array = (costom_interface__srv__Velocities_Response__Sequence *)allocator.allocate(sizeof(costom_interface__srv__Velocities_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = costom_interface__srv__Velocities_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
costom_interface__srv__Velocities_Response__Sequence__destroy(costom_interface__srv__Velocities_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    costom_interface__srv__Velocities_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
costom_interface__srv__Velocities_Response__Sequence__are_equal(const costom_interface__srv__Velocities_Response__Sequence * lhs, const costom_interface__srv__Velocities_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!costom_interface__srv__Velocities_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
costom_interface__srv__Velocities_Response__Sequence__copy(
  const costom_interface__srv__Velocities_Response__Sequence * input,
  costom_interface__srv__Velocities_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(costom_interface__srv__Velocities_Response);
    costom_interface__srv__Velocities_Response * data =
      (costom_interface__srv__Velocities_Response *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!costom_interface__srv__Velocities_Response__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          costom_interface__srv__Velocities_Response__fini(&data[i]);
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
    if (!costom_interface__srv__Velocities_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
