#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created march 2021
    by Juliette MILLET
    script to compute max model predictions
"""

from get_vector_note_vote import get_v1_vectors
import numpy as np

def categorizedas(vote):
    cat = np.asarray(vote).argmax()
    return cat

def compute_max_result(vote1, vote2):
    cat1 = categorizedas(vote1)
    cat2 = categorizedas(vote2)
    if cat1 == cat2:
        return 0.
    else:
        return 1


def add_max_score(assim_file, file_origin, file_out):
    res = get_v1_vectors(assim_file)

    f_in = open(file_origin, 'r')
    f_out = open(file_out, 'w')
    ind = f_in.readline().replace('\n', '')
    f_out.write(ind + ',max_score\n')
    ind = ind.split(',')

    for line in f_in:
        new_line = line.replace('\n', '').split(',')
        lang_stimuli = new_line[ind.index('language_stimuli')]
        language_indiv = new_line[ind.index('language_indiv')]
        TGT = new_line[ind.index('TGT')]
        OTH = new_line[ind.index('OTH')]
        vote_TGT = np.asarray(res[language_indiv][lang_stimuli + ';' + TGT]['vote'])
        vote_OTH = np.asarray(res[language_indiv][lang_stimuli + ';' + OTH]['vote'])

        result = compute_max_result(vote1 = vote_TGT, vote2 = vote_OTH)
        f_out.write(','.join(new_line + [str(result)]) + '\n')




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

    add_max_score(assim_file=args.file_assimilation, file_origin=args.file_input,
                        file_out=args.file_out)



