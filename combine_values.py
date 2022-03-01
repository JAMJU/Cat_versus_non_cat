#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created september 2021
    by Juliette MILLET
    scrip to combine gamma score and wav2vec and overlap score and wav2vec
"""
import pandas as pd

def add_combination(filename, filename_out):
    dataframe = pd.read_csv(filename)
    df_french = dataframe.loc[dataframe['language_indiv'] == 'french']
    df_english = dataframe.loc[dataframe['language_indiv'] == 'english']



    dico_values = {'english': {}, 'french': {}}
    for name in [ 'distAssim', 'wav2vec_10k_transf4', 'wav2vec_french_transf4_dtw','wav2vec_english_transf4_dtw' ]: # names to change if you want other column's titles
        dico_values['english'][name] = {'std': df_english[name].std(),'mean': df_english[name].mean()}
        dico_values['french'][name] = {'std': df_french[name].std(), 'mean': df_french[name].mean()}

    f_in = open(filename, 'r')
    ind = f_in.readline().replace('\n', '')
    f_out = open(filename_out, 'w')
    f_out.write(ind + ',combi_distA_w2,combi_distA_w2engnon,combi_distA_w2frnon\n')
    ind = ind.split(',')

    for line in f_in:
        new_line  = line.replace('\n', '').split(',')
        lang = new_line[ind.index('language_indiv')]
        values = dico_values[lang]
        dico_val_indiv = {}
        for name in ['distAssim', 'wav2vec_10k_transf4' , 'wav2vec_french_transf4_dtw','wav2vec_english_transf4_dtw']:
            dico_val_indiv[name] = (float(new_line[ind.index(name)]) - values[name]['mean'])/values[name]['std']

        f_out.write(','.join(new_line + [  str(dico_val_indiv['distAssim'] + dico_val_indiv['wav2vec_10k_transf4']),
                                         str(dico_val_indiv['distAssim'] + dico_val_indiv['wav2vec_english_transf4_dtw']),
                                         str(dico_val_indiv['distAssim'] + dico_val_indiv['wav2vec_french_transf4_dtw'])
                                         ]) + '\n')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='script to compute PAM-threshold values')
    parser.add_argument('file_input', metavar='f_in', type=str,
                        help='input file where you want to add the predictor values, must contain discrimination results, distAssim and wav2vec values')
    parser.add_argument('file_out', metavar='f_out', type=str,
                        help='file produced')

    args = parser.parse_args()

    file_in = args.file_input
    file_out = args.file_out
    add_combination(filename=file_in, filename_out=file_out)
