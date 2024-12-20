# Ativar o venv:
# .\Venv_AD_ROC\Scripts\activate.bat

# Rodar o código com o Venv:
# python Image_Converter.py

############################
# Image_Converter.py:
#   - código de tratamento das imagens dos arquivos de input
############################################################

import cv2
import glob
import pymupdf 
import os
import shutil

from PIL import Image 

FOLDER_Inputs = "./Input_Images/"
FOLDER_AD_ROC_Input = "./AD_ROC_Input/"
FOLDER_PDF_TMP = "./Tmp_PDF_to_Image/"

Input_Pdfs = [Pdfs for Pdfs in glob.glob(FOLDER_Inputs + "*.pdf")]

# print("\n***********************************")
# print(" >Pdfs from the input folder:\n", *Input_Pdfs, sep="\n > ")
# print(" [",len(Input_Pdfs), "]")
# print("***********************************")



def MOVE_INPUT_FILES():
    files = os.listdir(FOLDER_Inputs)

    print(" > Há um total de [",len(files),"] arquivos para análise. \n")

    for filename in files:
        shutil.copy(os.path.join(FOLDER_Inputs, filename), os.path.join(FOLDER_AD_ROC_Input, filename))

    for pdfs in glob.glob(FOLDER_AD_ROC_Input + "*.pdf"):
        os.remove(pdfs)

    files = os.listdir(FOLDER_AD_ROC_Input)

    for filename in files:  
        if filename.endswith('.jpg'):
            pass

        else:
            img_name = filename.split('.')[0]

            im = Image.open(FOLDER_AD_ROC_Input + filename).convert("RGB")
            im.save(FOLDER_AD_ROC_Input + img_name + '.jpg')

            im.close()

    for remove_invalid in glob.glob(FOLDER_AD_ROC_Input + "*"):
        if not remove_invalid.endswith('.jpg'):    
            os.remove(remove_invalid)



def DELETE_TMP_FILES(Tmp_files):
    for file in Tmp_files:
        os.remove(file)



def CONVERT_PDF_TO_IMAGE_FILE():
    try:

        Tmp_files_PDF_to_Image = glob.glob(FOLDER_PDF_TMP + "*")
        DELETE_TMP_FILES(Tmp_files_PDF_to_Image)

        for PDF in Input_Pdfs:
            
            Doc_PDF = pymupdf.open(PDF)

            PDF_Name = PDF.replace("./Input_Images\\", "")
            PDF_Name = PDF_Name.replace(".pdf", "")

            for i, PART in enumerate(Doc_PDF):
                pix = PART.get_pixmap()
                pix.save(f"./Tmp_PDF_to_Image/_PART_{i+1}.jpg")

            Doc_PDF.close()


        for filename in os.listdir(FOLDER_PDF_TMP):
            
            rename = PDF_Name + filename
            
            if filename.startswith("_PART_"):
                os.rename(os.path.join(FOLDER_PDF_TMP, filename), os.path.join(FOLDER_PDF_TMP, rename))


        files = os.listdir(FOLDER_PDF_TMP)
        for filename in files:
            shutil.move(os.path.join(FOLDER_PDF_TMP, filename), os.path.join(FOLDER_AD_ROC_Input, filename))
        
        Tmp_files_PDF_to_Image = glob.glob(FOLDER_PDF_TMP + '*')
        
        DELETE_TMP_FILES(Tmp_files_PDF_to_Image)

    except Exception as E:
        print("\n > Erro: [ ", E ," ].")


View_images = False     # Alterne para True caso queira visualizar as imagens de entrada

def VIEW_IMAGES(View_images):
    if View_images == False:
        pass
    elif View_images == True:
        try:
            AD_ROC_Input_Images = [Images for Images in glob.glob(FOLDER_AD_ROC_Input + "*")]

            for IMG in AD_ROC_Input_Images:
                
                IMG_Image = cv2.imread(IMG)
            
                IMG_Name = IMG.replace("./AD_ROC_Input\\", "")
                # print(IMG_Name)

                cv2.imshow(IMG_Name, IMG_Image) 
            
                cv2.waitKey(0)        
            
                cv2.destroyAllWindows() 

        except Exception as E:
            print("\n > Erro: [ ", E ," ].")

CONVERT_PDF_TO_IMAGE_FILE()

MOVE_INPUT_FILES()

# print("\n***********************************")
# print(" >Images for the AD ROC input folder:\n", *AD_ROC_Input_Images, sep="\n")
# print(" [",len(AD_ROC_Input_Images), "]")
# print("***********************************")

VIEW_IMAGES(View_images)
