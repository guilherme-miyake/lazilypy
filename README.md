# LazilyPy
#### Generic lazy evaluation with proper type hints

## How to Install
Install from Python Packages directory with
```bash
pip install lazilypy
```
Or build and install straight from this repository:
```bash
pip install git+https://github.com/guilherme-miyake/lazilypy.git@v.1.0.0
```

## How to use
### Lazy example:
```python
import time
from io import TextIOWrapper
import os

from lazilypy import Lazy, logger

logger.setLevel("DEBUG")
new_file = "lazy.txt"
# Lazy instance creates a ready-to-build instance
lazy: Lazy | TextIOWrapper = Lazy(open, new_file, "w")
# The instance has not been started yet, the object will be a Lazy and the path will not exist
logger.info(f"File exists? {os.path.exists(new_file)}")
logger.info(f"My object is: {lazy}")
# Once "anything" is done with the instance
time.sleep(1)
lazy.write('Hello World')
# Now the instance has been started, the object will be the TextIOWrapper and the path will exist
logger.info(f"File exists? {os.path.exists(new_file)}")
logger.info(f"My object is: {lazy}")
lazy.close()
```
### LazyContext example:
```python
import os
import time

from lazilypy import LazyContext, logger

logger.setLevel("DEBUG")
new_file = "lazy_context.txt"
# Lazy instance creates a ready-to-build instance
with LazyContext(open, new_file, "w") as lazy:
    # The instance has not been started yet, the object will be a Lazy and the path will not exist
    logger.info(f"File exists? {os.path.exists(new_file)}")
    logger.info(f"My object is: {lazy}")
    # Once "anything" is done with the instance
    time.sleep(1)
    lazy.write('Hello World')
    # Now the instance has been started, the object will be the TextIOWrapper and the path will exist
    logger.info(f"File exists? {os.path.exists(new_file)}")
    logger.info(f"My object is: {lazy}")
```
If a given context is not used, it is not started, and it will not exit as well.

### @make_lazy decorator example:

```python
import time
from lazilypy import Lazy, make_lazy


@make_lazy
def do_stuff() -> bool:
    print("Such stuff")
    print("Much lazy")
    return True


def take_a_nap():
    print("zZzZzZ...")
    time.sleep(2)


stuff: Lazy | bool = do_stuff()
take_a_nap()
if stuff:
    print("Wow")
```

## Issues and Limitations

### The `is` operator is not supported
This operator will not initialize the instance and will always point to the Lazy instance,
usually resulting in `False` assertions:
```python
Lazy(bool, 1) is True  # returns False
Lazy(bool, 1) == True  # returns True
```

### Beware of expected side effects
The Lazy object is a abstraction that depends on its own generated object, 
and as such it has no control over side effects.

In the example below, you are able to use the `child` object before the `parent` one,
and in doing so, it may lead to a failed attempt to retrieve an `child` that was never created.

```python
parent = Lazy(Parent)
child = Lazy(Child)
```
