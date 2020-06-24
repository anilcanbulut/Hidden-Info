import cv2
import argparse

#argument parser is for cmd usage.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="image path")
ap.add_argument("-s", "--size", required=True, help="message size")

args = vars(ap.parse_args())

#This function decodes the message that is hided inside of the image.
#I apply the same steps as I explained it in the encoding code. If the 
#value of the corresponding pixel value is even, this means 0 and if the
#pixel value is odd this means it is bit 1.
def decode_message(img, message_len):
	count = 0
	recovered_bits = []
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if count == message_len*3:
				break

			if(img[i][j][0] % 2) == 0:
				recovered_bits.append("0")
			else:
				recovered_bits.append("1")
				
			if(img[i][j][1] % 2) == 0:
				recovered_bits.append("0")
			else:
				recovered_bits.append("1")
				
			if(img[i][j][2] % 2) == 0:
				recovered_bits.append("0")
			else:
				recovered_bits.append("1")
			
			count += 1
	return recovered_bits

#I take the binary information that is obtained from the image and convert it to the original message.
def binary_to_message(binary):
	recovered_message = []
	count = 0
	for i in range(int(len(binary)/9)):
		recovered_message.append(chr(int(binary[(i*8)+count:(i*8+8)+count],2)))
		count += 1
	return recovered_message

#image name provided by the user
file_name = args["image"]

#reading the image by opencv
img = cv2.imread(file_name)

#message size provided by the user. We need to now how many pixels contain the informations to decode.
message_len = int(args["size"])

#recovered bits are stored inside of a variable
recovered_bits = decode_message(img,message_len)
binary = ''.join('{}'.format(bit) for bit in recovered_bits)

#converting the binary information to the message
recovered_message = binary_to_message(binary)
message = ''.join('{}'.format(letter) for letter in recovered_message)

print(message)