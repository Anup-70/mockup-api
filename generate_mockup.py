import subprocess

def generate_mockup(template, mask, artwork, displacement_map, lighting_map, adjustment_map, out):
    tmp = 'mpcs/mockup.mpc'

    # Function to run a command and handle errors
    def run_command(cmd):
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    
    # Get dimensions of the template
    def get_image_size(image_path):
        cmd = ['magick', 'identify', '-format', '%wx%h', image_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        width, height = map(int, result.stdout.strip().split('x'))
        return width, height

    # Calculate perspective coordinates based on center alignment
    template_width, template_height = get_image_size(template)
    artwork_width, artwork_height = get_image_size(artwork)

    x_center = template_width // 2
    y_center = template_height // 2

    # Calculate the coordinates based on the center of the image
    coords = f'0,0,{x_center - artwork_width // 2},0,' \
             f'0,{artwork_height},{x_center - artwork_width // 2},{template_height},' \
             f'{artwork_width},0,{x_center + artwork_width // 2},0,' \
             f'{artwork_width},{artwork_height},{x_center + artwork_width // 2},{template_height}'

    # Add border
    cmd1 = ['magick', artwork, '-bordercolor', 'transparent', '-border', '1', tmp]
    run_command(cmd1)

    # Add perspective transform
    cmd2 = [
        'magick', template, '-alpha', 'transparent', '(', tmp, '+distort', 'perspective', coords, ')',
        '-background', 'transparent', '-layers', 'merge', '+repage', tmp
    ]
    run_command(cmd2)

    # Set background color
    cmd3 = ['magick', tmp, '-background', 'transparent', '-alpha', 'remove', tmp]
    run_command(cmd3)

    # Add displacement
    cmd4 = ['magick', tmp, displacement_map, '-compose', 'displace', '-set', 'option:compose:args', '20x20', '-composite', tmp]
    run_command(cmd4)

    # Add highlights
    cmd5 = ['magick', tmp, '(', '-clone', '0', lighting_map, '-compose', 'hardlight', '-composite', ')', '+swap', '-compose', 'CopyOpacity', '-composite', tmp]
    run_command(cmd5)

    # Adjust colors
    cmd6 = ['magick', tmp, '(', '-clone', '0', adjustment_map, '-compose', 'multiply', '-composite', ')', '+swap', '-compose', 'CopyOpacity', '-composite', tmp]
    run_command(cmd6)

    # Compose artwork
    cmd7 = ['magick', template, tmp, mask, '-compose', 'over', '-composite', '-resize', '800', out]
    run_command(cmd7)

# Example usage:
# generate_mockup('path_to_template_image', 'path_to_mask_image', 'path_to_artwork_image', 'path_to_displacement_map', 'path_to_lighting_map', 'path_to_adjustment_map', 'path_to_output_image')