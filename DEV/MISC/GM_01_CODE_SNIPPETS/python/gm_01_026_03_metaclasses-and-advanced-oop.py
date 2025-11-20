# PATTERN: Metaclasses and Advanced OOP

class PluginMeta(type):
    def __new__(mcs, name, bases, namespace):
        # Add a default attribute to all classes created with this metaclass
        namespace['plugin_type'] = name.lower()
        cls = super().__new__(mcs, name, bases, namespace)
        return cls

class BasePlugin(metaclass=PluginMeta):
    def execute(self):
        raise NotImplementedError

class MyTextPlugin(BasePlugin):
    def execute(self):
        return f"Executing {self.plugin_type} plugin."

# PATTERN: Metaclasses and Advanced OOP

class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name="default"):
        # __init__ is called every time, but on the same instance
        # To prevent re-initialization, one might add a flag
        if not hasattr(self, '_initialized'):
            self.name = name
            self._initialized = True

# PATTERN: Metaclasses and Advanced OOP

class ComponentRegistry:
    _components = {}

    def __init_subclass__(cls, component_type=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if component_type:
            cls._components[component_type] = cls
        else:
            # Enforce component_type for all direct subclasses
            raise TypeError(f"Class {cls.__name__} must define a 'component_type'.")

class Processor(ComponentRegistry, component_type="processor"):
    def process(self, data):
        return f"Processing {data} with {self.__class__.__name__}"

class Validator(ComponentRegistry, component_type="validator"):
    def validate(self, data):
        return f"Validating {data} with {self.__class__.__name__}"

# PATTERN: Metaclasses and Advanced OOP

class ValidatedString:
    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise ValueError("Value must be a string.")
        setattr(obj, self.private_name, value)

class User:
    name = ValidatedString()
    email = ValidatedString()

    def __init__(self, name, email):
        self.name = name
        self.email = email