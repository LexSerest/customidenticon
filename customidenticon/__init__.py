import io
from PIL import Image, ImageDraw
import hashlib


def _pixels(data,
            format="png",
            salt="",
            background="#f0f0f0",
            block_visibility=140,
            block_size=30,
            border=25,
            size=5,
            hash_func=None):
    """
    Generating GitHub-like symmetrical identicons.
    End image size = size * block_size + border * 2

    :param data: string
    :param format: output format (JPEG, PNG)
    :param block_size: size for one box (in pixels)
    :param border: size for border (in pixels)
    :param background: color for background. Format "#F4F4F4" or (244, 244, 244)
    :param salt: salt for a more varied result (only string)
    :param block_visibility: block transparency (in hex format. 255 - not transparent)
    :param size: number of blocks used
    :param hash_func: function to create a hash (hashlib.sha1, hashlib.sha256, hashlib.md5, etc)

    :return bytes
    """

    if not hash_func:
        if size < 11:
            hash_func = hashlib.sha1
        else:
            hash_func = hashlib.sha512

    hashed = hash_func((str(data) + salt).encode("utf8")).hexdigest()
    color = "#" + hashed[:6] + hex(block_visibility)[2:]

    offset = size % 2
    center = size // 2 + offset
    magic_int_all = 2 ** (size * center)
    magic_int = 2 ** size
    img_size = block_size * size + border * 2

    hash_data = hashed[6:center * 8]

    if len(hash_data) < center * 8 - 6:
        raise Exception("Not enough hash size to generate. Please use another hash function or change size.")

    p = int(hash_data, 16) % magic_int_all
    img = Image.new("RGB", (img_size, img_size), color=background)
    draw = ImageDraw.Draw(img, "RGBA")

    to = range(center)
    for pos in to:
        data = bin((p >> (size * pos)) % magic_int)[2:].zfill(size)
        for index, visible in enumerate(data):
            if int(visible):
                x0 = block_size * pos + border
                y0 = block_size * index + border
                x1 = x0 + block_size - 1
                y1 = y0 + block_size - 1
                draw.rectangle([x0, y0, x1, y1], fill=color)

                if offset and (pos != to[-1]) or not offset:
                    x0 = block_size * ((size - 1) - pos) + border
                    x1 = x0 + block_size - 1
                    draw.rectangle([x0, y0, x1, y1], fill=color)

    byte = io.BytesIO()
    img.save(byte, format=format)
    return byte.getvalue()


def _blocks(data,
            format="png",
            salt="",
            background="#f0f0f0",
            block_visibility=140,
            block_size=50,
            border=25,
            size=3,
            hash_func=None):
    """
    Generating blocks of different colors.
    End image size = size * block_size + border * 2

    :param data: string
    :param format: output format (JPEG, PNG)
    :param block_size: size for one box (in pixels)
    :param border: size for border (in pixels)
    :param background: color for background. Format "#F4F4F4" or (244, 244, 244)
    :param salt: salt for a more varied result (only string)
    :param block_visibility: block
     (in hex format. 255 - not transparent)
    :param size: number of blocks used
    :param hash_func: function to create a hash (hashlib.sha1, hashlib.sha256, hashlib.md5, etc)

    :return bytes
    """

    if not hash_func:
        if size == 2:
            hash_func = hashlib.sha1
        elif size == 3:
            hash_func = hashlib.sha256
        else:
            hash_func = hashlib.sha512

    hashed = hash_func((str(data) + salt).encode("utf8")).hexdigest()
    block_visibility = hex(block_visibility)[2:]

    img_size = size * block_size + border * 2
    img = Image.new("RGB", (img_size, img_size), color=background)
    draw = ImageDraw.Draw(img, "RGBA")

    offset = 0
    for x in range(size):
        for y in range(size):
            color = hashed[offset:offset + 6] + block_visibility

            if len(color) != 8:
                raise Exception("Not enough hash size to generate. Please use another hash function or change size.")

            offset += 6

            x0 = x * block_size + border
            y0 = y * block_size + border
            x1 = x * block_size + block_size - 1 + border
            y1 = y * block_size + block_size - 1 + border
            draw.rectangle([x0, y0, x1, y1], fill="#" + color)

    byte = io.BytesIO()
    img.save(byte, format=format)
    return byte.getvalue()


def _layers(data,
            format="png",
            salt="",
            background="#f0f0f0",
            block_visibility=140,
            block_size=50,
            border=25,
            size=3,
            hash_func=None):
    """
    Generation of blocks of different colors located on each other.
    End image size = size * block_size + border * 2

    :param data: string
    :param format: output format (JPEG, PNG)
    :param block_size: size for one box (in pixels)
    :param border: size for border (in pixels)
    :param background: color for background. Format "#F4F4F4" or (244, 244, 244)
    :param salt: salt for a more varied result (only string)
    :param block_visibility: block transparency (in hex format. 255 - not transparent)
    :param size: number of blocks used
    :param hash_func: function to create a hash (hashlib.sha1, hashlib.sha256, hashlib.md5, etc)

    :return bytes
    """

    if not hash_func:
        if size == 2:
            hash_func = hashlib.sha1
        elif size == 3:
            hash_func = hashlib.sha256
        else:
            hash_func = hashlib.sha512

    hashed = hash_func((str(data) + salt).encode("utf8")).hexdigest()
    block_visibility = hex(block_visibility)[2:]

    img_size = size * block_size + border * 2
    img = Image.new("RGB", (img_size, img_size), color=background)
    draw = ImageDraw.Draw(img, "RGBA")
    block_size = block_size // 2

    offset = 0
    for x in range(size):
        color = hashed[offset:offset + 6] + block_visibility

        if len(color) != 8:
            raise Exception("Not enough hash size to generate. Please use another hash function or change size.")

        offset += 6

        x0 = x * block_size + border
        y0 = x * block_size + border
        x1 = img_size - 1 - x * block_size - border
        y1 = img_size - 1 - x * block_size - border
        draw.rectangle([x0, y0, x1, y1], fill=background)
        draw.rectangle([x0, y0, x1, y1], fill="#" + color)

    byte = io.BytesIO()
    img.save(byte, format=format)
    return byte.getvalue()


def create(data, type="pixels", **kwargs):
    funcs = {
        "pixels": _pixels,
        "blocks": _blocks,
        "layers": _layers,
    }

    if type not in funcs.keys():
        raise Exception("Type does not exist")

    return funcs[type](data, **kwargs)

