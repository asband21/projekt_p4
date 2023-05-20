# generated from rosidl_generator_py/resource/_idl.py.em
# with input from costom_interface:srv/Velocities.idl
# generated code does not contain a copyright notice


# Import statements for member types

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Velocities_Request(type):
    """Metaclass of message 'Velocities_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('costom_interface')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'costom_interface.srv.Velocities_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__velocities__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__velocities__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__velocities__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__velocities__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__velocities__request

            from geometry_msgs.msg import Twist
            if Twist.__class__._TYPE_SUPPORT is None:
                Twist.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Velocities_Request(metaclass=Metaclass_Velocities_Request):
    """Message class 'Velocities_Request'."""

    __slots__ = [
        '_velocity',
        '_position',
    ]

    _fields_and_field_types = {
        'velocity': 'geometry_msgs/Twist',
        'position': 'geometry_msgs/Twist',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Twist'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Twist'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from geometry_msgs.msg import Twist
        self.velocity = kwargs.get('velocity', Twist())
        from geometry_msgs.msg import Twist
        self.position = kwargs.get('position', Twist())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.velocity != other.velocity:
            return False
        if self.position != other.position:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @property
    def velocity(self):
        """Message field 'velocity'."""
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        if __debug__:
            from geometry_msgs.msg import Twist
            assert \
                isinstance(value, Twist), \
                "The 'velocity' field must be a sub message of type 'Twist'"
        self._velocity = value

    @property
    def position(self):
        """Message field 'position'."""
        return self._position

    @position.setter
    def position(self, value):
        if __debug__:
            from geometry_msgs.msg import Twist
            assert \
                isinstance(value, Twist), \
                "The 'position' field must be a sub message of type 'Twist'"
        self._position = value


# Import statements for member types

# already imported above
# import rosidl_parser.definition


class Metaclass_Velocities_Response(type):
    """Metaclass of message 'Velocities_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('costom_interface')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'costom_interface.srv.Velocities_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__velocities__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__velocities__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__velocities__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__velocities__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__velocities__response

            from geometry_msgs.msg import Twist
            if Twist.__class__._TYPE_SUPPORT is None:
                Twist.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Velocities_Response(metaclass=Metaclass_Velocities_Response):
    """Message class 'Velocities_Response'."""

    __slots__ = [
        '_error_velocity',
        '_error_position',
    ]

    _fields_and_field_types = {
        'error_velocity': 'geometry_msgs/Twist',
        'error_position': 'geometry_msgs/Twist',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Twist'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Twist'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from geometry_msgs.msg import Twist
        self.error_velocity = kwargs.get('error_velocity', Twist())
        from geometry_msgs.msg import Twist
        self.error_position = kwargs.get('error_position', Twist())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.error_velocity != other.error_velocity:
            return False
        if self.error_position != other.error_position:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @property
    def error_velocity(self):
        """Message field 'error_velocity'."""
        return self._error_velocity

    @error_velocity.setter
    def error_velocity(self, value):
        if __debug__:
            from geometry_msgs.msg import Twist
            assert \
                isinstance(value, Twist), \
                "The 'error_velocity' field must be a sub message of type 'Twist'"
        self._error_velocity = value

    @property
    def error_position(self):
        """Message field 'error_position'."""
        return self._error_position

    @error_position.setter
    def error_position(self, value):
        if __debug__:
            from geometry_msgs.msg import Twist
            assert \
                isinstance(value, Twist), \
                "The 'error_position' field must be a sub message of type 'Twist'"
        self._error_position = value


class Metaclass_Velocities(type):
    """Metaclass of service 'Velocities'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('costom_interface')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'costom_interface.srv.Velocities')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__velocities

            from costom_interface.srv import _velocities
            if _velocities.Metaclass_Velocities_Request._TYPE_SUPPORT is None:
                _velocities.Metaclass_Velocities_Request.__import_type_support__()
            if _velocities.Metaclass_Velocities_Response._TYPE_SUPPORT is None:
                _velocities.Metaclass_Velocities_Response.__import_type_support__()


class Velocities(metaclass=Metaclass_Velocities):
    from costom_interface.srv._velocities import Velocities_Request as Request
    from costom_interface.srv._velocities import Velocities_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
