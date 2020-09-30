import os
import cv2
import numpy as np
from WordSegmentation import wordSegmentation, prepareImg
import DataLoader
from Model import NeuralNetwork, retrieve_model_with_create_arhitecture, retrieve_model
from tensorflow import keras

images_for_model = []
considered_indent = 60


def send_words_to_nn(img):
    list_word, num_with = getImages(img)
    NN = NeuralNetwork(create=False)
    model = retrieve_model()
    model2 = keras.Model(model.get_layer('input').input, model.layers[14].output)
    text = ''
    for i in range(0, num_with):
        print(i)
        if list_word[i].shape[0] == 32 and list_word[i].shape[1] == 32:
            text = text + '\n'
        elif list_word[i].shape[0] % 10 == 0:
            text = text + '  ' * (int(list_word[i].shape[0] / 10))
        else:
            word = DataLoader.prepare_image_with_img_arg(list_word[i])
            aux, interpreted_text = NN.return_text(word, model2)
            text = text + interpreted_text + ' '
            print(interpreted_text)
    return text


def increase_contrast_and_apply_treshold(image):
    img = image
    img = cv2.GaussianBlur(img, (5, 5), 0)
    # -----Converting image to LAB Color model-----------------------------------
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    # -----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)

    # -----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)

    # -----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv2.merge((cl, a, b))

    # -----Converting image from LAB Color model to RGB model--------------------
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    # cv2.imwrite('out/final_constrast.png', final)
    # read
    image = final
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Remove horizontal
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (150, 1))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)

    # Remove vertical
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 150))
    detected_lines_v = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=1)
    cnts2 = cv2.findContours(detected_lines_v, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts2 = cnts2[0] if len(cnts2) == 2 else cnts2[1]
    for c in cnts2:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)
    # cv2.imwrite('out/detected_lines_v.png', 255 - detected_lines_v)
    # Repair image
    # repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 6))
    # result = 255 - cv2.morphologyEx(255 - image, cv2.MORPH_CLOSE, repair_kernel, iterations=2)
    # cv2.imwrite('out/tresh.png', thresh)
    # cv2.imwrite('out/detected_lines.png', 255-detected_lines)
    # cv2.imwrite('out/image.png', image)
    # # cv2.imwrite('out/result.png', result)
    if len(detected_lines) == 0:
        # kernel = np.ones((2, 2))
        # img = cv2.erode(thresh, kernel, iterations=2)
        return thresh
    image_black_and_white = np.array(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    nr_min = np.median(image_black_and_white)
    detected_lines = np.asarray(detected_lines)
    img = np.minimum(image_black_and_white.astype(int) + detected_lines.astype(int),
                     np.ones((detected_lines.shape[0], detected_lines.shape[1])) * nr_min)
    # cv2.imwrite('out/result_minus.png', img)

    detected_lines_v = np.asarray(detected_lines_v)
    img = np.minimum(img.astype(int) + detected_lines_v.astype(int),
                     np.ones((detected_lines.shape[0], detected_lines.shape[1])) * nr_min)
    # cv2.imwrite('out/result_si_vertical.png', img)


    img = img.astype('uint8')
    ret, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    # cv2.imwrite('out/tresh1.png', img)
    kernel = np.ones((3, 1))
    img = cv2.erode(img, kernel, iterations=2)
    kernel2 = np.ones((1, 3))
    img = cv2.erode(img, kernel2, iterations=2)
    # cv2.imwrite('out/%s/eroded2.png' % path, img)
    # img = cv2.morphologyEx(255-img, cv2.MORPH_CLOSE, kernel)
    # cv2.imwrite('out/close1.png', img)
    # cv2.waitKey(0)
    kernel3 = np.ones((2, 2))
    img = cv2.dilate(img, kernel3, iterations=3)
    th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 61, 14)
    # cv2.imwrite('out/treshhold3.png', th3)
    return th3


def getImages(img):
    """reads images from data/ and outputs the word-segmentation to out/"""

    # read input images from 'in' directory
    imgFiles = os.listdir('data/')
    for (i, f) in enumerate(imgFiles):
        print('Segmenting words of sample %s' % f)

        # read image, prepare it by resizing it to fixed height and converting it to grayscale
        img = increase_contrast_and_apply_treshold(img)
        img = prepareImg(img, img.shape[0])
        # execute segmentation with given parameters
        # -kernelSize: size of filter kernel (odd integer)
        # -sigma: standard deviation of Gaussian function used for filter kernel
        # -theta: approximated width/height ratio of words, filter function is distorted by this factor
        # - minArea: ignore word candidates smaller than specified area
        res = wordSegmentation(img, kernelSize=151, sigma=50, theta=7, minArea=2500)
        # minimum_x = np.amin(res[0], axis=0)  151
        # write output to 'out/inputFileName' directory
        if not os.path.exists('out/%s' % f):
            os.mkdir('out/%s' % f)

        # iterate over all segmented words
        print('Segmented into %d words' % len(res))
        rand_nou = np.ones((32, 32, 3)) * (255, 0, 0)
        indent = 0
        k = 0
        first_word_in_line = True
        last_new_line_word = (-1, -1, -1, -1)
        for (j, w) in enumerate(res):
            (wordBox, wordImg) = w
            (x, y, wi, h) = wordBox
            # cv2.imwrite('umm.png', wordImg)

            # cv2.imwrite('out/%s/%d.png'%(f, j), wordImg) # save word
            # cv2.rectangle(img,(x,y),(x+wi,y+h),0,1) # draw bounding box in summary image

            img_resized = DataLoader.extract_img(wordImg)

            # pxmin = np.min(img_resized)
            # pxmax = np.max(img_resized)
            # imgContrast = (img_resized - pxmin) / (pxmax - pxmin) * 255
            #
            # # increase line width
            # kernel = np.ones((3, 3), np.uint8)
            # imgMorph = cv2.erode(imgContrast, kernel, iterations=1)

            if indent < 0:
                indent = 0

            if j != 0:
                lastWB, last_img = res[j - 1]
                if y >= lastWB[1] + lastWB[3]-5:
                    print('new line:' + str(k) + ', ' + str(j))
                    images_for_model.append(rand_nou.astype('uint8'))
                    cv2.imwrite('out/%s/%d.png' % (f, k), rand_nou.astype('uint8'))
                    k += 1

                    if last_new_line_word[0] != -1:
                        if x > last_new_line_word[0] + considered_indent:
                            indent += 1
                            if indent > 0:
                                indent_ = np.ones((indent * 10, 32, 3)) * (0, 255, 0)
                                images_for_model.append(indent_.astype('uint8'))
                                cv2.imwrite('out/%s/%d.png' % (f, k), indent_.astype('uint8'))
                            k += 1
                        elif x < last_new_line_word[0] - considered_indent:
                            indent -= 1
                            if indent > 0:
                                indent_ = np.ones((indent * 10, 32, 3)) * (0, 255, 0)
                                images_for_model.append(indent_.astype('uint8'))
                                cv2.imwrite('out/%s/%d.png' % (f, k), indent_.astype('uint8'))
                                k += 1
                        elif indent > 0:
                            indent_ = np.ones((indent * 10, 32, 3)) * (0, 255, 0)
                            images_for_model.append(indent_.astype('uint8'))
                            cv2.imwrite('out/%s/%d.png' % (f, k), indent_.astype('uint8'))
                            k += 1

                    last_new_line_word = wordBox

            # write
            cv2.imwrite('out/%s/%d.png' % (f, k), img_resized)
            k += 1
            images_for_model.append(img_resized)
            first_word_in_line = False

        # output summary image with bounding boxes around words
        cv2.imwrite('out/%s/summary.png' % f, img)
        print(len(images_for_model))
        return images_for_model, k


if __name__ == '__main__':
    print(send_words_to_nn())
