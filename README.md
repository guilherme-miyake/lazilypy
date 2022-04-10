# LazilyPy
#### Generic lazy evaluation with proper type hints
#### [Full documentation](https://github.com/guilherme-miyake/lazilypy/wiki/LazilyPy)
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
### Basic example:
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