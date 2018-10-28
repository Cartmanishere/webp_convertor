from concurrent.futures import as_completed, ThreadPoolExecutor
from subprocess import check_output
import os
from script import *
import time
from PIL import ImageSequence

THREADS = 4 # Change this to increase multithreading

data_dir = os.path.join(os.getcwd(), 'data')

def assure_folder_exists(folder, root=data_dir):
    full_path = os.path.join(root, folder)
    if os.path.isdir(full_path):
        return folder, full_path
    else:
        os.mkdir(full_path)
        return folder, full_path

_, data_dir = assure_folder_exists('data', root=os.getcwd())
_, tmp_dir = assure_folder_exists('tmp', root=os.getcwd())
_, output_dir = assure_folder_exists('output', root=os.getcwd())

def get_image(image_path):
	
	if image_path.split('.')[-1] == 'gif':
		img = Image.open(image_path)
		frame = next(ImageSequence.Iterator(img)).copy().convert('RGBA')
		return frame

	else:
		return Image.open(image_path)

def convert_image(image_path, folder_name):
    '''
    Main function which will convert the image and store it in the appropriate folder
    '''
    img = get_image(image_path)
    new_img = alpha_padding(img, pad_dims=512)
    name = '.'.join(image_path.split('\\')[-1].split('.')[:-1]) + '.png'
    
    # Save this temporarily
    new_img.save(os.path.join(tmp_dir, name))
    
    # Convert this image
    out_name, out_path = assure_folder_exists(folder_name, root=output_dir)
    filename = '.'.join(name.split('.')[:-1]) + '.webp'

    # command = "cwebp -q 75 -quiet tmp\\{} -o output\\{}\\{}".format(name, folder_name, filename)

    command = 'cwebp -q 75 -quiet "{}" -o "{}"'.format(os.path.join(tmp_dir, name), os.path.join(out_path, filename))

    check_output(command, shell=True)
    # os.unlink(os.path.join(tmp_dir, name))

    return os.path.join(out_path, filename)


if __name__ == "__main__":
# # Get all the pack images
    packs = {l:os.path.join(data_dir, l) for l in os.listdir(data_dir)}

    for name, pack in zip(packs.keys(), packs.values()):

        print('Converting pack.. {}'.format(name))

        files = { l: os.path.join(pack, l) for l in os.listdir(pack) }

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            f = [ executor.submit(convert_image, filepath, name) for filepath in files.values()]

            for future in as_completed(f):
            	future.result()

        print('Converted {} stickers'.format(len(files.values())))
        print('Time taken with {} threads {:.3f}s'.format(THREADS, time.time() - start_time))
        print()

        # Clean the tmp directory after work
        for i in os.listdir(tmp_dir):
        	os.unlink(os.path.join(tmp_dir, i))