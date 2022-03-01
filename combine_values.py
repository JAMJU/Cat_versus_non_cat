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

    df_english.loc['gamma_norm'] = 1. - df_english['gamma_norm']
    df_french.loc['gamma_norm'] = 1. - df_french['gamma_norm']
    df_english.loc['overlap_score_naive'] = - df_english['overlap_score_naive']
    df_french.loc['overlap_score_naive'] = - df_french['overlap_score_naive']

    dico_values = {'english': {}, 'french': {}}
    for name in ['overlap_score_naive', 'gamma_norm', 'wav2vec_10k_en_transf4','wav2vec_10k_fr_transf4','wav2vec_10k_transf4', 'wav2vec_french_transf4_dtw','wav2vec_english_transf4_dtw' ]:
        dico_values['english'][name] = {'std': df_english[name].std(),'mean': df_english[name].mean()}
        dico_values['french'][name] = {'std': df_french[name].std(), 'mean': df_french[name].mean()}

    f_in = open(filename, 'r')
    ind = f_in.readline().replace('\n', '')
    f_out = open(filename_out, 'w')
    f_out.write(ind.replace('overlap_score_naive', 'neg_overlap') + ',combi_ov_w2engfit,combi_ov_w2frfit,combi_ov_w2,combi_gam_w2engfit,combi_gam_w2frfit,combi_gam_w2,combi_ov_w2engnon,combi_ov_w2frnon,combi_gam_w2engnon,combi_gam_w2frnon\n')
    ind = ind.split(',')

    for line in f_in:
        new_line  = line.replace('\n', '').split(',')
        # we rearrange that
        new_line[ind.index('gamma_norm')] = str(1. - float(new_line[ind.index('gamma_norm')]))
        new_line[ind.index('overlap_score_naive')] = str( - float(new_line[ind.index('overlap_score_naive')]))
        lang = new_line[ind.index('language_indiv')]
        values = dico_values[lang]
        dico_val_indiv = {}
        for name in ['overlap_score_naive', 'gamma_norm', 'wav2vec_10k_en_transf4','wav2vec_10k_fr_transf4','wav2vec_10k_transf4' , 'wav2vec_french_transf4_dtw','wav2vec_english_transf4_dtw']:
            dico_val_indiv[name] = (float(new_line[ind.index(name)]) - values[name]['mean'])/values[name]['std']

        f_out.write(','.join(new_line + [str( dico_val_indiv['overlap_score_naive'] + dico_val_indiv['wav2vec_10k_en_transf4']),
                                         str( dico_val_indiv['overlap_score_naive'] + dico_val_indiv['wav2vec_10k_fr_transf4']),
                                         str( dico_val_indiv['overlap_score_naive'] + dico_val_indiv['wav2vec_10k_transf4']),
                                         str(dico_val_indiv['gamma_norm'] + dico_val_indiv['wav2vec_10k_en_transf4']),
                                         str(dico_val_indiv['gamma_norm'] + dico_val_indiv['wav2vec_10k_fr_transf4']),
                                         str(dico_val_indiv['gamma_norm'] + dico_val_indiv['wav2vec_10k_transf4']),
                                         str(dico_val_indiv['overlap_score_naive'] + dico_val_indiv[
                                             'wav2vec_english_transf4_dtw']),
                                         str(dico_val_indiv['overlap_score_naive'] + dico_val_indiv[
                                             'wav2vec_french_transf4_dtw']),
                                         str(dico_val_indiv['gamma_norm'] + dico_val_indiv['wav2vec_english_transf4_dtw']),
                                         str(dico_val_indiv['gamma_norm'] + dico_val_indiv['wav2vec_french_transf4_dtw'])
                                         ]) + '\n')

if __name__ == '__main__':
    file_in = 'final_with_unfit_w2v.csv'
    file_out = 'all_values.csv'
    add_combination(filename=file_in, filename_out=file_out)
