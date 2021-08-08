from PIL import Image
import os

def animation_generator():
    # SETUP START #
    NO_OF_LEDs = 256
    DIN_PIN = 6
    SPEED = 100
    # path to your GIF file
    im = Image.open("src/source.gif")
    # SETUP END #

    z = 0
    try:
        while 1:
            z = z + 1
            im.seek(im.tell() + 1)
            # RESIZE FOR 16x16 MATRIX
            img = im.resize((16, 16), Image.ANTIALIAS)
            img.save("frames/frame_" + str(z) + ".png")

            width, height = img.size
            print(str(width) + 'x' + str(height))

            read_image_rgb = img.convert("RGB")
            width_range = range(width)
            height_range = range(height)

            color_list = []

            for n_height in height_range:
                for n_width in width_range:
                    rgb_pixel_value = read_image_rgb.getpixel((n_width, n_height))
                    print(str(n_width) + 'x' + str(n_height))
                    color_list.append('0x' + str('%02x%02x%02x' % rgb_pixel_value))

            a = 0
            temp_list = []
            backward_txt = open("temp/backward_" + str(z) + ".txt", "w")
            for element in color_list:
                a = a + 1
                if a <= width:
                    temp_list.append(element)
                if a == width:
                    for line in reversed(temp_list):
                        backward_txt.write(line + ", ")
                    temp_list.clear()
                    a = 0
                    backward_txt.write("\n")
            backward_txt.close()

            b = 0
            forward_txt = open("temp/forward_" + str(z) + ".txt", "w")
            for element in color_list:
                b = b + 1
                if b <= width:
                    forward_txt.write(element + ", ")
                if b == width:
                    forward_txt.write("\n")
                    b = 0
            forward_txt.close()

            backward_lines = []
            with open("temp/backward_" + str(z) + ".txt") as f:
                for line in f:
                    backward_lines.append(line)

            forward_lines = []
            with open("temp/forward_" + str(z) + ".txt") as f:
                for line in f:
                    forward_lines.append(line)

            for i in range(1, len(backward_lines), 2):
                backward_lines[i] = forward_lines[i]

            backward_forward_txt = open("temp/backward_forward_" + str(z) + ".txt", "w")
            backward_forward_txt.write("const long Frame_" + str(z) + "[] PROGMEM = \n")
            backward_forward_txt.write("{\n")
            for element in backward_lines:
                backward_forward_txt.write(element)
            backward_forward_txt.write("}")
            backward_forward_txt.close()

    except EOFError:
        pass

    total_files = 0
    total_frames = []
    DIR = 'frames'
    for base, dirs, files in os.walk(DIR):
        for Files in files:
            total_files += 1
            total_frames.append(total_files)

    # write .ino output file
    matrix_ino = open("matrix_animation.ino", "w")
    matrix_ino.write('#include "FastLED.h" \n')
    matrix_ino.write('#include <avr/pgmspace.h> \n')
    matrix_ino.write('\n')
    matrix_ino.write('#define DIN_PIN ' + str(DIN_PIN) + '\n')
    matrix_ino.write('#define NO_OF_LEDs ' + str(NO_OF_LEDs) + '\n')
    matrix_ino.write('\n')
    matrix_ino.write('CRGB leds [' + str(NO_OF_LEDs) + '];')
    matrix_ino.write('\n')
    matrix_ino.write('\n')
    for no_of_frames in total_frames:
        with open("temp/backward_forward_" + str(no_of_frames) + ".txt") as f:
            for line in f:
                matrix_ino.write(line)
                print(line)
            matrix_ino.write(';\n\n')
    matrix_ino.write('\n\n\n')
    matrix_ino.write('void setup() { \n')
    matrix_ino.write('  FastLED.addLeds<NEOPIXEL,DIN_PIN>(leds, NO_OF_LEDs); \n')
    matrix_ino.write('  FastLED.setBrightness(20); \n')
    matrix_ino.write('}')
    matrix_ino.write('\n\n\n')
    matrix_ino.write('void loop() { \n')
    matrix_ino.write('  for(int frame_count = 0; frame_count < ' + str(len(total_frames)) + '; frame_count++) {\n')
    for no_of_frames in total_frames:
        matrix_ino.write('      for(int i = 0; i < NO_OF_LEDs; i++) { \n')
        matrix_ino.write('          leds[i] = pgm_read_dword(& (Frame_' + str(no_of_frames) + '[i])); \n')
        matrix_ino.write('      }\n\n')
        matrix_ino.write('  FastLED.show();\n')
        matrix_ino.write('  delay(' + str(SPEED) + ');\n\n')
    matrix_ino.write('  } \n')
    matrix_ino.write('} \n')
