#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created march 2021
    by Juliette MILLET
    functions for bottstrap computations
"""
import random as rd

def get_dico_corres_file(data_file, french = True, english = True):
    dico ={}
    f = open(data_file, 'r')
    ind = f.readline().replace('\n', '').split(',')
    count = 0
    for line in f:

        newline = line.replace('\n', '').split(',')
        language_indiv = newline[ind.index('language_indiv')]
        #print(language_indiv)
        if (not french and language_indiv == 'french'):
            #print('out')
            count += 1
            continue
        if (not english and language_indiv == 'english'):
            count += 1
            continue
        if newline[ind.index('filename')] in dico:
            dico[newline[ind.index('filename')]].append(count)
        else:
            dico[newline[ind.index('filename')]] = [count]
        count += 1
    f.close()
    return dico


def sample_lines(dico_line_files):
    # we sample three results per filename
    list_lines = []
    for filename in dico_line_files:
        list_lines = list_lines + [dico_line_files[filename][rd.randrange(0,stop= len(dico_line_files[filename]))],
                                   dico_line_files[filename][rd.randrange(0, stop=len(dico_line_files[filename]))],
                                   dico_line_files[filename][rd.randrange(0, stop=len(dico_line_files[filename]))],
                                   dico_line_files[filename][rd.randrange(0, stop=len(dico_line_files[filename]))],
                                   dico_line_files[filename][rd.randrange(0, stop=len(dico_line_files[filename]))]]
    return list_lines