import re
from collections import namedtuple
from functools import cache
from itertools import takewhile

from assignable import Assignable


class ConfigData(Assignable):
    pass

ConfigModule = namedtuple('ConfigModule', ['mod', 'sub'])
KeyValuePair = namedtuple('KeyValuePair', ['key', 'val'])

modpat = re.compile(r'\[(?P<module>\w+)(?:\s?"?(?P<submodule>\w+)?")?\]')
kvppat = re.compile(r'\t?(?P<key>\w+)\s?=\s?(?P<value>.*)$')

@cache
def is_mod(text:str) -> bool:
    """returns true if if the given string represets a module name

    Args:
        text (str): _description_

    Returns:
        bool: _description_ """
    return modpat.match(text) is not None

@cache
def is_kvp(text:str) -> bool:
    """determines if the given string is a kvp within a module

    Args:
        text (str): _description_

    Returns:
        bool: _description_
    """
    return kvppat.match(text) is not None

@cache
def get_mod(text:str) -> ConfigModule:
    mod, sub = modpat.match(text).groups()
    return ConfigModule(mod, sub)

@cache
def get_kvp(text:str) -> KeyValuePair:
    key, val = kvppat.match(text).groups()
    return KeyValuePair(key, val)
    

def read_config(path = '.\.git\config'):
    try:
      with open(path, 'r') as file:
        return file.read()
    except FileNotFoundError:
        print('Unable to find config file', path)



def main():
    
    config = ConfigData()
    # datum  = read_config()
    datum = read_config()
    lines  = datum.strip().splitlines()
    
    for idx, line in enumerate(lines):
        # loop for the config file "module" names
        if is_mod(line):
            # get module name from string, parse key
            mod = get_mod(line)
            key = '.'.join(mod) if mod.sub else mod.mod
            
            # 
            kvp_iter =  [ *takewhile(is_kvp, lines[idx+1:]) ]
            kvp_list =  [ get_kvp(kvp) for kvp in kvp_iter ]
            kvp_dict =  { key:val for key, val in kvp_list }
            config[key] = kvp_dict
 
    return config
        
        
if __name__ == '__main__':
    config = main()
    print(config)
    