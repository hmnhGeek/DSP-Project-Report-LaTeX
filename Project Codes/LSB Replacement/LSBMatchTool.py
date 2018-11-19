import argparse as ap 
import lsb_matching

parser = ap.ArgumentParser()
parser.add_argument('image', type=str, help='Pass image address here.')
parser.add_argument('-e', action='store_true', dest='e', help='Pass this to expose stego-image.')
args = parser.parse_args()

if not args.e:
	# this means we have to hide the data in the image.
	text = raw_input("Enter the text: ")
	print lsb_matching.lsb_matching.image_embedding(args.image, text, args.image+"-stego.png")
else:
	key = input("Enter the key: ")
	msg = lsb_matching.lsb_matching.expose_message(args.image, key)
	print msg
