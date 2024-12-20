############################
# Global_variables.py:
#   - código com variáveis e métodos e hiperparâmetros de uso pelos outros códigos do projeto
#     do AD-ROC, (Não é executado individualmente)
#############################################################################################

import time
import pandas as pd
from datetime import timedelta
from datetime import datetime

def ELAPSED_TIME(start_time):
    elapsed = (time.time() - start_time)
    elapsed = str(timedelta(seconds=elapsed))
    elapsed = elapsed[0:10]

    return elapsed

start_time = time.time()
procedures_list = []


# Código do Ad-ROC.py:
Exec_Preprocess = True      # Caso queira ignorar o pré-processamento, alterne essa opção para 'False'
######################



# Código do PreProcess.py:
Exec_Grayscale = True           # Para ignorar por completo a etapa de transformação de imagem para grayscale (escala de cinza), alterne para 'False'.
Resize = True                   # Para ignorar o redimensionamento da imagem, alterne para 'False'.
Resize_Amount = 3               # Índice de redimencionamento da imagem, valores altos ajudam a melhorar a qualidade de predição mas aumentam o tamanho das imagens
                                # (ex: Resize_Amount = 3, aumenta o tamanho da imagem em 3 vezes)
                        
Exec_Noise_Smoothing = True    # Para ignorar por completo a etapa de suavização e remoção de ruído, alterne para 'False'.
Exec_smoothing = True
Exec_sharpening = True

Exec_Threshold = True           # Para ignorar por completo a etapa de thresholding (binarização), alterne para 'False'.

Exec_Skew = False               # Para ignorar por completo a etapa de correção de rotação da imagem, alterne para 'False'.
Step = 1                        # Determina quantas vezes será executado a etapa de correção de rotação da imagem.

Exec_Trimm = True               # Para ignorar por completo a etapa de redução de bordas, alterne para 'False'.
additional_trimm = 30           # Número adicional em pixels para a redução das bordas.
#########################



# Código do TextPrediction.py:
PyThesseract_DIR = r'C:\Program Files\Tesseract-OCR\tesseract.exe'      # Diretório da aplicação do Pythesseract, altere para o local onde tenha instalado a aplicação.

Confidence_Threshold = 50   # Valor mínimo de consideração de confiança para a predição das palavras na imagem pelo tesseract
Box_Pixel_add = 2           # número de pixels adicionais para aumentar o retângulo que ressalta as palavras consideradas pelo tesseract
##############################



# Código do PostProcess.py:
current_time = datetime.now().strftime('(%d/%m/%Y) - %H:%M:%S')
Execute_clear = True            # Caso necessite remover símbolos ou potenciais prediçoes incorretas, alterne para 'True'.
Exec_Distance_Methods = True   # Para ignorar por completo a etapa de análise de métodos de distância, alterne para 'False'.


# Roteiro Strings para utilizar os métodos de distância para comparação
# Comparison_Strings = 'Ficha de encaminhamento'    #   Roteiro para os arquivos do tipo ENCAMINHAMENTO

# Comparison_Strings = 'Solicitação de Tratamento Fora de Domicílio'    #   Roteiro para os arquivos do tipo FORA_DOMICILIO_1

# Comparison_Strings = 'Identificação do Paciente'    #   Roteiro para os arquivos do tipo IDENTIFICAÇÃO

# Comparison_Strings = 'Laudo para Solicitação/Autorização de Procedimento Ambulatorial'    #   Roteiro para os arquivos do tipo LAUDO

Comparison_Strings = 'Guia de Referência e Contrarreferência'    #   Roteiro para os arquivos do tipo REFERÊNCIA_CONTRAREFERENCIA

OP_Comparison = 0
###########################