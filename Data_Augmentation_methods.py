# Ativar o venv:
# .\Venv_AD_ROC\Scripts\activate.bat

# Rodar o código com o Venv:
# python Data_Augmentation_methods.py

############################
# Data_Augmentation_methods.py:
#   - Esse código tem o propósito de realizar o aumento de dados das imagens de entrada, basicamente cria versões com ruído,
#     versões com rotação e versões com ambas operações para testar a capacidade de pré-processamento do AD-ROC.
#
#     Esse código é executado de maneira individual, não execute antes ou após a aplicação principal do AD-ROC,
#     transfira ou exclua os arquivos gerados.
############################################################


from Image_Converter import *
import numpy as np
import imutils
from skimage.util import random_noise
from skimage import img_as_ubyte

FOLDER_AD_ROC_Input = "./AD_ROC_Input/"
FOLDER_AUGMENTATION_RESULTS = "./Augmentation_results/"

files = os.listdir(FOLDER_AD_ROC_Input)

CONVERT_PDF_TO_IMAGE_FILE()

MOVE_INPUT_FILES()

def DATA_AUGMENTATION_METHODS(OP):
    if OP == 1:     # Rotacionar a imaggem em um ângulo aleatório entre -90 e 90
        for image in files:

            CURRENT_IMAGE_PATH = FOLDER_AD_ROC_Input + image
            CURRENT_IMAGE = cv2.imread(CURRENT_IMAGE_PATH)

            degrees = np.random.randint(-90, 90)

            CURRENT_IMAGE_Rotated = imutils.rotate_bound(CURRENT_IMAGE, degrees)

            print("Graus em que a imagem foi rotacionada > ", degrees)

            cv2.imshow("Rotacionada", CURRENT_IMAGE_Rotated)
            cv2.waitKey(0)

            AUGMENTED_IMAGE_PATH = FOLDER_AUGMENTATION_RESULTS + image
            cv2.imwrite(AUGMENTED_IMAGE_PATH, CURRENT_IMAGE_Rotated)


    if OP == 2:
        for image in files:

            CURRENT_IMAGE_PATH = FOLDER_AD_ROC_Input + image
            CURRENT_IMAGE = cv2.imread(CURRENT_IMAGE_PATH)

            CURRENT_IMAGE_Noisy = random_noise(CURRENT_IMAGE, mode='gaussian')

            cv2.imshow("Ruidosa", CURRENT_IMAGE_Noisy)
            cv2.waitKey(0)

            AUGMENTED_IMAGE_PATH = FOLDER_AUGMENTATION_RESULTS + image
            cv2.imwrite(AUGMENTED_IMAGE_PATH, img_as_ubyte(CURRENT_IMAGE_Noisy))

    if OP == 3:
        for image in files:

            CURRENT_IMAGE_PATH = FOLDER_AD_ROC_Input + image
            CURRENT_IMAGE = cv2.imread(CURRENT_IMAGE_PATH)

            degrees = np.random.randint(-90, 90)

            CURRENT_IMAGE_Rotated = imutils.rotate_bound(CURRENT_IMAGE, degrees)

            print("Graus em que a imagem foi rotacionada > ", degrees)

            CURRENT_IMAGE_Noisy = random_noise(CURRENT_IMAGE_Rotated, mode='gaussian')

            cv2.imshow("Ruidosa e rotacionada", CURRENT_IMAGE_Noisy)
            cv2.waitKey(0)

            AUGMENTED_IMAGE_PATH = FOLDER_AUGMENTATION_RESULTS + image
            cv2.imwrite(AUGMENTED_IMAGE_PATH, img_as_ubyte(CURRENT_IMAGE_Noisy))



DATA_AUGMENTATION_METHODS(3)