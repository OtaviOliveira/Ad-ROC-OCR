# Ativar o venv:
# .\Venv_AD_ROC\Scripts\activate.bat

# Rodar o código com o Venv:
# python PostProcess.py

############################
# PostProcess.py:
#   - código com os métodos de tratamento e preparação do dataframe dos textos preditos
#######################################################################################

import pandas as pd
import Global_variables as Gv
import Distance_methods as Dm
from itertools import chain
import os
import nltk
from itertools import product

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('portuguese')

from collections import OrderedDict


FOLDER_PREDICTED_CSVs = "./AD_ROC_Predictions/Predicted_Texts_CSVs/"
files = os.listdir(FOLDER_PREDICTED_CSVs)



##  MÉTODOS: ###################################################
def CLEAR_BAD_SYMBOLS(TXT_PREDICTED_Df, OP):
    if OP == 0:   # Operação 0: remove os espaços em branco em excesso e substitui espaços em branco para o símbolo '_'.
        TXT_PREDICTED_Df = TXT_PREDICTED_Df.replace(r' +', ' ', regex=True)
        TXT_PREDICTED_Df = TXT_PREDICTED_Df.replace(r' +', '_', regex=True)

    elif OP == 1: # Operação 1: substitui caracteres especiais para o símbolo '#'.
        TXT_PREDICTED_Df = TXT_PREDICTED_Df.replace(r'\W', '#', regex=True)

    elif OP == 2: # Operação 2: substitui o símbolo '_' para um único espaço em branco e subsitui o símbolo '#' para '_' marcando que ali houve remoção de caracteres especiais.
        TXT_PREDICTED_Df = TXT_PREDICTED_Df.replace(r'_', ' ', regex=True)
        TXT_PREDICTED_Df = TXT_PREDICTED_Df.replace(r'#', '_', regex=True)

    Gv.procedures_list.append("CLEAR_BAD_SYMBOLS")

    return TXT_PREDICTED_Df



def DISTANCE_METHODS(Comparison_Strings, OP, Exec_Distance_Methods):


    def Comparison_Input_List(Comparison_Strings, Input_Strings, OP):
        Comparison_Strings_Individual = Comparison_Strings.split()

        Comparison_Strings_Individual = [line.lower() for line in Comparison_Strings_Individual]

        if OP == 1:
            Comparison_Strings_Individual = [line for line in Comparison_Strings_Individual if line not in stopwords]
        elif OP == 0:
            pass

        Input_Strings = list(set(Input_Strings))

        return Comparison_Strings_Individual, Input_Strings
    


    if Exec_Distance_Methods == True:
    
        TXT_Strings = os.listdir("./Strings_to_Compare/")

        for filename in TXT_Strings:

            Input_Strings_File = filename

            TXT_To_Compare = "./Strings_to_Compare/" + Input_Strings_File


            with open(TXT_To_Compare, encoding="utf8") as Input_Strings:
                Input_Strings = [line.rstrip('\n') for line in Input_Strings]


            Input_Strings = [line.replace(r'_', '') for line in Input_Strings]
            Input_Strings = [line.replace(r'\W', ' ') for line in Input_Strings]

            Input_Strings = [line.lower() for line in Input_Strings]



            def JW_Strings(Input_Strings, Comparison_Strings_Individual):
                JW_Scores_DF = []

                for String in Input_Strings:
                    for Word in Comparison_Strings_Individual:
                        JW_Scores_DF.append(
                            {
                                'Arquivo_Analizado': filename,
                                'Str_Input': String,
                                'Str_Comparação': Word,
                                'Escore_JaroWinkler': Dm.JARO_WINKLER_DISTANCE(String, Word)
                            }
                        )


                JW_Scores_DF = pd.DataFrame(JW_Scores_DF)
                JW_Scores_DF = JW_Scores_DF.sort_values(['Escore_JaroWinkler'], ascending=[False])

                JW_Scores_DF = JW_Scores_DF[JW_Scores_DF['Escore_JaroWinkler'] >= 0.85]
                JW_Scores_DF = JW_Scores_DF.drop_duplicates()

                JW_Scores_DF = JW_Scores_DF.reset_index(drop=True)

                return  JW_Scores_DF



            if OP == 0:     #Operação 0: Método de distância de LEVENSHTEIN

                Comparison_Strings = Comparison_Strings.lower()
                print("\n > Frase para comparação:", Comparison_Strings)

                Comparison_Strings_Individual, Input_Strings = Comparison_Input_List(Comparison_Strings, Input_Strings, Gv.OP_Comparison)

                JW_Scores_DF = JW_Strings(Input_Strings, Comparison_Strings_Individual)
                JW_Scores_DF = list(JW_Scores_DF["Str_Comparação"])
                JW_Scores_DF = [line.lower() for line in JW_Scores_DF]
                JW_Scores_DF = list(set(JW_Scores_DF))

                print('Strings resultantes do Jaro-Winkler: ', JW_Scores_DF)

                
                every_combination = [' '.join(string) for string in product(JW_Scores_DF, repeat=len(JW_Scores_DF))]

                LEV_high_scores = []

                for combination in every_combination:
                    LEV_high_scores.append(Dm.LEVENSHTEIN_DISTANCE(combination, Comparison_Strings)[1])


                LEV_max_score = max(LEV_high_scores)
                LEV_max_score_idx = LEV_high_scores.index(LEV_max_score)
                LEV_max_score_String = every_combination[LEV_max_score_idx]

                LEV_Scores_DF = []
                LEV_Scores_DF.append(
                            {
                                'Arquivo_Analizado': filename,
                                'Melhor_Str': LEV_max_score_String,
                                'Str_Comparação': Comparison_Strings,
                                'Escore_Levenshtein': LEV_max_score
                            }
                        )

                print('Frase com a melhor correspondência: (', LEV_max_score_String, ')| Escore de correlação pela distância de Levenshtein: [', LEV_max_score, ']')

                LEV_Scores_DF = pd.DataFrame(LEV_Scores_DF)

                print('\n> Resultados da comparação das Strings pelo método Levenshtein (frase inteira):\n', LEV_Scores_DF, "\n---------------------\n")
                CSV_OUTPUT_Results = "./Results_Levenshtein/" + filename + '_LEV_RESULTS.csv'

                LEV_Scores_DF.to_csv(CSV_OUTPUT_Results, index=True, sep=";")
            #---------------------------------------------------------------



            #---------------------------------------------------------------
            if OP == 1:     #Operação 1: Método de distância de JARO-WINKLER

                Comparison_Strings_Individual, Input_Strings = Comparison_Input_List(Comparison_Strings, Input_Strings, Gv.OP_Comparison)

                print("\n > Strings para comparação:", Comparison_Strings_Individual)

                JW_Scores_DF = JW_Strings(Input_Strings, Comparison_Strings_Individual)


                print('\n> Resultados da comparação das Strings pelo método Jaro-Winkler (palavra por palavra):\n', JW_Scores_DF, "\n---------------------\n")
                CSV_OUTPUT_Results = "./Results_Jaro_Winkler/" + filename + '_JW_RESULTS.csv'

                JW_Scores_DF.to_csv(CSV_OUTPUT_Results, index=True, sep=";")



################################################################



for filename in files:

    current = FOLDER_PREDICTED_CSVs + filename
    TXT_PREDICTED_Df = pd.read_csv(current, sep=';')

    if Gv.Execute_clear == True:
        print(" > Limpando texto do CSV: ",filename)

        TXT_PREDICTED_Df = CLEAR_BAD_SYMBOLS(TXT_PREDICTED_Df, 0) # Operação 0: remove os espaços em branco em excesso e substitui espaços em branco para o símbolo '_'.
        TXT_PREDICTED_Df = CLEAR_BAD_SYMBOLS(TXT_PREDICTED_Df, 1) # Operação 1: substitui caracteres especiais para o símbolo '#'.

        bad_symbols_number = TXT_PREDICTED_Df['TEXT'].str.count("#")
        bad_symbols_number_sum = bad_symbols_number.sum()

        TXT_PREDICTED_Df = CLEAR_BAD_SYMBOLS(TXT_PREDICTED_Df, 2) # Operação 2: substitui o símbolo '_' para um único espaço em branco e subsitui o símbolo '#' para '_' marcando que ali houve remoção de caracteres especiais.

        print(" > Número total de símbolos removidos: [",bad_symbols_number_sum,"]\n")



    head, sep, tail = filename.partition('.')
    filename = head

    filename_txt = ".\\Final_Output_Results\\FinalTXT_" + filename + ".txt"

    TXT_PREDICTED_Df = TXT_PREDICTED_Df[TXT_PREDICTED_Df['TEXT'] != ""]
    TXT_PREDICTED_Df = TXT_PREDICTED_Df[TXT_PREDICTED_Df['TEXT'] != "_"]

    TXT_PREDICTED_Df['TEXT'].to_csv(filename_txt, header=None, index=False, sep=';', mode='w')



    Header_File  = filename_txt + '_HEADER.txt'
    word_number = len(TXT_PREDICTED_Df['TEXT']) - 1
    procedures_list = list(OrderedDict.fromkeys(Gv.procedures_list))
    procedures_list = ', '.join(procedures_list)
    elapsed = Gv.ELAPSED_TIME(Gv.start_time)

    FinalTxt_Header = ["+++ INFO: ++++++++++++++",
                        "   Documento: " + filename,
                        "   Data: " + Gv.current_time + "  Tempo de execução total do AD-ROC: " + elapsed,
                        "   Procedimentos realizados: " + procedures_list,
                        "   Número de Palavras totais preditas: " + str(word_number),
                        "++++++++++++++++++++++++\n",
                        "+++ TEXTO: +++++++++++++"]
    


    with open(filename_txt, 'r', encoding="utf8") as read_objc, open(Header_File, 'w', encoding="utf8") as write_objc:

        for line in FinalTxt_Header:
            write_objc.write(line + '\n')

        for line in read_objc:
            write_objc.write(line)

    os.remove(filename_txt)
    os.rename(Header_File, filename_txt)

DISTANCE_METHODS(Gv.Comparison_Strings, Gv.OP_Comparison, Gv.Exec_Distance_Methods)