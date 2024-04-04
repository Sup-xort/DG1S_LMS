from .settings.base import *

from .settings.prod import *

try:
   from .settings.local import *
except:
   pass