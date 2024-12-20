# Ativar o venv:
# .\Venv_AD_ROC\Scripts\activate.bat

# Rodar o código com o Venv:
# python AD_ROC.py

############################
# AD_ROC.py:
#   - código principal de execução da aplicação do AD_ROC
############################################################

import time
import os
import Global_variables as Gv

print('\n▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄')
print('██▀▄─██▄─▄▄▀█▀▀▀▀▀██▄─▄▄▀█─▄▄─█─▄▄▄─█')
print('██─▀─███─██─█████████─▄─▄█─██─█─███▀█')
print('▀▄▄▀▄▄▀▄▄▄▄▀▀▀▀▀▀▀▀▀▄▄▀▄▄▀▄▄▄▄▀▄▄▄▄▄▀')
print('▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n')

filepath = os.path.abspath(__file__)
direcotry_name = os.path.dirname(filepath)
os.chdir(direcotry_name)

print("Path de operação atual: ", filepath, "\n")


def EXECUTE_PREPROCESS(Exec_Preprocess):
    if Exec_Preprocess == True:
        print("[", Gv.ELAPSED_TIME(Gv.start_time), "] > Executando etapas de Pré-Processamento, chamando código PreProcess.py...")
        import PreProcess
        print("[", Gv.ELAPSED_TIME(Gv.start_time), "] > Pré-Processamento finalizado.")
    else:
        print("[", Gv.ELAPSED_TIME(Gv.start_time), "] > Ignorando etapas de Pré-Processamento.")



print("\n***********************************")
print("[", Gv.ELAPSED_TIME(Gv.start_time), "] > Convertendo os arquivos de Input...")
import Image_Converter
print("\n***********************************")

EXECUTE_PREPROCESS(Gv.Exec_Preprocess)

print("\n***********************************")
print("[", Gv.ELAPSED_TIME(Gv.start_time), "] > Executando etapa de predição de texto, chamando código TextPrediction.py...")
import TextPrediction
print("[", Gv.ELAPSED_TIME(Gv.start_time), "] > Etapa de predição de texto finalizada.")


print("\n***********************************")
print("[", Gv.ELAPSED_TIME(Gv.start_time), "] > Executando etapa de Pós-Processamento, chamando código PostProcess.py...")
import PostProcess
print("[", Gv.ELAPSED_TIME(Gv.start_time), "] > Etapa de Pós-Processamento finalizada, confira os arquivos .txt gerados.")

print('\n\n***** AD-ROC ENCERRADO *****')
print('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄')