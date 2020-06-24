'''
Created by Anılcan Bulut
https://github.com/anilcanbulut

This code that i have developed can be used to encode a message inside of an image.
The algorithm simply works as follows:

- First, I convert the message to its binary representation. Each character in the message
  is converted to their 8 bit representation.
- Then, since each pixel in the image contain 3 data (RGB values), for a given character that
  is 8 bits, I take three pixels each time to encode only one character information and do the
  same things to others. For example, if there are 50 characters inside of the message, I use
  50*3 = 150 pixels to encode the image.
- How do I encode it? I look at the RGB values of the pixel, if I have the bit 1 to encode and
  if the value of the corresponding pixel value is even I make it odd. If I have the bit 0 to
  encode and the pixel value is odd, I make it even.

These are the three steps that I apply.

'''

import cv2
import argparse

#argument parser is for cmd usage.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="image path")
ap.add_argument("-m", "--message", required=True, help="message to be encoded")

args = vars(ap.parse_args())

#This function converts the each letter in the message to their 8 bit representation and
#returns the binary information in the output.
def message_to_binary(message):
	binary = ''.join('{0:08b}'.format(ord(letter), 'b') for letter in message)
	return binary


#Here, we encode the binary data inside the given image.
def encode_message(img, binary, message_len):
	count = 0
	count2 = 0

	i=0
	j=0
	while i != img.shape[0]:
		while j != img.shape[1]:
			if count2 == message_len:
				break

			if (j % 3) == 0:
				letter_bin = binary[(count2*8):8*(count2+1)]
				for k in range(8):
					if letter_bin[k] == '0':
						if (img[i][j][count] % 2) != 0:
							img[i][j][count] = img[i][j][count] - 1
					if letter_bin[k] == '1':
						if (img[i][j][count] % 2) == 0:
							img[i][j][count] = img[i][j][count] - 1
					count += 1
					if (count % 3) == 0:
						j += 1
						count = 0
				count = 0
				count2 += 1
			j += 1
		i += 1
	return img		

#Image name provided by the user
file_name = args["image"]

#Reading the image by opencv
img = cv2.imread(file_name)

#Message provided by the user
message = args["message"]

#converting the message to binary
binary = message_to_binary(message)
print("Encoded message length: {}".format(len(message)))

#encoding the message inside of the provided image
img = encode_message(img, binary, len(message))

#Saving the encoded image that has the information
cv2.imwrite("encoded_image.png",img)
print("\nThe message is successfully encoded")