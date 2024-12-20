# Ativar o venv:
# .\Venv_AD_ROC\Scripts\activate.bat

# Rodar o código com o Venv:
# python PreProcess.py

############################
# PreProcess.py:
#   - código com os métodos de ratamento e preparação das imagens
############################################################

import cv2
import os
import numpy as np
import skimage 
import Global_variables as Gv

from scipy.stats import mode
from skimage.filters import unsharp_mask

FOLDER_AD_ROC_Input = "./AD_ROC_Input/"
files = os.listdir(FOLDER_AD_ROC_Input)
print(" > [",len(files),"] arquivos serão pré-processados em seguida: \n")


##  MÉTODOS: ###################################################

def SHOW_FOR_TESTING(input_image):
    cv2.imshow("Test", input_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def TRIMM_BORDERS(Exec_Trimm, additional_trimm):
    if Exec_Trimm == True:
        for image in files:

            CURRENT_IMAGE_PATH = FOLDER_AD_ROC_Input + image
            CURRENT_IMAGE = cv2.imread(CURRENT_IMAGE_PATH)

            CURRENT_IMAGE_DILATE = cv2.GaussianBlur(CURRENT_IMAGE, (3,3), 0)
            CURRENT_IMAGE_DILATE = cv2.dilate(CURRENT_IMAGE_DILATE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))

            CURRENT_IMAGE_DILATE = cv2.cvtColor(CURRENT_IMAGE_DILATE, cv2.COLOR_BGR2GRAY)
            CURRENT_IMAGE_DILATE = cv2.threshold(CURRENT_IMAGE_DILATE, 127, 255, cv2.THRESH_BINARY)[1]


            White_points = cv2.findNonZero(CURRENT_IMAGE_DILATE) # x,y order

            White_points_x = []
            White_points_y = []

            White_points_len = len(White_points)

            for p in range(White_points_len):

                White_points_x.append(int(White_points[p][0][0]))
                White_points_y.append(int(White_points[p][0][1]))


            White_points_x = list(filter(lambda num: num != 0, White_points_x))
            White_points_y = list(filter(lambda num: num != 0, White_points_y))


            White_points_min_x = min(White_points_x)
            White_points_max_x = max(White_points_x)

            White_points_min_y = min(White_points_y)
            White_points_max_y = max(White_points_y)


            start_point = ((White_points_min_x + additional_trimm), (White_points_min_y + (additional_trimm * 2))) # x, y
            end_point = ((White_points_max_x - additional_trimm), (White_points_max_y - (additional_trimm * 2))) # x, y
        

            color = (255, 255, 255)
            thickness = 3

            CURRENT_IMAGE_Fit = cv2.rectangle(CURRENT_IMAGE, start_point, end_point, color, thickness)
            CURRENT_IMAGE_Fit = CURRENT_IMAGE_Fit[start_point[1]:end_point[1], start_point[0]:end_point[0]]

            cv2.imwrite(CURRENT_IMAGE_PATH, CURRENT_IMAGE_Fit)

            Gv.procedures_list.append("REMOVE_BACKGROUND")

    else:
        print(" > Ignorando a etapa de remoção de fundo de imagem.")


def GRAYSCALE_IMAGES(Exec_Grayscale, Resize, Resize_Amount):
    if Exec_Grayscale == True:
        for image in files:

            CURRENT_IMAGE_PATH = FOLDER_AD_ROC_Input + image

            CURRENT_IMAGE = cv2.imread(CURRENT_IMAGE_PATH)
            CURRENT_IMAGE_Gray = cv2.cvtColor(CURRENT_IMAGE, cv2.COLOR_BGR2GRAY)
            OLD_IMAGE_shape = CURRENT_IMAGE.shape   

            if(Resize == True):
                CURRENT_IMAGE_Gray = cv2.resize(CURRENT_IMAGE_Gray, None, fx = Resize_Amount, fy = Resize_Amount, interpolation = cv2.INTER_CUBIC)
            else:
                pass

            CURRENT_IMAGE_shape = CURRENT_IMAGE_Gray.shape   
            print(" > Alterando a imagem para escala de cinza: ", CURRENT_IMAGE_PATH, " | Tamanho original: ", OLD_IMAGE_shape, " | Tamanho redimensionado (Caso haja redimensionamento): ", CURRENT_IMAGE_shape)

            cv2.imwrite(CURRENT_IMAGE_PATH, CURRENT_IMAGE_Gray)

            Gv.procedures_list.append("GRAYSCALE_IMAGES")

    else:
        print(" > Ignorando a etapa de escala de cinza (Grayscale).")


def THRESHOLD_IMAGES(Exec_Threshold):
    if Exec_Threshold == True:
        for image in files:

            CURRENT_IMAGE_PATH = FOLDER_AD_ROC_Input + image
            CURRENT_IMAGE = cv2.imread(CURRENT_IMAGE_PATH, cv2.IMREAD_GRAYSCALE)

            CURRENT_IMAGE_Thresh = cv2.adaptiveThreshold(CURRENT_IMAGE, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 31, 15)

            print(" > Binarizando a seguinte imagem: ", CURRENT_IMAGE_PATH)

            cv2.imwrite(CURRENT_IMAGE_PATH, CURRENT_IMAGE_Thresh)

            Gv.procedures_list.append("THRESHOLD_IMAGES")

    else:
        print(" > Ignorando etapa de binarização (Thresholding).")


def NOISE_REDUCTION_SMOOTHING(Exec_Noise_Smoothing, Exec_smoothing, Exec_sharpening):
    if Exec_Noise_Smoothing == True:
        for image in files:

            CURRENT_IMAGE_PATH = FOLDER_AD_ROC_Input + image

            print(" > Diminuindo ruído para a seguinte imagem: ", CURRENT_IMAGE_PATH)

            CURRENT_IMAGE = cv2.imread(CURRENT_IMAGE_PATH, cv2.IMREAD_GRAYSCALE)

            if Exec_smoothing == True:
                CURRENT_IMAGE_Denoised = skimage.restoration.denoise_tv_chambolle(CURRENT_IMAGE, weight = 0.2)

            if Exec_sharpening == True:
                CURRENT_IMAGE_Denoised = unsharp_mask(CURRENT_IMAGE, radius = 20, amount = 2)


            cv2.imwrite(CURRENT_IMAGE_PATH, skimage.img_as_ubyte(CURRENT_IMAGE_Denoised))

            Gv.procedures_list.append("NOISE_REDUCTION_SMOOTHING")

    else:
        print(" > Ignorando etapa de redução de ruído.")


def IMAGE_SKEWING(Exec_Skew, Step):
    if Exec_Skew == True:
        for image in files:
  
            CURRENT_IMAGE_PATH = FOLDER_AD_ROC_Input + image
            CURRENT_IMAGE = cv2.imread(CURRENT_IMAGE_PATH, cv2.IMREAD_GRAYSCALE)

            print(" > Corrigindo ângulo para a seguinte imagem (passo: ", Step, "): ", CURRENT_IMAGE_PATH)


            h, theta, d = skimage.transform.hough_line(CURRENT_IMAGE)
            angles = skimage.transform.hough_line_peaks(h, theta, d)[1]
            angle = np.rad2deg(mode(angles)[0])


            if (angle < 0):
                angle = angle + 90
                
            else:
                angle = angle - 90
                
            CURRENT_IMAGE_ROTATED = skimage.transform.rotate(CURRENT_IMAGE, angle, preserve_range=True).astype(np.uint8)

            cv2.imwrite(CURRENT_IMAGE_PATH, CURRENT_IMAGE_ROTATED)

            Gv.procedures_list.append("IMAGE_SKEWING")

    else:
        print(" > Ignorando etapa de rotação (skewing).")
################################################################


################################################################
GRAYSCALE_IMAGES(Gv.Exec_Grayscale, Gv.Resize, Gv.Resize_Amount)
print("----")


NOISE_REDUCTION_SMOOTHING(Gv.Exec_Noise_Smoothing, Gv.Exec_smoothing, Gv.Exec_sharpening)
print("----")


THRESHOLD_IMAGES(Gv.Exec_Threshold)
print("----")


if Gv.Exec_Skew == True:
    for Step in range(Gv.Step):
        IMAGE_SKEWING(Gv.Exec_Skew, Step = (Step + 1))
        print("----")


TRIMM_BORDERS(Gv.Exec_Trimm, Gv.additional_trimm)
print("----")