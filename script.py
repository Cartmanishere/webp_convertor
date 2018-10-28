from PIL import Image
import os
import math
import numpy as np

def get_width_and_height(img, resize_to=512):
    size = list(img.size)

    if max(size) < resize_to or min(size) > resize_to:
    	dim = 0 if size[0] > size[1] else 1
    	size[~dim] = math.floor(size[~dim] * (resize_to / size[dim]))
    	size[dim] = resize_to

    elif size[0] > resize_to:
        size[1] = math.floor(size[1] * (resize_to / size[0]))
        size[0] = resize_to

    elif size[1] > resize_to:
        size[0] = math.floor(size[0] * (resize_to / size[1]))
        size[1] = resize_to

    size = tuple(size)

    assert max(size) <= 512, 'Size: {} - Image_size - {}'.format(size, img.size)

    return size, img.resize(size)


def alpha_padding(img, pad_dims=512):
    '''
    Convert the image into pad_dims x pad_dims by padding with alpha channel
    '''
    (w, h), img = get_width_and_height(img, resize_to=pad_dims)

    orig_img = np.array(img)
    if orig_img.shape[-1] < 3:
    	orig_img = np.array(img.convert('RGBA'))

    main_img = np.zeros((pad_dims, pad_dims, 4))
    main_img[:, :, 3] = 0
    main_img = main_img
    main_img = main_img.astype('uint8')
    
    
    if h < pad_dims and w < pad_dims:
        v_diff = (pad_dims - h) // 2
        h_diff = (pad_dims - w) // 2
        
        if orig_img.shape[-1] == 4:
            main_img[v_diff:h+v_diff, h_diff:w+h_diff, :] = orig_img

        elif orig_img.shape[-1] == 3:
            main_img[v_diff:h+v_diff, h_diff:w+h_diff, :3] = orig_img
            main_img[v_diff:h+v_diff, h_diff:w+h_diff, 3] = 255

        else:
            raise ValueError('No operation specified for {} mode images.'.format(orig_img.shape[-1]))


    elif h < pad_dims:
        # Alpha pad the h dimension
        diff = pad_dims - h
        offset = diff // 2

        if orig_img.shape[-1] == 4:
            main_img[offset:h+offset, :, :] = orig_img

        elif orig_img.shape[-1] == 3:
            main_img[offset:h+offset, :, :3] = orig_img
            main_img[offset:h+offset, :, 3] = 255

        else:
            raise ValueError('No operation specified for {} mode images.'.format(orig_img.shape[-1]))

    elif w < pad_dims:
        # Alpha pad the w dimension
        diff = pad_dims - w
        offset = diff // 2

        if orig_img.shape[-1] == 4:
            main_img[:, offset:w+offset, :] = orig_img

        elif orig_img.shape[-1] == 3:
            main_img[:, offset:w+offset, :3] = orig_img
            main_img[:, offset:w+offset, 3] = 255

        else:
            raise ValueError('No operation specified for {} mode images.'.format(orig_img.shape[-1]))


    else:
    	if orig_img.shape[-1] == 4:
    		main_img = orig_img

    	elif orig_img.shape[-1] == 3:
    		main_img[:, :, :3] = orig_img
    		main_img[:, :, 3] = 255

    	else:
            raise ValueError('No operation specified for {} mode images.'.format(orig_img.shape[-1]))


    assert main_img.shape == (pad_dims, pad_dims, 4), 'There was some error in resizing. Padded image has dimensions {}'.format(main_img.shape)
    
    
    return Image.fromarray(main_img, 'RGBA')

if __name__ == "__main__":
    files = { l: os.path.join(data_dir, l) for l in os.listdir(data_dir) }

    for filename, filepath in zip(files.keys(), files.values()):

    	img = Image.open(filepath)

    	new_img = alpha_padding(img, pad_dims=512)

    	new_img.save(os.path.join(tmp_dir, filename))

    	print('{} saved in {}/ folder'.format(filename, tmp_dir))



