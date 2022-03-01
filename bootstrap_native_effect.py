#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created march 2021
    by Juliette MILLET
    evaluate model on native effect
"""
import pandas as pd
from scipy.stats import pearsonr
import numpy as np
from multiprocessing import Pool
import plotly.graph_objects as go
from sampling import get_dico_corres_file, sample_lines
nb = "30"



def commpute_differences_faster(filename_, levels, values_comparison_french, values_comparison_english, sampled_lines, it):
    """ Compute diff french minus english"""
    data = pd.read_csv(filename_, sep=',', encoding='utf-8')

    all_val = []

    data = data.iloc[sampled_lines]

    data_fr = data[data['language_indiv'] == 'french'].copy()
    data_en = data[data['language_indiv'] == 'english'].copy()

    # We normalize english and french side for the model so they are comparable
    for i in range(len(values_comparison_english)):
        data_fr[values_comparison_french[i]] = data_fr[values_comparison_french[i]]  / data_fr[values_comparison_french[i]].std()
        data_en[values_comparison_english[i]] = data_en[values_comparison_english[i]] / data_en[values_comparison_english[i]].std()

    data_en['triplet_compo'] =data_en['TGT'] + ';' + data_en['OTH'] + ';' + data_en['prev_phone'] + ';' + data_en[
        'next_phone'] + ';' + data_en['language_stimuli']
    data_fr['triplet_compo'] = data_fr['TGT'] + ';' + data_fr['OTH'] + ';' + data_fr['prev_phone'] + ';' + data_fr[
        'next_phone'] + ';' + data_fr['language_stimuli']
    data_en['contrast'] = data_en['TGT'] + ';' + data_en['OTH'] + ';' + data_en['language_stimuli']
    data_fr['contrast'] = data_fr['TGT'] + ';' + data_fr['OTH'] + ';' + data_fr['language_stimuli']

    data_fr.to_csv('temp_fr'+ str(it)+'.csv')
    data_en.to_csv('temp_en'+ str(it) +'.csv')
    data_fr = ''
    data_en = ''
    data_fr_file = {}
    data_en_file = {}
    data_fr_triplet = {}
    data_en_triplet = {}
    data_fr_contrast = {}
    data_en_contrast = {}

    for k in values_comparison_french  + ['correct_answer']:
        data_fr_file[k] = {}
        data_fr_triplet[k] = {}
        data_fr_contrast[k] = {}
    for k in values_comparison_english  + ['correct_answer']:
        data_en_file[k] = {}
        data_en_triplet[k] = {}
        data_en_contrast[k] = {}

    f = open('temp_fr'+ str(it)+'.csv', 'r')
    ind= f.readline().replace('\n', '').split(',')

    for line in f:
        new_line = line.replace('\n', '').split(',')
        file = new_line[ind.index('filename')].replace('"', "")
        triplet_compo =new_line[ind.index('triplet_compo')].replace('"', "")
        contrast = new_line[ind.index('contrast')].replace('"', "")
        for k in values_comparison_french + ['correct_answer']:
            delta = float(new_line[ind.index(k)])
            data_fr_file[k][file] = data_fr_file[k].get(file, []) + [delta]
            data_fr_triplet[k][triplet_compo] = data_fr_triplet[k].get(triplet_compo, []) + [delta]
            data_fr_contrast[k][contrast] = data_fr_contrast[k].get(contrast, []) + [delta]
    f.close()
    #print(data_fr_contrast["correct_answer"].keys())
    f = open('temp_en'+ str(it) +'.csv', 'r')
    ind = f.readline().replace('\n', '').split(',')

    for line in f:
        new_line = line.replace('\n', '').split(',')
        file = new_line[ind.index('filename')].replace('"', "")
        triplet_compo = new_line[ind.index('triplet_compo')].replace('"', "")
        contrast = new_line[ind.index('contrast')].replace('"', "")
        for k in values_comparison_english + ['correct_answer']:
            delta = float(new_line[ind.index(k)])
            data_en_file[k][file] = data_en_file[k].get(file, []) + [delta]
            data_en_triplet[k][triplet_compo] = data_en_triplet[k].get(triplet_compo, []) + [delta]
            data_en_contrast[k][contrast] = data_en_contrast[k].get(contrast, []) + [delta]
    f.close()

    os.remove('temp_fr'+ str(it)+'.csv')
    os.remove('temp_en'+ str(it)+'.csv')
    #print(data_fr_contrast)

    for k in values_comparison_english + ['correct_answer']:
        for file in data_en_file[k]:
            data_en_file[k][file] = np.asarray(data_en_file[k][file]).mean()
        for triplet in data_en_triplet[k]:
            data_en_triplet[k][triplet] = np.asarray(data_en_triplet[k][triplet]).mean()
        for cont in data_en_contrast[k]:
            data_en_contrast[k][cont] = np.asarray(data_en_contrast[k][cont]).mean()
    for k in values_comparison_french + ['correct_answer']:
        for file in data_fr_file[k]:
            data_fr_file[k][file] = np.asarray(data_fr_file[k][file]).mean()
        for triplet in data_fr_triplet[k]:
            data_fr_triplet[k][triplet] = np.asarray(data_fr_triplet[k][triplet]).mean()
        for cont in data_fr_contrast[k]:
            data_fr_contrast[k][cont] = np.asarray(data_fr_contrast[k][cont]).mean()



    if  'file' in levels:
        triplet_list = list(data_en_file[values_comparison_english[0]].keys())
        diff_humans = []
        diff_models = {}
        for i in range(len(values_comparison_english)):
            diff_models[values_comparison_english[i]] = []
        triplet_done = []
        for trip in triplet_list:
            if trip in triplet_done:
                continue
            other = trip
            if '_0' in trip:
                other.replace('_0', '_1')
            if '_1' in trip:
                other.replace('_1', '_0')
            triplet_done.append(trip)
            triplet_done.append(other)
            # we average OTH-TGT and TGT-OTH
            val_fr_human = (data_fr_file['correct_answer'][trip] + data_fr_file['correct_answer'][other])/2.
            val_en_human = (data_en_file['correct_answer'][trip] + data_en_file['correct_answer'][other])/2.
            # it is already averaged for the model

            diff_humans.append(val_fr_human - val_en_human)

            for i in range(len(values_comparison_english)):
                val_fr_model =data_fr_file[values_comparison_french[i]][trip]
                val_en_model = data_en_file[values_comparison_english[i]][trip]
                diff_models[values_comparison_english[i]].append(val_fr_model - val_en_model)
        all_val +=[ np.asarray(diff_humans)]
        for i in range(len(values_comparison_english)):
            all_val += [diff_models[values_comparison_english[i]]]


    if 'triplet' in levels:

        triplet_list = list(data_en_triplet[values_comparison_english[0]].keys())
        diff_humans = []
        diff_models = {}
        for i in range(len(values_comparison_english)):
            diff_models[values_comparison_english[i]] = []
        triplet_done = []
        for trip in triplet_list:
            if trip in triplet_done:
                continue
            # we average on TGT-OTH OTH-TGT
            other = trip.split(';')
            #print(other)
            other = ';'.join([other[1], other[0], other[2], other[3], other[4]])
            triplet_done.append(other)
            triplet_done.append(trip)

            val_fr_human = (data_fr_triplet['correct_answer'][trip] + data_fr_triplet['correct_answer'][other]) / 2.
            val_en_human = (data_en_triplet['correct_answer'][trip] + data_en_triplet['correct_answer'][other]) / 2.
            diff_humans.append(val_fr_human - val_en_human)
            for i in range(len(values_comparison_english)):
                val_fr_model = (data_fr_triplet[values_comparison_french[i]][trip] +
                                data_fr_triplet[values_comparison_french[i]][other])/2.
                val_en_model = (data_en_triplet[values_comparison_english[i]][trip] +
                                data_en_triplet[values_comparison_english[i]][other])/2.
                diff_models[values_comparison_english[i]].append(val_fr_model - val_en_model)
        all_val += [np.asarray(diff_humans)]
        for i in range(len(values_comparison_english)):
            all_val += [diff_models[values_comparison_english[i]]]




    if  'contrast' in levels:

        triplet_list =  list(data_en_contrast[values_comparison_english[0]].keys())
        diff_humans = []
        diff_models = {}
        for i in range(len(values_comparison_english)):
            diff_models[values_comparison_english[i]] = []
        triplet_done = []
        for trip in triplet_list:
            if trip in triplet_done:
                continue
            # we average on TGT-OTH OTH-TGT
            other = trip.split(';')
            other = ';'.join([other[1], other[0], other[2]])
            triplet_done.append(other)
            triplet_done.append(trip)

            val_fr_human = (data_fr_contrast['correct_answer'][trip] + data_fr_contrast['correct_answer'][other])  / 2.
            val_en_human = (data_en_contrast['correct_answer'][trip] + data_en_contrast['correct_answer'][other])  / 2.
            diff_humans.append(val_fr_human - val_en_human)
            for i in range(len(values_comparison_english)):
                val_fr_model = (data_fr_contrast[values_comparison_french[i]][trip] +
                                data_fr_contrast[values_comparison_french[i]][other]) / 2.
                val_en_model = (data_en_contrast[values_comparison_english[i]][trip] +
                                data_en_contrast[values_comparison_english[i]][other]) / 2.

                diff_models[values_comparison_english[i]].append(val_fr_model - val_en_model)

        all_val += [np.asarray(diff_humans)]
        for i in range(len(values_comparison_english)):
            all_val += [diff_models[values_comparison_english[i]]]
    return all_val

def compute_correlation(diff_models, diff_humans):
    #print(diff_models)
    #print(diff_humans)
    return pearsonr(diff_models, diff_humans)

def function_to_parallel(args):

    it = args[0]
    outfile_file = args[1]
    outfile_triplet = args[2]
    outfile_contrast = args[3]
    file_data = args[4]
    models_couples = args[5]
    models = args[6]
    dico_french = args[7]
    dico_english = args[8]


    english_lines = sample_lines(dico_english)
    french_lines = sample_lines(dico_french)
    lines_sampled = english_lines + french_lines
    diffs = commpute_differences_faster(filename_=file_data, levels=['file', 'triplet', 'contrast'],
                                        values_comparison_english=[models_couples[modi]['english'] for modi in models],
                                        values_comparison_french=[models_couples[modi]['french'] for modi in models],
                                        sampled_lines=lines_sampled, it = it)
    line_file = []
    line_triplet = []
    line_contrast = []
    line_file.append(str(it))
    line_triplet.append(str(it))
    line_contrast.append(str(it))
    # first file
    count = 0
    diff_humans = diffs[0]
    count += 1
    #out = open(outfile_file, 'a')
    for i in range(len((models))):
        r, p = compute_correlation(diff_models=diffs[count], diff_humans=diff_humans)
        count += 1
        #out.write(',' + str(r) + ',' + str(p))
        line_file.append(str(r) )
        line_file.append(str(p))
    #out.close()

    # then triplet
    diff_humans = diffs[count]
    count += 1
    #out = open(outfile_triplet, 'a')
    for i in range(len((models))):
        r, p = compute_correlation(diff_models=diffs[count], diff_humans=diff_humans)
        count += 1
        line_triplet.append(str(r))
        line_triplet.append(str(p))
        #out.write(',' + str(r) + ',' + str(p))

    #out.close()

    # then contrast
    diff_humans = diffs[count]
    count += 1
    #out = open(outfile_contrast, 'a')
    for i in range(len((models))):
        r, p = compute_correlation(diff_models=diffs[count], diff_humans=diff_humans)
        line_contrast.append(str(r))
        line_contrast.append(str(p))
        count += 1
        #out.write(',' + str(r) + ',' + str(p))
    #out.close()
    return line_file, line_triplet, line_contrast

def iterations(models_couples, file_data, outfile_file, outfile_triplet, outfile_contrast, nb_it):
    dico_english = get_dico_corres_file(data_file=file_data, french = False, english = True)
    dico_french = get_dico_corres_file(data_file=file_data, french = True, english = False)

    models = list(models_couples.keys())
    for fili in [outfile_file, outfile_triplet, outfile_contrast]:
        out = open(fili, 'a')
        out.write('nb')
        for mod in models:
            out.write(',' + mod + ',' + mod+ '_p_val')
        out.write('\n')
        out.close()

    div = int(nb_it/int(nb))

    for k in range(div):
        with Pool(int(nb)) as p:
            lines = p.map(function_to_parallel, [[k*int(nb) + i, outfile_file, outfile_triplet,
                                          outfile_contrast, file_data, models_couples, models,
                                          dico_french, dico_english] for i in range(int(nb))])
            for li in lines:
                file, trip, cont = li
                out = open(outfile_file, 'a')
                out.write(','.join(file))
                out.close()
                out = open(outfile_triplet, 'a')
                out.write(','.join(trip))
                out.close()
                out = open(outfile_contrast, 'a')
                out.write(','.join(cont))
                out.close()

                for fili in [outfile_file, outfile_triplet, outfile_contrast]:
                    out = open(fili, 'a')
                    out.write('\n')
                    out.close()






if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='script to analyze native language effect using bootstraping')
    parser.add_argument('file_in', metavar='f_do', type=str,
                        help='folder where outputs are')

    args = parser.parse_args()


    dico_models = {'wav2vec':{'english':'wav2vec_english_transf4_dtw', 'french':'wav2vec_french_transf4_dtw'},
                   'distAssim':{'english':'distAssim', 'french':'distAssim'},
                   'dpgmm':{'english':'dpgmm_english', 'french':'dpgmm_french'}}
    iterations(models_couples=dico_models, file_data=args.file_in, outfile_file="all_native_effect_file.csv",
               outfile_contrast="all_native_effect_contrast.csv", outfile_triplet="all_native_effect_triplet.csv", nb_it=10000)




