# zapuskaet, parsit kakoy iz scriptov, tipo esli dict, to bot, inache launcher
# i launcher tam sam uzhe parsit ip 

import sys
from ast import literal_eval

script = "launcher"

try:
  i = sys.argv[1]
  print(i)
  parsed_config = literal_eval(i)
  print(f'successfully parsed cli config')
  print(f'parsed_config: {parsed_config}')
  if type(parsed_config) != dict:
    raise TypeError
  script = parsed_config['script']

except Exception:
  print('exception during parsing')

if script == 'maps':
  from maps import *
elif script == 'quest':
  from quest import *
elif script == 'aqueduct':
  from aqueduct import *
else:
  from launcher import *