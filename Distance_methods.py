# Ativar o venv:
# .\Venv_AD_ROC\Scripts\activate.bat

# Rodar o código com o Venv:
# python Distance_methods.py

############################
# Distance_methods.py:
#   - código com os métodos de distância para medir a semelhança das strings do modelo com a predição
#####################################################################################################

import jellyfish

def LEVENSHTEIN_DISTANCE(STR_Input, STR_Comparison):
    LEV_distance = jellyfish.levenshtein_distance(STR_Input, STR_Comparison)

    STR_Input_len = len(STR_Input)
    STR_Comparison_len = len(STR_Comparison)

    Biggest_String = max(STR_Input_len, STR_Comparison_len)

    LEV_Correlation = 1 - (LEV_distance/Biggest_String)
    
    return LEV_distance, LEV_Correlation

def JARO_WINKLER_DISTANCE(STR_Input, STR_Comparison):
    JAR_distance = jellyfish.jaro_winkler_similarity(STR_Input, STR_Comparison)
    return JAR_distance


def DISTANCE_EXAMPLES():    #   Esse método é uma símples demonstração do uso dos métodos de distância Levenshtein e Jaro-Winkler.

    string_x = 'Referência'
    string_y = 'Refeen'

    LEV_Distance, LEV_Correlation = LEVENSHTEIN_DISTANCE(string_x, string_y)

    print("\n LEVENSHTEIN DISTANCE = ", LEV_Distance, "\n > Quer dizer que", LEV_Distance,
                                     "é o número de mudanças que (", string_x, ") precisa ser submetida para se transformar em (", string_y, ").")
    
    print(" O valor de Correlação entre (", string_x, ") e (", string_y, ") é o valor ", LEV_Correlation)

    print("------------------------------------------------\n")

    JAR_distance = JARO_WINKLER_DISTANCE(string_x, string_y)

    print(" JARO-WINKLER DISTANCE = ", JAR_distance, "\n > Quer dizer que (", string_x, ") tem o valor de correlação de similaridade de", JAR_distance ,"com (", string_y, "), sendo o mais perto de 1 o mais similar e 0 o menos similar.",
          "Jaro-Winkler trás mais ênfase no prefixo das palavras em comparação.")

    print("------------------------------------------------\n")

    print("Utilize o método de Levenshtein para analizar a correlação entre frazes e o método de Jaro-Winkler para analizar a correlação entre palavras.")


# DISTANCE_EXAMPLES()