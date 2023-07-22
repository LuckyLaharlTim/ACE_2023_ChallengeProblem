from PIL import Image
import numpy as np
import math
from post_test import *


def input_stego(message, im):
    bin_message = ''.join(format(ord(x), 'b') for x in message)
    str_len = len(bin_message)
    num = bin(str_len)[2:]
    final_len = (20 - len(num))*"0" + num
    final_message = final_len + bin_message
    pixels = np.array(im)
    str_index = 0
    for row in range(len(pixels)):
        for pixel in range(len(pixels[row])):
            for channel in range(len(pixels[row][pixel])):
                bin_pixel = bin(pixels[row][pixel][channel])
                if str_index < len(final_message):
                    pixels[row][pixel][channel] = (int(bin_pixel[:-1] + final_message[str_index], 2))
                str_index += 1
    final = Image.fromarray(pixels)
    return final

def decrypt_stego(im):
    pixels = np.array(im).flatten()
    message_len = ""
    for i in range(20):
        message_len += (bin(pixels[i])[-1])
    message = ""
    for j in range(20, 20 + int(message_len, 2)):
        message += ((bin(pixels[j])[-1]))
    final = ""
    for i in range(0, len(message), 7):
        final += chr(int(message[i:i+7], 2))
    return final

def replace_spaces(text):
    new_text = ""
    for i in text:
        if i == " ":
            new_text += "_"
        else:
            new_text += i
    return new_text

ip_address = input("enter ip address of server: ")
port = input("enter port of server: ")
options = input("type 1 to encrypt a png file, 2 to decrypt a png file: ")

if int(options) == 1:
    png_name = input("Type the name of your image including the .png: ")
    image_object = Image.open(png_name)
    one_frame = (len(np.array(image_object).flatten()) - 20)/7
    frame_int = int(math.floor(one_frame))
    new_message = replace_spaces(input("Type your message: "))
    num_frames = math.ceil(len(new_message)/one_frame)

    if len(new_message) > one_frame:
        print("too long, must be lesis than {} characters based on the file", one_frame)
    else:
        new_image_object = input_stego(new_message, image_object)
    name = "encrypted_" + png_name 
    new_image_object.save(name)
    server_post(name, ip_address, port)
    print("File saved as " + name)

    
if int(options) == 2:
    server_get(ip_address, port)
    server_response = Image.open("PicofTheDay.png")
    final = ""
    message_piece = decrypt_stego(server_response)
    final += message_piece
    print(final)

