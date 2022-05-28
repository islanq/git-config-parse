from abc import ABC

class Assignable(ABC, dict):
     
     def __init__(self, /, **kwargs):
          self.__dict__.update(kwargs)
    
     def __getitem__(self, key):
          return self.__dict__[key]
    
     def __setitem__(self, key, value):
          if type(value) is dict:
               value = Assignable(**value)
          self.__dict__[key] = value
          
     def __str__(self):
          temp = {}
          for k, v in self.__dict__.items():
               if issubclass(type(v), Assignable):
                    v = str(v)
               temp[k] = v
          return str(temp)
          
     def keys(self): 
          return self.__dict__.keys()
     
     def values(self): 
          return self.__dict__.values()
     
     def items(self): 
          return self.__dict__.items()
     
   