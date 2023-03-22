from PIL import Image
from apply import process
import cv2

# Load the image
input_image = cv2.imread('/test/test.png')
# Define the default arguments
prompt = "Old school rapper in the style of 90's vintage anime, surrealism, akira style. detailed line art. fine details. inside a 7/11 in tokyo"
a_prompt = "best quality, extremely detailed"
n_prompt = "longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality"
num_samples = 1
image_resolution = 512
ddim_steps = 20
guess_mode = False
strength = 1.0
scale = 6.0
seed = -2
eta = 0.0
low_threshold = 50
high_threshold = 60

# Call the process function with the arguments
process(input_image, prompt, a_prompt, n_prompt, num_samples, image_resolution, ddim_steps, guess_mode, strength, scale, seed, eta, low_threshold, high_threshold)
