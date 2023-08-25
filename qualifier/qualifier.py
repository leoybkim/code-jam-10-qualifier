from PIL import Image

def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.


    1. 
    The tile size allows splitting the image completely with no remainders. 
    For example a tile size of `(128, 128)` divides an image of size `(256, 256)` into exactly 4 tiles. 
    A tile size of 127 or 129 would not work with this image.

    2. 
    The ordering of the tiles is valid. 
    A valid ordering is one where each source tile in the input image is used exactly once.
    """

    R = image_size[1] // tile_size[1]
    C = image_size[0] // tile_size[0]
    tile_count = R*C

    can_split = (image_size[0] % tile_size[0] == 0) and (image_size[1] % tile_size[1] == 0)
    can_order = len(ordering) == len(set(ordering)) and len(ordering) == tile_count

    return can_split and can_order


def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """
    with Image.open(image_path) as img:
        if not valid_input(img.size, tile_size, ordering):
            raise ValueError("The tile size or ordering are not valid for the given image")

        W, H = img.size
        tW, tH = tile_size

        R = H // tH # number of rows
        C = W // tW # number of columns

        # (0,0) is the top left corner of the image
        # crop function takes in coordinates of the image (left, top, right, bottom)
        # Iterate each row and column to find the next set of coordinates

        tiles = []

        for r in range(R):
            for c in range(C):
                left = c * tW
                top = r * tH
                right = left + tW
                bottom = top + tH
                tile = img.crop((left, top, right, bottom))
                tiles.append(tile)

        output = Image.new(img.mode, img.size)  # mode could be RGB or RGBA

        # Stich the image back up as instructed in the ordering list
        for r in range(R):
            for c in range(C):
                i = r*C + c
                if i < len(tiles):
                    output.paste(tiles[ordering[i]], (c*tW, r*tH))

        output.save(out_path)
