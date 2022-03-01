#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created march 2021
    by Juliette MILLET
    script to compute distassim predictions
"""

import numpy as np
from numpy.linalg import norm

from get_vector_note_vote import get_v1_vectors

def get_norm_gamma_value(dico_assim, language_indiv, TGT, OTH, lang_stimuli):
    vector_TGT = np.asarray(dico_assim[language_indiv][lang_stimuli + ';' + TGT]['product'])
    vector_OTH = np.asarray(dico_assim[language_indiv][lang_stimuli + ';' + OTH]['product'])
    gamma = vector_TGT.dot(vector_OTH) / (norm(vector_TGT, 2)* norm(vector_OTH,2))
    return gamma



def compute_gamm_value(file_discrimination, dico_assim, file_output):
    f = open(file_output, 'w')
    f_in = open(file_discrimination, 'r')
    ind = f_in.readline()
    f.write(ind.replace('\n', '') + ',distAssim' + '\n')
    ind = ind.replace('\n', '').split(',')

    for line in f_in:
        new_line = line.replace('\n', '').split(',')
        language_indiv = new_line[ind.index('language_indiv')]
        lang_stimuli = new_line[ind.index('language_stimuli')]
        TGT = new_line[ind.index('TGT')]
        OTH = new_line[ind.index('OTH')]
        gamma_norm = get_norm_gamma_value(dico_assim=dico_assim, language_indiv=language_indiv,
                                          TGT = TGT, OTH = OTH, lang_stimuli=lang_stimuli)
        #if language_indiv == 'french':
        f.write(','.join(new_line + [str(gamma_norm)]) + '\n')
    f.close()




if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='script to compute PAM-threshold values')
    parser.add_argument('file_assimilation', metavar='f_as', type=str,
                        help='file where assimilation results are')
    parser.add_argument('file_input', metavar='f_in', type=str,
                        help='input file where you want to add the predictor values, must contain discrimination results')
    parser.add_argument('file_out', metavar='f_out', type=str,
                        help='file produced')

    args = parser.parse_args()
    res = get_v1_vectors(args.file_assimilation)

    compute_gamm_value(file_discrimination=args.file_input, dico_assim=res, file_output=args.file_out)


