import unittest
import io

from PIL import Image

from customidenticon import create


class ForHashTest:
    def __init__(self, *args):
        pass

    def hexdigest(self):
        return "000000" + "f"*150


def gen_image(data, type="pixels", **kwargs):
    identicon = create(data, type, **kwargs)
    return Image.open(io.BytesIO(identicon))


def gen_for_test(type, size=3, block_size=1):
    return gen_image("Test",
                     type=type,
                     hash_func=ForHashTest,
                     border=1,
                     background=(250, 250, 250),
                     block_size=block_size,
                     size=size,
                     block_visibility=255)


class IdenticonTestCase(unittest.TestCase):
    def test_pixels_create(self):
        image = gen_image("test")
        self.assertEqual(image.format, "PNG")
        self.assertEqual((200, 200), image.size)

        image = gen_image("test", format="jpeg")
        self.assertEqual(image.format, "JPEG")
        self.assertEqual((200, 200), image.size)

        image = gen_image("test", border=10, block_size=10, size=6)
        size = 6 * 10 + 10 * 2  # size * block_size + border * 2
        self.assertEqual((size, size), image.size)

    def test_blocks_create(self):
        image = gen_image("test", type="blocks")
        self.assertEqual(image.format, "PNG")
        self.assertEqual((200, 200), image.size)

        image = gen_image("test", type="blocks", format="jpeg")
        self.assertEqual(image.format, "JPEG")
        self.assertEqual((200, 200), image.size)

        image = gen_image("test", type="blocks", border=10, block_size=10, size=4)
        size = 4 * 10 + 10 * 2  # size * block_size + border * 2
        self.assertEqual((size, size), image.size)

    def test_layers_create(self):
        image = gen_image("test", type="layers")
        self.assertEqual(image.format, "PNG")
        self.assertEqual((200, 200), image.size)

        image = gen_image("test", type="layers", format="jpeg")
        self.assertEqual(image.format, "JPEG")
        self.assertEqual((200, 200), image.size)

        image = gen_image("test", type="layers", border=10, block_size=10, size=4)
        size = 4 * 10 + 10 * 2  # size * block_size + border * 2
        self.assertEqual((size, size), image.size)

    def test_pixels_generated_image(self):
        image = gen_for_test("pixels", 5)
        image_size = 7  # size + border * 2

        self.assertEqual((image_size, image_size), image.size)

        rgb_im = image.convert("RGB")
        color = (0, 0, 0)
        background = (250, 250, 250)
        for x in range(image_size):
            for y in range(image_size):
                if x == 0 or x == image_size-1 or y == 0 or y == image_size-1:
                    self.assertEqual(background, rgb_im.getpixel((x, y)))
                else:
                    self.assertEqual(color, rgb_im.getpixel((x, y)))

    def test_blocks_generated_image(self):
        image = gen_for_test("blocks", 5)
        image_size = 7  # size + border * 2

        self.assertEqual((image_size, image_size), image.size)

        rgb_im = image.convert("RGB")
        color1 = (0, 0, 0)
        color2 = (255, 255, 255)
        background = (250, 250, 250)
        for x in range(image_size):
            for y in range(image_size):
                if x == 0 or x == image_size-1 or y == 0 or y == image_size-1:
                    self.assertEqual(background, rgb_im.getpixel((x, y)))
                else:
                    if x == 1 and y == 1:
                        self.assertEqual(color1, rgb_im.getpixel((x, y)))
                    else:
                        self.assertEqual(color2, rgb_im.getpixel((x, y)))

    def test_layers_generated_image(self):
        image = gen_for_test("layers", 3, 2)
        image_size = 8  # size * block_size + border * 2

        self.assertEqual((image_size, image_size), image.size)

        rgb_im = image.convert("RGB")
        color1 = (0, 0, 0)
        color2 = (255, 255, 255)
        background = (250, 250, 250)
        for x in range(image_size):
            for y in range(image_size):
                if x == 0 or x == image_size-1 or y == 0 or y == image_size-1:
                    self.assertEqual(background, rgb_im.getpixel((x, y)))
                else:
                    if x == 1 or x == image_size-2 or y == 1 or y == image_size-2:
                        self.assertEqual(color1, rgb_im.getpixel((x, y)))
                    else:
                        self.assertEqual(color2, rgb_im.getpixel((x, y)))


if __name__ == "__main__":
    unittest.main(warnings="ignore")
