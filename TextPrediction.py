# Ativar o venv:
# .\Venv_AD_ROC\Scripts\activate.bat

# Rodar o código com o Venv:
# python TextPrediction.py

############################
# TextPrediction.py:
#   - código com os métodos do Tesseract e ROC em si
####################################################

from pytesseract import Output
import pytesseract
import cv2 
import pandas as pd
import numpy as np
import os
import Global_variables as Gv



pytesseract.pytesseract.tesseract_cmd = Gv.PyThesseract_DIR
print("\n### pytesseract ###")
print(pytesseract)
print("###################\n")

FOLDER_AD_ROC_Input = "./AD_ROC_Input/"
FOLDER_AD_ROC_Predictions = './AD_ROC_Predictions/'

files = os.listdir(FOLDER_AD_ROC_Input)



filename_index = 0

for filename in files:

    filename_index = filename_index + 1

    print(" > Predizendo o texto para o arquivo:",filename, " arquivo de número: ", filename_index)

    IMG_Name = filename

    IMG_Image = FOLDER_AD_ROC_Input + IMG_Name
    IMG_Image = cv2.imread(IMG_Image)


    IMG_Dict = pytesseract.image_to_data(IMG_Image, config='--psm 11', output_type=Output.DICT, lang="por")
    # print(IMG_Dict.keys())



##  MÉTODOS: ###################################################
    def TEXT_ZONING(IMG_Image, IMG_Dict, Box_Pixel_add, IMG_Name, Confidence_Threshold, FOLDER_AD_ROC_Predictions):

        Bounding_Boxes = len(IMG_Dict['text'])

        for i in range(Bounding_Boxes):
            if int(IMG_Dict['conf'][i]) >= Confidence_Threshold:
                (Box_Position_x, Box_Position_y, Box_width, Box_height) = (IMG_Dict['left'][i] - int(Box_Pixel_add/2),
                                                                            IMG_Dict['top'][i] - int(Box_Pixel_add/2),
                                                                            IMG_Dict['width'][i] + int(Box_Pixel_add),
                                                                            IMG_Dict['height'][i] + int(Box_Pixel_add))
                
                IMG_Image = cv2.rectangle(IMG_Image, (Box_Position_x, Box_Position_y),
                                                    (Box_Position_x + Box_width, Box_Position_y + Box_height),
                                                    (0, 255, 0), 2)

        IMG_Name = IMG_Name.replace('.jpg', '')

        IMG_Name = FOLDER_AD_ROC_Predictions + 'BB_' + str(IMG_Name) + '.jpg'

        cv2.imwrite(IMG_Name, IMG_Image)


    def TEXT_DATAFRAME(IMG_Dict, Confidence_Threshold, FOLDER_AD_ROC_Predictions):

        TXT_PREDICTED_Df = pd.DataFrame({'TEXT':IMG_Dict["text"], 'CONFIDENCE':IMG_Dict["conf"], 'FILE INDEX':filename_index})

        TXT_PREDICTED_Df['TEXT'] = TXT_PREDICTED_Df['TEXT'].astype(str)
        TXT_PREDICTED_Df = TXT_PREDICTED_Df[TXT_PREDICTED_Df['CONFIDENCE'] >= Confidence_Threshold]  

        TXT_PREDICTED_Df = TXT_PREDICTED_Df.replace('', pd.NA, inplace=False)

        TXT_PREDICTED_Df = TXT_PREDICTED_Df.dropna()

        TXT_PREDICTED_Df = TXT_PREDICTED_Df.reset_index()
        TXT_PREDICTED_Df['index'] = TXT_PREDICTED_Df.index

        CSV_OUTPUT_Text = FOLDER_AD_ROC_Predictions + 'Predicted_Texts_CSVs/' + filename + '.csv'

        CSV_OUTPUT_Text = CSV_OUTPUT_Text.replace('.jpg', '')

        TXT_PREDICTED_Df.to_csv(CSV_OUTPUT_Text, index=False, sep=";")
################################################################


    TEXT_ZONING(IMG_Image, IMG_Dict, Gv.Box_Pixel_add, IMG_Name, Gv.Confidence_Threshold, FOLDER_AD_ROC_Predictions)

    TEXT_DATAFRAME(IMG_Dict, Gv.Confidence_Threshold, FOLDER_AD_ROC_Predictions)
