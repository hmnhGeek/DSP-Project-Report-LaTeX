import argparse as ap
import imagediff.imagediff

parser = ap.ArgumentParser()
parser.add_argument('image1', type=str, help='Stego image.')
parser.add_argument('image2', type=str, help='Cover image.')
parser.add_argument('--percent', action='store_true', help='Percentage difference in the images.')
parser.add_argument('--heatmap', action='store_true', help="Generate matplolib heatmap.")
args = parser.parse_args()

print("This program uses Python 3. Beware...")

try:
    if args.image1 and args.image2:
        if args.percent and not args.heatmap:
            imagediff.imagediff.bruteforce(args.image1, args.image2)
        elif not args.percent and args.heatmap:
            imagediff.imagediff.heatMap(args.image1, args.image2)
        elif args.percent and args.heatmap:
            imagediff.imagediff.bruteforce(args.image1, args.image2)
            imagediff.imagediff.heatMap(args.image1, args.image2)
        else:
            print("Pass some argument. Issue --help flag to get help.")
    else:
        print("Number of images don't match the required dataset.")

except:
    print("You might be using Python 2.x. Please use Python 3.")
