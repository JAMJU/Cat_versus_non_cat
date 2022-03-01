#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created march 2021
    by Juliette MILLET
    script to compute negoverlap values predictions
"""
from get_vector_note_vote import get_v1_vectors
import numpy as np


def get_overlap_score(vector_1,vector_2):
    overlap = 0
    for dim in range(len(vector_1)):
        overlap += min(vector_1[dim], vector_2[dim])
    return overlap


def add_naive(assim_file, file_origin, file_out,  name ='overlap_score_naive'):
    res = get_v1_vectors(assim_file)

    f_in = open(file_origin, 'r')
    f_out = open(file_out, 'w')
    ind = f_in.readline().replace('\n', '')
    f_out.write(ind + ',' + name + '\n')
    ind = ind.split(',')
    #print(ind)
    for line in f_in:
        new_line = line.replace('\n', '').split(',')
        #print(new_line)
        lang_stimuli = new_line[ind.index('language_stimuli')]
        language_indiv = new_line[ind.index('language_indiv')]
        TGT = new_line[ind.index('TGT')]
        OTH = new_line[ind.index('OTH')]
        vector_TGT = np.asarray(res[language_indiv][lang_stimuli + ';' + TGT]['vote'])
        vector_OTH = np.asarray(res[language_indiv][lang_stimuli + ';' + OTH]['vote'])

        over_score = get_overlap_score(vector_OTH, vector_TGT)
        neg_over = -over_score
        f_out.write(line.replace('\n', '') + ',' + str(neg_over) + '\n') # we load the negative version of that
    f_in.close()
    f_out.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='script to compute neg overlap values')
    parser.add_argument('file_assimilation', metavar='f_as', type=str,
                        help='file where assimilation results are')
    parser.add_argument('file_input', metavar='f_in', type=str,
                        help='input file where you want to add the predictor values, must contain discrimination results')
    parser.add_argument('file_out', metavar='f_out', type=str,
                        help='file produced')

    args = parser.parse_args()
    add_naive(assim_file=args.file_assimilation, file_origin=args.file_input, file_out=args.file_out, name = 'neg_overlap')
