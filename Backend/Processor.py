import cv2

def preprocess_img(self, img):
    img = self.grayscale(img)
    img = self.threshold(img, 100)
    img = self.blur(img)
    return self.resize(img, 900, 900)

def blur(self, img):
    return cv2.GaussianBlur(img, (3, 3), 0)

def grayscale(self, img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def threshold(self, img, thresh):
    return cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)

def resize(img, height, width):
    old_w, old_h, channels = img.shape
    w_ratio, h_ratio = old_w/width, old_h/height
    new_dim = (width, height)
    return cv2.resize(img, new_dim, interpolation=cv2.INTER_AREA), w_ratio, h_ratio

# Calculates the percentage of each box being within the other. Box1 and box2 are represented by (x1,y1,x2,y2) where x2 > x1 an y2 > y1.
def regionOfConvergence(box1, box2):
    x1 = max(box1[0], box2[0])
    x2 = min(box1[2], box2[2])
    y1 = max(box1[1], box2[1])
    y2 = min(box1[3], box2[3])

    if x1 >= x2 or y1 >= y2:
        return [0, 0]

    conv_area = (x2-x1)*(y2-y1)
    box1_area = (box1[2]-box1[0])*(box1[3]-box1[1])
    box2_area = (box2[2]-box2[0])*(box2[3]-box2[1])

    return [conv_area/box1_area, conv_area/box2_area]

    # Compares all the bounding boxes of an image and gets rid of overlapping bounding boxes.

def rm_low_acc_boxes(img_boxes, acc_floor):
    boxes = []
    for box in img_boxes:
        if box[1] >= acc_floor:
            boxes.append(box)
    return boxes

def rm_overlap_boxes(img_boxes):
    i = 0
    while i < len(img_boxes):
        j = i+1
        while j < len(img_boxes):
            roc = regionOfConvergence(img_boxes[i][0], img_boxes[j][0])

            if roc[0] >= 0.5 or roc[1] >= 0.5:
                if img_boxes[i][1] > img_boxes[j][1] or (img_boxes[i][1] == img_boxes[j][1] and roc[0] > roc[1]):  # if confidence of box i > box j
                    img_boxes.remove(img_boxes[j])
                else:
                    img_boxes.remove(img_boxes[i])
                    j = i+1
            else:
                j += 1
        i += 1

    return img_boxes

def process_bounding_boxes(img_boxes):
    b_boxes = rm_low_acc_boxes(img_boxes, 0.66)
    if len(b_boxes) == 0: return []
    b_boxes = rm_overlap_boxes(b_boxes)
    if len(b_boxes) == 0: return []
    coords = []
    for coord, confidence in b_boxes:
        coords.append(coord)
    return coords

#Takes a single image and returns a list of crops from image
def crop(bounding_box_list, image):
    #crops = model.get_bouding_boxes(image)  #crops = [((x,y,x,y), c), ...]
    crops = process_bounding_boxes(bounding_box_list)   #coordCrop = [(x,y, x,y), ...]
    if crops == []: return []
    cropped_img = get_crops(crops, image)
    return cropped_img   

def get_crops(boxes, image):
    crops = []
    for box in boxes:
        x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        crops.append(image[y1:y2, x1:x2])
    return crops

