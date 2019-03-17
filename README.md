# CustomIdenticon

![image](https://user-images.githubusercontent.com/22620605/53684108-2c1c3180-3d1a-11e9-84ca-64547fb6ad51.png)

Python library for generate a variety of identicons. 

[![image](https://travis-ci.org/LexSerest/customidenticon.svg?branch=master)](https://travis-ci.org/LexSerest/customidenticon)

## Features

- 3 different types of identicons
- change the final image size (size of elements, number of elements)
- change border size
- change background color 
- change the transparency of elements
- change the output format (PNG, JPEG, etc.)
- choice of hashing algorithm (including your own)


## Installation

`pip install customidenticon`

## Usage
End image size = size * block_size + border * 2
```python
import customidenticon
identicon = customidenticon.create(
    "Test data",            # Data
    type="pixels",          # Type of algorithm (pixels, blocks or layers)
    format="png",           # Output format
    salt="",                # salt for more variants
    background="#f0f0f0",   # background color
    block_visibility=140,   # transparency of elements in the image (0-255)
    block_size=30,          # size of elements (px)
    border=25,              # border (px)
    size=5,                 # number of elements
    hash_func=None          # hash function (auto)
)

```

### Save 
```python
import customidenticon
identicon = customidenticon.create("Test data", size=5)
# identicon = b"\x89PNG\r\n\x1a\n\x00\x00\x00..."

# save to file
with open("identicon.png", "wb") as f:
    f.write(identicon)

# to image
import io
from PIL import Image
image = Image.open(io.BytesIO(identicon))
```

## Hash algorithm
Use `hashlib` for change algorithm
```python
import hashlib
import customidenticon
identicon = customidenticon.create("Test data", hash_func=hashlib.sha3_256)
```
Example custom hash algorithm
```python
import customidenticon
class MySuperHashAlgorithm:
    def __init__(self, *args):
        pass
    def hexdigest(self):
        return "0"*200
        
identicon = customidenticon.create("Test data", hash_func=MySuperHashAlgorithm)
```

## Examples

```python
import customidenticon
# Create github-like (5x5)
identicon1 = customidenticon.create("Test") # 200x200px (default for all)
# or
identicon1 = customidenticon.create("Test", type="pixels") 

# Create "pixels" type (6x6)
# End image size 200x200px (6 * 25 + 25 * 2)
identicon2 = customidenticon.create("Test", size=6, block_size=25) 

# Create "layers" type (3 layer)
# End image size 200x200px (default size = 3 and block_size = 50)
identicon4 = customidenticon.create("Test", type="layers")

# Create "layers" type (8 layer)
# End image size 200x200px (8 * 20 + 20 * 2)
identicon5 = customidenticon.create("Test", type="layers", size=8, block_size=20, border=20)

# Create "blocks" type (3x3) (200x200px)
identicon6 = customidenticon.create("Test", type="block", block_visibility=100)
```


##### Result 
![image](https://user-images.githubusercontent.com/22620605/53685533-0c423900-3d2d-11e9-89e0-e3cc7bfa7548.png)
