import pandas as pd

#-------------------------------------------------------------------------------------------------------------------------#
# ------------------ 1. Fonction import des dataframes à partir des fichiers source .csv ---------------------------------#
#-------------------------------------------------------------------------------------------------------------------------#
def create_df(name_df, path, encoding_value):

    # dict_of_dfs est un dictionnaire pour stocker tous les dataframes
    # dict_of_dfs = dict()
    
    # path = '/home/hapax94/Documents/vincent/fichiers_générés_par_Hervé_181217/wac_181217/wac/'
    all_file = path + name_df + '.csv'

    liste_tuples = []
    
    idx_last_slash = all_file.rfind("/") + 1
    idx_dot = all_file.index(".")
    name_file = all_file[idx_last_slash:idx_dot]

    print ("name_file:",name_file)

    # On prend la dernière partie après le dernier "_"
    which_file = name_file.split('_')[-1]
    
    which_type = name_file.split('_')[0]
    
    print ("which_file", which_file)
    
    if  which_file == 'descriptions' and which_type == 'wine':
    	# 12/02/2017 : on appelle "label" plutot "title"
        # list_of_columns = ['slug','fil_ariane','label','url', 'description','image_url']
        if name_file == 'wine_figaro_descriptions':
            list_of_columns = ['description']
        else:    
            list_of_columns = ['slug','fil_ariane','title','url', 'description','image_url']
        
    elif which_file == 'descriptions' and which_type == 'smart':
        list_of_columns = ['slug','rayon0','rayon1','rayon2','title','description']
    elif which_file == 'properties' and which_type == 'wine':
        # ATTENTION ! ajout de last_col pour pouvoir charger le fichier 
#         list_of_columns = ['label','not_relevant_index','property', 'property_label']
        list_of_columns = ['slug','not_relevant_index','property', 'property_label','last_col']
        print ("list_of_columns:",list_of_columns)
    
    elif which_file == 'categories' and which_type == 'wine':
        list_of_columns = ['slug','category','count','description', 'fil_ariane','category_url']
        
    elif which_file == 'variants' and which_type == 'wine':
        # "xslug|xnum|xtype|xoption|xprice|xavailability|xend_date|xper_price|xcro_price|xloy_price"
        list_of_columns = ['slug','not_relevant_index','type','option', 
                           'price','availability','end_date','price_per_unit','cro_price','loy_price']
    # 09/01/2018 : ajout cas fichier "footprints"
    elif which_file == 'footprints' and which_type == 'wine':
        # list_of_columns = ['slug', 'distributeur', 'label', 'option', 'price', 'cro_price', 'url','undefined','region', 'appellation', 'millesime', 'color', 'size', 'image_url']
        list_of_columns = ['slug', 'distributeur', 'title', 'option', 'price', 'cro_price', 'url','undefined','region', 
                           'appellation', 'millesime', 'color', 'size', 'image_url']

    # 23/01/2019 : données "Bio"
    elif which_type == 'orgc':
        
        if  which_file == 'category':
            list_of_columns = ['xid','xbreadcrumb','xtitle','xslug', 'xcount','xdescription','xmeta_title','xmeta_description', 'xmeta_keywords', 'xapi', 'xweb', 'xcrawled_at', 'xurl', 'xrun']
        
        elif which_file == 'offer':
            list_of_columns = ['xid','xnum','xoffer_num','xbrand','xtitle','xvariant','xseller','xprice','xstock','xgtin','xsku','xquality','xshipping','xpromo','xpremium','xextra_price','xentry_price','xbest_offer','xbest_price','xfull_price','xunit_pricing','xseller','xslug','ximg','xbreadcrumb','xsubtitle','xprize','xgrade','xgrades','xcustom1','xcustom2','xcustom3','xcustom4','xcustom5','xcustom6','xcustom7','xcustom8','xapi','xweb','xcrawled_at','xurl','xrun']

        elif which_file == 'product':
            list_of_columns = ['xid','xtitle','xbrand','xbreadcrumb','xsubtitle','xdescription','xslug','ximg','xmeta_title','xmeta_description','xmeta_keywords','xapi','xweb','xcrawled_at','xurl','xru']

    liste_tuples = []
    file = open(all_file, 'r',encoding=encoding_value) 
    
    if which_type == 'wine':
        line_number = 0
    elif which_type == 'smart':
        line_number = 1
    elif which_type == 'orgc':
        line_number = 0

    for line in file:
        line_number = line_number + 1
        if (line_number == 1 and which_type == 'wine') or (line_number == 2 and which_type == 'smart'):
            nb_sep = line.count('\t')
            print("Nb de séparateurs tabulation sur la 1ère ligne: ",nb_sep)
         
        line_without_eof = line.replace('\t\n','')
        line_splitted = line_without_eof.split('\t')
        
        if (line_number == 1 and which_type == 'wine') or (line_number == 2 and which_type == 'smart'):
            print(line_splitted)
            # 10/01/2018 pour les fichiers Pricing 
            # print("Nb de champs sur la 1ère ligne: ",nb_sep - 1)
            print("Nb de champs sur la 1ère ligne: ",nb_sep)
        
        if (line_number >= 1 and which_type == 'wine') or (line_number >= 3 and which_type == 'smart'):
            liste_tuples.append(line_splitted)

        # 23/01/2019 : pour les données "Bio", les fichiers contiennent les noms des colonnes
        # donc la lecture des fichiers ne commencent qu'à la 2ème ligne
        if which_type == 'orgc' and line_number != 1:
            liste_tuples.append(line_splitted)
        
#         if line_number == 1:
#             print("Données de la 1ère ligne pour", name_df, " : ", liste_tuples)
        
    # Enfin on transforme la liste en dataframe grâce à item tuples
    
    
    df_out = pd.DataFrame.from_records(liste_tuples,columns = list_of_columns)
    #dict_of_dfs[name_df] = temp_df

    file.close() 

    #return(dict_of_dfs[name_df])
    return df_out

#-----------------------------------------------------------------------------------------------------------------------------#
# --------------------------- 2. Fonction de nettoyage des titles ------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------#

import re
import unicodedata
def cleansing_titles(my_str):
    # NB si on travaille avec des Series, pas besoin de mettre str.<function_name>
    # 27/12/2017: suppression des accents
    # 29/12/2017: on enlève la ponctuation (les "," et ":" on laisse les apostrophes "'")
    
    # Pour toute ponctuation on ferait:
    #     my_str.translate(None, string.punctuation)
    
    # On remplace les ponctuations tiret, virgule et deux-points 
    # quand elles servent de séparateurs
    
    # 12/02/2018 : je reporte après, la suppression des tirets, virgules et des deux-points
#     my_str = (my_str.strip()).lower().replace('-',' ').replace(' , ',' ').replace(' : ',' ')
    my_str = (my_str.strip()).lower()
    
    # 12/02/2018 : constaté qu'on peut avoir un "blanc" du type ' '
    # donc suppression du mot ' ' ou '' ou "'" si on le rencontre
    #  and word not in [' ','',"'"]:
    
    # 30/12/2017: enfin, on enlève les guillemets (<=> double quotes ?)
    # 13/02/2018: ajout suppression de "'" et remplacement de '.' par ' '
    
    # 21/02/2018: ATTENTION on garde les  '.'
    #  my_str = my_str.replace('"','').replace(" ' ",'').replace('.',' ')
    my_str = my_str.replace('"','').replace(" ' ",'')
    
    # 11/02/2018 : on enlève aussi cf cas rencontré pour "wac": "Domaine Georges Vernay Viognier ''Le Pied De Samson'' 2016"
    my_str = my_str.replace("''",'')
    
    # 30/12/2017 : enlever les blancs inutiles
    my_str = re.sub(re.compile(r'\s+'), ' ',my_str)
    
    my_str = unicodedata.normalize('NFD', my_str).encode('ascii', 'ignore').decode('ascii')
    # 29/12/2017: on enlève la ponctuation (les ",:, etc..." sauf les apostrophes "'")

    return my_str


#-----------------------------------------------------------------------------------------------------------------------------#
# --------------------------- 2. Fonction qui extrait les n grams ------------------------------------------------------------#
# --------------------------- * Input *: un texte et un paramètre n ----------------------------------------------------------#
#---------------------------- * Output *: les n grams ------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------#
# import nltk
# from nltk.tokenize import word_tokenize

# def find_ngrams(input_list,ngrams_indice):
        
#     ngram_list = []
#     ngrams_indice = ngrams_indice - 1
#     print (input_list)
#     # print ("word_tokenize(input_list)",word_tokenize(input_list))
#     for i in range(len(word_tokenize(input_list)) - ngrams_indice):
#         to_append = ''
# #         print ("valeur de i:",i)
#         for k in range(ngrams_indice + 1):
# #             print("valeur de k:",k)
#             if k < ngrams_indice: 
#                 to_append = to_append + word_tokenize(input_list)[i+k]  + " "
#             else:
# #                 print ('to_append: ',to_append)
#                 to_append = to_append + word_tokenize(input_list)[i+k]

#         ngram_list.append((to_append))
    
#     return ngram_list

def find_ngrams(input_list,ngrams_indice):
        
    ngram_list = []
    ngrams_indice = ngrams_indice - 1
    
    for i in range(len(input_list)-ngrams_indice):
        to_append = ''
#         print ("valeur de i:",i)
        
        for k in range(ngrams_indice + 1):
#             print("valeur de k:",k)
            if k < ngrams_indice:
                
                to_append = to_append + input_list[i+k]  + " "
            else:
#                 print ('to_append: ',to_append)
                to_append = to_append + input_list[i+k]

        ngram_list.append((to_append))
    
    return(ngram_list)
