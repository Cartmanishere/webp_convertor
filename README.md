## Webp Convertor

This module converts images (png, jpg and gif) into webp format.

This module is used to generate usable sticker version for the new whatsapp sticker update.

Currently, all the images are generated strictly in 512x512 dimensions.

If the image is bigger than or smaller than 512, then it is resized to 512x512 while mainitaining aspect ratio.

Any differences in dimensions are resolved by adding alpha padding (transparent padding.)

### Dependencies

This script requires following python libraries installed in your environemnt

1. ```numpy```
2. ```PIL```
3. Webp convertor which can be obtained from [here].(https://storage.googleapis.com/downloads.webmproject.org/releases/webp/index.html)

### Usage

- Clone the latest repository locally

- Put the images you want to convert into `data` folder in the root of the repository -
	
``` 
 Webp Convertor
    |
    ├───data
          ├─── pack1
          ├─── pack2        
          ├─── pack3
```

Where each `pack` is a folder containing source images.

- Run the program like this - `python convert.py`

- You will find the converted images in `ouptut` folder

### Known Issues :

* This script is heavily under development. Always switch to the latest verison before using.
* Some formats or some edge cases in the images may generate error. Please open an issue if you find such instances.

### License :

This project is licensed under the terms of the MIT license.

