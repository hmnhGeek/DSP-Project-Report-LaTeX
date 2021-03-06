# Image Steganographer (Edge-Adaptive)

Hide your text messages that are meant to be kept secret from other people, inside an image. Written in pure Python, the data is securely hidden inside the image and is only accessible to those who have the key.

## Requirements
Please install them manually. No `requirements.txt` is available currently. Without these four essential modules, this software will not work. Do upgrade `pip` before installing: `sudo pip --upgrade pip`.

* Numpy
* Scipy
* Pillow
* Matplotlib

## How to use?

* Get into `Project Codes/PVD/`
* Run `python stego-maker-gui.py`

On issuing the command, the following GUI screen will pop up.

<img src="/readme_images/Home.png" width="500">

### Hiding Text
To hide some message in some image, click on `Stego-Generator` button. You will get the following screen. Be ready with a message file (.txt).

<img src="/readme_images/stego-gen.png" width="500">

Now, there is an entry box where it is written `Block size goes here...`. In that, type any integer which represents the block size in which the image will be divided into non-overlapping units B X B. Choose other details and click on `Embedd` button to start the embedding sub-routine. **A parallel process will start, avoid doing any other tasks on the software.**

After embedding will be done, a message box will alert you about this. **The stego-image will be in the same folder, where original image is. It will have a name `final.final.png`.** A key file (binary file) will also be generated `final.<image_name>.<image_format>.dat` in the same folder.
**You can rename these both files as per your choice but the software will generate these names only.**

### Exposing the Stego-Image
To expose a stego-image in which some text is hidden, go to the home page and click on `Stego-Exposer` button.
This window will pop up. Choose the stego image and the correct key file and click on `Decode Image` to start the sub-routine for decoding. Avoid doing any other tasks on the software until this routine gets over.

<img src="/readme_images/expose.png" width="500">

### Bit Planes
Although bit planes is not in any way related to embedding data or extracting data from the image, they are something very important and this software can generate them too.

* Go to home page.
* Click on `Bit Plane Generator`.

You will see this.

<img src="/readme_images/bitplanes.png" width="500">

Enter the bit plane number in the entry box and click on `Generate`. On this part, `threading` is not used. So when `Generate` is clicked, the window may freeze and may stop responding. Be patient and wait till maximum of 1 to 2 minutes in the worst case. Below are LSB and MSB planes respectively.

<img src="/readme_images/bit8.png" width="400">  <img src="/readme_images/bit1.png" width="400">

To read about bit planes, either refer to the `Report` directory in the repository or go though this link - [Bit Planes](https://en.wikipedia.org/wiki/Bit_plane)

## Example
Just so that you see the similarity, the left one is the original image and the right one is the stego image.

<img src="/readme_images/baboon.png" width="400">  <img src="/readme_images/stego.png" width="400">

## Disclaimer 
Distributed over **Standard MIT License**

```
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
 the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
 and to permit persons to whom the Software is furnished to do so, subject to the following conditions: 

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## IMPORTANT NOTE
**The main code resides `Project Codes/PVD/`**, however, individual modules used by the GUI (modules made by the author) are separately available in `Project Codes` directory as well. Their own command line tools are available in their respective directory.

## AUTHOR
This full software pack with its documentation in `Report` folder is done by **Himanshu Sharma**, the owner of this github repository and account. 