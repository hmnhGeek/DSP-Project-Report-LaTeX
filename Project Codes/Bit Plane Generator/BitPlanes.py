from bit_planes import bit_planes as bpl
import argparse as ap 

parser = ap.ArgumentParser()
parser.add_argument('image', type=str, help='Image path')
parser.add_argument('plane', type=int, help='Bit plane number')
args = parser.parse_args()

if args.image and args.plane:
	bpl.generateBitPlane(args.image, args.plane)
