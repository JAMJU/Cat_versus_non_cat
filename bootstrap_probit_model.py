#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created march 2021
    by Juliette MILLET
    script to test if gamma value predicts discrimination well
"""
import os
nb = "30"

from multiprocessing import Pool
import pandas as pd
from statsmodels.formula.api import probit
from sampling import get_dico_corres_file, sample_lines


def model_probit_binarized(data_file,  model, lines_sampled): # for the model, you have to add the +
    #print(lines_sampled)
    data_ = pd.read_csv(data_file, sep=',', encoding='utf-8')
    #data_['inverted_gamma'] = 1./data_['gamma_value']

    data_['binarized_answer'] = (data_['binarized_answer'] + 1.) / 2  # we transform -1 1 into 0 1
    data_['english'] = 1 - data_['language_indiv_code']
    data_['french'] = data_['language_indiv_code']


    data = data_.iloc[lines_sampled]
    # we normalize data
    for val in ['nb_stimuli'] + [mod.replace(' ', '')  for mod in model.split('+')]:
        data[val] = (data[val] -data[val].mean())/data[val].std()
    model_probit = probit("binarized_answer ~ TGT_first_code + C(individual) + nb_stimuli  + " + model, data) #
    result_probit = model_probit.fit()

    return model_probit.loglike(result_probit.params)

def func_to_parallel(args):
    dico_lines = args[0]
    list_names= args[1]
    it = args[2]
    file_humans = args[3]
    list_sampled = sample_lines(dico_lines)
    list_log = [str(it)]
    for mod in list_names:
        print(mod)
        log= model_probit_binarized(data_file=file_humans, model=mod,
                                                 lines_sampled=list_sampled)
        list_log.append(str(log))
    return list_log


def iteration_model(filename, nb_it, outfile, french = True, english = True):
    dico_lines = get_dico_corres_file(filename, french=french, english = english) # the selection of language is done here

    f_names = open(filename, 'r')
    line_names = f_names.readline().replace('\n', '').split(',')
    list_names = []
    start = False
    for nam in line_names:
        if start:
            list_names.append(nam)
        elif not start and nam == "language_stimuli_code":  # end of info start of models
            start = True

    f_names.close()
    print(list_names)
    out = open(outfile, 'a')
    out.write('nb,' + ','.join(list_names))
    out.write('\n')

    out.close()



    print('Beginning')
    div = int(nb_it / int(nb))

    for k in range(div):
        with Pool(int(nb)) as p:
            lines = p.map(func_to_parallel,
                          [[dico_lines, list_names,  k * int(nb) + i, filename] for i in
                           range(int(nb))])
            for li in lines:
                out = open(outfile , 'a')
                out.write(','.join(li))
                out.write('\n')
                out.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='script to analyze output from humans vs model\'s outputs and sample the results using bootstrap')
    parser.add_argument('file_humans', metavar='f_do', type=str,
                        help='file with outputs humans t give')
    parser.add_argument('outfile', metavar='f_do', type=str,
                        help='file with log likelihood answers')
    parser.add_argument('nb_it', metavar='f_do', type=int,
                        help='nb of sampling')
    parser.add_argument('french', metavar='f_do', type=str,
                        help='if french participants used')
    parser.add_argument('english', metavar='f_do', type=str,
                        help='if english participants used')

    args = parser.parse_args()

    fr = True if args.french == 'True' else False
    en = True if args.english == 'True' else False
    print('french', fr,'english', en)

    iteration_model(filename=args.file_humans, nb_it=args.nb_it, outfile=args.outfile, french=fr, english=en)
