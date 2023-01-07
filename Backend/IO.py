
import zipfile, cv2, os

#Takes a list of ImageStructs and outputs a Zipfile object of all the cropped images
def create_zip(crops, image_name):
    path = "./output_images/Crop.zip"
    with zipfile.ZipFile(path, 'a', zipfile.ZIP_DEFLATED) as zfile:
        i = 1
        for crop in crops: 
            img_bytes = cv2.imencode('.jpg', crop)[1].tobytes()
            zfile.writestr('{}_{}.jpg'.format(image_name, i), img_bytes)
            i += 1

#Takes binary data of a zipfile and reads all files within the zipfile. 
'''
def read_zip(path):
    img_ext = ['.png', '.jpg', '.jpeg']

    with ZipFile(path) as zfile:
        for img_file_path in zfile.namelist():
            if img_file_path[-1] != '/':
                for ext in img_ext:
                    if ext in img_file_path: 
                        bytes = ZipFile.read(zfile, name=img_file_path)
                        img = Image.open(io.BytesIO(bytes))
                        yield ImageStruct(img)

'''

def clear_input():
    input_dir = './input_images'
    for file in os.listdir(input_dir):
        os.remove(os.path.join(input_dir, file))