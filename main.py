import static
import animation
from art import *
import shutil

matrix_generator = text2art("ARDUINO    MATRIX     GEN")
print(matrix_generator)

print("1. Generate matrix from one static image")
print("2. Generate matrix from gif")

generator_option = input("Choose operation: ")

if generator_option == str(1):
    static.stactic_generator()
if generator_option == str(2):
    animation.animation_generator()
