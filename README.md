# Image Steganographer (Edge-Adaptive)

Hide your text messages that are meant to be kept secret from other people, inside an image. Written in pure Python, the data is securely hidden inside the image and is only accessible to those who have the key.

## How to use?

* Get into `Project Codes/PVD/`
* Run `python stego-maker-gui.py`

On issuing the command, the following GUI screen will pop up.

<img src="/readme_images/Home.png" width="500">

### Hiding Text
To hide some message in some image, click on `Stego-Generator` button. You will get the following screen.

<img src="/readme_images/stego-gen.png" width="500">

Now, there is an entry box where it is written `Block size goes here...`. In that, type any integer which represents the block size in which the image will be divided into non-overlapping units B X B.