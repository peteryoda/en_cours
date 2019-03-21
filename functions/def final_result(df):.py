def final_result(df):
    
    temp1 = []
    temp2 = []
    
#     print ("On traite : ",df['slug'])
    
    if df['keep_overlapped_entity_X_phrases'] != []:
        if df['keep_overlapped_entity_X_phrases'][0] not in temp1:
            temp1.append(df['keep_overlapped_entity_X_phrases'][0])
     
    if  df['not_overlapped_entity_X_phrases'] != []:
        if temp1 != []:   
            for each in df['not_overlapped_entity_X_phrases']:
#                 print ("each:",each)
#                 print ("temp1",temp1)

                if each == temp1[0]:
                    resultat = df['not_overlapped_entity_X_phrases']
                else:
                    temp2.append(each)

                    temp2.append(temp1[0])
                    resultat = temp2

        else:
            resultat = df['not_overlapped_entity_X_phrases']
    else :
        resultat = df['keep_overlapped_entity_X_phrases']
        
    del temp1, temp2
    
    return resultat

def difference_title_vs_final_result_X_phrases(df):
    temp = df['title'].strip()
    for each in df['final_result_X_phrases']:
        if each in temp:
#             print ("title: ", df['title'])
#             print ("each: ",each)
            # Si on trouve each au début du titre ou si on trouve each à la fin du titre
#             print(exec("'"+"^" + each + "'"))
            if re.search('^' + each , temp):
#                 print ("au début !", each)
                temp = re.sub(each,'',temp).strip()
            elif re.search(each + '$', temp):
#                 print ("en fin !", each)
                temp = re.sub(each,'',temp).strip()
#             print ("temp :",temp,"\n")
            else:
#                 print ("au milieu !", each)
                temp = re.sub(each,'-',temp).strip()
                
#         print ("\n")
            
    resultat = temp
    return resultat

def add_entity_1_grams(df):
    
    resultat = []
    
    if df['difference_title_vs_final_result_X_phrases'] != '' and len(word_tokenize(df['difference_title_vs_final_result_X_phrases'])) == 1:
        for each in df['final_result_X_phrases']:
#             print (each)
            resultat.append(each)
        resultat.append(df['difference_title_vs_final_result_X_phrases'])
    elif df['difference_title_vs_final_result_X_phrases'] == '': 
        for each in df['final_result_X_phrases']:
            resultat.append(each)
    elif len(word_tokenize(df['difference_title_vs_final_result_X_phrases'])) > 1:
        if '-' not in word_tokenize(df['difference_title_vs_final_result_X_phrases']):
            for each in df['final_result_X_phrases']:
#                 print (each)
                resultat.append(each)
                
        else:
            for each in df['final_result_X_phrases']:
#                 print (each)
                resultat.append(each)
            for each in word_tokenize(df['difference_title_vs_final_result_X_phrases']):
                if each != '-':  
                    resultat.append(each)
                    
    return resultat