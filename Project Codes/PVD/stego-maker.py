import argparse as ap
import pvd.pvd

parser = ap.ArgumentParser()
parser.add_argument('image', type=str, help="Image location")
parser.add_argument('--hide', action='store_true', help="Pass this to hide message.")
parser.add_argument('--expose', action='store_true', help="Pass this to expose text.")
args = parser.parse_args()

if args.image and args.hide:
    message = str(raw_input("Enter a message: "))
    block_size = int(input("Enter block size: "))
    pvd.pvd.pixelate(args.image, message, block_size)
else:
    key_file = str(raw_input("Key File: "))
    print(pvd.pvd.decode(args.image, key_file))
