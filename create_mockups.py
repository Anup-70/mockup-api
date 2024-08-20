import os
from generate_mockup import generate_mockup  # Import the generate_mockup function
from create_maps import create_maps  # Assuming create_maps is another function you have
from PIL import Image

path_to_template_image = 'base_images/template.jpg'
path_to_mask_image = 'base_images/mask.png'
path_to_displacement_map = 'maps/displacement_map.png'
path_to_lighting_map = 'maps/lighting_map.png'
path_to_adjustment_map = 'maps/adjustment_map.jpg'


def resize_swatch_to_cover(path_to_base_image, file_path):
    # Open the base image and the swatch image
    base_image = Image.open(path_to_base_image)
    swatch_image = Image.open(file_path)
    
    base_width, base_height = base_image.size
    swatch_width, swatch_height = swatch_image.size
    
    # Calculate the scale factors to cover the base image
    width_scale = base_width / swatch_width
    height_scale = base_height / swatch_height
    scale = max(width_scale, height_scale)
    
    # Resize the swatch image
    swatch_image = swatch_image.resize((int(swatch_width * scale), int(swatch_height * scale)))

    # crop the swatch image to the size of the base image
    swatch_width, swatch_height = swatch_image.size
    left = (swatch_width - base_width) / 2
    top = 0
    right = (swatch_width + base_width) / 2
    bottom = base_height

    swatch_image = swatch_image.crop((left, top, right, bottom))

    # Save the resized swatch image

    swatch_image.save(file_path)


def resize_swatch_to_fit(path_to_base_image, file_path, bottom_padding=300):
    base_image = Image.open(path_to_base_image)
    swatch_image = Image.open(file_path)
    
    base_width, base_height = base_image.size
    
    swatch_width, swatch_height = swatch_image.size
    new_width = 400
    new_height = int((new_width / swatch_width) * swatch_height)
    swatch_image = swatch_image.resize((new_width, new_height), Image.ANTIALIAS)
    
    new_image = Image.new("RGB", (base_width, base_height), (0, 0, 0))
    
    paste_x = (base_width - new_width) // 2
    paste_y = base_height - new_height - bottom_padding
    
    if paste_y + new_height > base_height:
        paste_y = base_height - new_height
    
    new_image.paste(swatch_image, (paste_x, paste_y))
    new_image.save(file_path)


def create_mockups(images_list):
    create_maps(path_to_template_image, path_to_mask_image)
    os.makedirs('mockups', exist_ok=True)

    for file in images_list:
        # Generate the file path
        file_path = os.path.join('swatches', file)
        print(file_path)
        if os.path.isfile(file_path):

            path_to_base_image = "base_images/template.jpg"
            resize_swatch_to_fit(path_to_base_image, file_path)

            output_file = os.path.join('mockups', file)

            generate_mockup(
                path_to_template_image,
                path_to_mask_image,
                file_path,
                path_to_displacement_map,
                path_to_lighting_map,
                path_to_adjustment_map,
                output_file
            )

            print(f"Mockup created for {file}")