#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created march 2021
    by Juliette MILLET
    script to compute liberman model predictions
"""

from get_vector_note_vote import get_v1_vectors
import numpy as np

def is_categorized(vote, note, threshold):
    for i in range(len(vote)):
        if vote[i] > threshold:
            return True, i, note[i]
    return False, None, None



def compute_threshold_result(vote1, note1, vote2, note2, threshold, threshold_sim, threshold_uncat_uncat, is_native):

    if is_native:
        return 1.

    is_cat1, res1, not1 = is_categorized(vote1, note1, threshold)
    is_cat2, res2, not2 = is_categorized(vote2, note2, threshold)

    # two cat assimilation
    if is_cat1 and is_cat2 and res1!= res2:
        return 1. # perfect score

    # single cat assimilation
    if is_cat1 and is_cat2 and res1 == res2:
        # same degree of assim
        if abs(not1 - not2) < threshold_sim:
            return 0.
        else:
            return 1.

    # categorized/ uncategorized case
    if (is_cat1 and not is_cat2) or (is_cat2 and not is_cat1):
        return 1.

    # uncategorized/ uncategorized case
    if not is_cat1 and not is_cat2:
        # in this case we need to compare the assim patterns
        # we take all the phone that are above threshold
        pat_assim1 = []
        pat_assim2 = []
        for i in range(len(vote1)):
            if vote1[i] > threshold_uncat_uncat:
                pat_assim1.append(i)
            if vote2[i] > threshold_uncat_uncat:
                pat_assim2.append(i)
        # if the two patterns are different -> ok
        if len(pat_assim2) != len(pat_assim1):
            return 1.
        if pat_assim2 != pat_assim1:
            return 1.
        else:
            return 0.

def add_threshold_score(assim_file, file_origin, file_out, threshold, threshold_sim, threshold_uncat_uncat):
    res = get_v1_vectors(assim_file)

    f_in = open(file_origin, 'r')
    f_out = open(file_out, 'w')
    ind = f_in.readline().replace('\n', '')
    f_out.write(ind + ',threshold_score\n')
    ind = ind.split(',')

    for line in f_in:
        new_line = line.replace('\n', '').split(',')
        lang_stimuli = new_line[ind.index('language_stimuli')]
        language_indiv = new_line[ind.index('language_indiv')]
        is_native = False
        if (lang_stimuli == "FR" and language_indiv == "french") or (lang_stimuli == 'EN' and language_indiv == "english"):
            is_native = True
        TGT = new_line[ind.index('TGT')]
        OTH = new_line[ind.index('OTH')]
        vote_TGT = np.asarray(res[language_indiv][lang_stimuli + ';' + TGT]['vote'])
        vote_OTH = np.asarray(res[language_indiv][lang_stimuli + ';' + OTH]['vote'])
        note_TGT = np.asarray(res[language_indiv][lang_stimuli + ';' + TGT]['note'])
        note_OTH = np.asarray(res[language_indiv][lang_stimuli + ';' + OTH]['note'])

        result = compute_threshold_result(vote1 = vote_TGT, note1 = note_TGT, vote2 = vote_OTH, note2 = note_OTH, threshold=threshold,
                                 threshold_sim=threshold_sim, threshold_uncat_uncat=threshold_uncat_uncat, is_native=is_native)
        f_out.write(','.join(new_line + [str(result)]) + '\n')




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

    thres = 0.70
    thresh_sim = 3
    thresh_uncat_uncat = 0.07

    data = args.file_input
    add_threshold_score(assim_file=args.file_assimilation, file_origin=data,
                        file_out=args.file_out, threshold=thres, threshold_sim=thresh_sim,
                        threshold_uncat_uncat=thresh_uncat_uncat)



