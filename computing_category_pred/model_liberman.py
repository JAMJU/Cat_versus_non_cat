#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created march 2021
    by Juliette MILLET
    script to compute liberman model predictions
"""
from get_vector_note_vote import get_v1_vectors
import numpy as np



def get_pr(rep_tgt, rep_oth, rep_x):
    """ rep_... are vector representation taken from assimilation pattern, each dim = one vowel in native language
    we return the probability of being right for this TGT/OTH/X triplet"""
    pr = 0

    for i in range(len(rep_tgt)):
        for j in range(len(rep_x)):
            if i == j:
                continue
            pr += rep_tgt[i]*rep_oth[j]*rep_x[i]

    return pr

def get_p50(rep_tgt, rep_oth, rep_x):
    """ rep_... are vector representation taken from assimilation pattern, each dim = one vowel in native language
        we return the probability of being at chance level for this TGT/OTH/X triplet"""
    p50 = 0

    for i in range(len(rep_tgt)):
        for j in range(len(rep_x)):
            p50 += rep_tgt[i]*rep_oth[i]*rep_x[j]

    for i in range(len(rep_tgt)):
        for j in range(len(rep_oth)):
            for k in range(len(rep_x)):
                if i != j and i!= k and j!=k:
                    p50 += rep_tgt[i]*rep_oth[j]*rep_x[k]

    return p50

def add_naive_version(assim_file, file_origin, file_out):
    res = get_v1_vectors(assim_file)

    f_in = open(file_origin, 'r')
    f_out = open(file_out, 'w')
    ind = f_in.readline().replace('\n', '')
    f_out.write(ind + ',liberman_naive\n')
    ind = ind.split(',')

    for line in f_in:
        new_line = line.replace('\n', '').split(',')
        lang_stimuli = new_line[ind.index('language_stimuli')]
        language_indiv = new_line[ind.index('language_indiv')]
        TGT = new_line[ind.index('TGT')]
        OTH = new_line[ind.index('OTH')]
        vector_TGT = np.asarray(res[language_indiv][lang_stimuli + ';' + TGT]['vote'])
        vector_OTH = np.asarray(res[language_indiv][lang_stimuli + ';' + OTH]['vote'])
        vector_X = np.asarray(res[language_indiv][lang_stimuli + ';' + TGT]['vote'])

        pr = get_pr(vector_TGT, vector_OTH, vector_X)
        p50 = get_p50(vector_TGT, vector_OTH, vector_X)

        pcorr = pr + 0.5*p50 # probability to be correct

        f_out.write(line.replace('\n', '') + ',' + str(pcorr) + '\n')
    f_in.close()
    f_out.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='script to compute max values')
    parser.add_argument('file_assimilation', metavar='f_as', type=str,
                        help='file where assimilation results are')
    parser.add_argument('file_input', metavar='f_in', type=str,
                        help='input file where you want to add the predictor values, must contain discrimination results')
    parser.add_argument('file_out', metavar='f_out', type=str,
                        help='file produced')

    args = parser.parse_args()

    file_assim = args.file_assimilation
    file_discrim = args.file_input

    add_naive_version(assim_file=file_assim, file_origin=file_discrim, file_out=args.file_out)















