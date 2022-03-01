#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created march 2021
    by Juliette MILLET
    script to compute distance from representation
"""
import os
nb = "10"
os.environ["OMP_NUM_THREADS"] = nb
os.environ["OPENBLAS_NUM_THREADS"] = nb
os.environ["MKL_NUM_THREADS"] = nb
os.environ["VECLIB_MAXIMUM_THREADS"] = nb
os.environ["NUMEXPR_NUM_THREADS"] = nb
from dtw_experiment import compute_dtw
from get_representations import get_triphone_mfccs, get_triphone_wav2vec, get_triphone_dpgmm


def get_distances_and_delta(triphone_TGT, triphone_OTH, triphone_X, get_func, distance):
    TGT = get_func(triphone_TGT)
    OTH = get_func(triphone_OTH)
    X = get_func(triphone_X)

    TGTX = compute_dtw(TGT,X, distance, norm_div=True)
    OTHX = compute_dtw(OTH,X, distance, norm_div=True)

    delta = OTHX - TGTX

    return TGTX, OTHX, delta


def get_distance_for_triplets(filename_triplet_list, file_out, get_func, distance):
    f = open(filename_triplet_list, 'r')
    ind = f.readline().replace('\n', '').split(',')
    print(ind)
    f_out = open(file_out, 'w')
    f_out.write(','.join(ind + ['TGTX', 'OTHX', 'delta', 'decision\n']))
    kee_dis = {}
    count = 0
    for line in f:
        if count % 100 == 0:
            print(count)
        count += 1
        new_line = line.replace('\n', '').split(',')
        OTH_item = new_line[ind.index('OTH_item')].replace('.wav', '')
        TGT_item = new_line[ind.index('TGT_item')].replace('.wav', '')
        X_item = new_line[ind.index('X_item')].replace('.wav', '')
        if TGT_item + ',' + OTH_item + ',' + X_item in kee_dis.keys():
            key = TGT_item + ',' + OTH_item + ',' + X_item
            TGTX = kee_dis[key][0]
            OTHX = kee_dis[key][1]
            delta = kee_dis[key][2]
        else:
            TGTX, OTHX, delta = get_distances_and_delta(triphone_TGT=TGT_item, triphone_OTH=OTH_item, triphone_X=X_item, get_func=get_func, distance = distance)
            kee_dis[TGT_item + ',' + OTH_item + ',' + X_item] = [TGTX, OTHX, delta]
        f_out.write(','.join(new_line + [str(TGTX), str(OTHX), str(delta), '1\n' if delta> 0. else '0\n']))

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='script to compute distances')
    parser.add_argument('model_name', metavar='f_do', type=str,
                        help='model')
    parser.add_argument('path_to_data', metavar='f_do', type=str,
                        help='path to representations')
    parser.add_argument('path_folder_out', metavar='f_do', type=str,
                        help='path where to put file produced')
    parser.add_argument('triplet_list_file', metavar='f_do', type=str,
                        help='files with a list of triplet')
    args = parser.parse_args()

    triplet_file = args.triplet_list_file





    mfccs = lambda x: get_triphone_mfccs(folder_data=args.path_to_data, triphone_name=x)

    dpgmm = lambda x: get_triphone_dpgmm(folder_data=args.path_to_data, triphone_name=x)

    wav2vec = lambda x: get_triphone_wav2vec(folder_data=args.path_to_data, triphone_name=x)



    if args.model == 'mfccs':
        func = mfccs
    elif 'wav2vec' in args.model:
        func = wav2vec
    elif 'dpgmm' in args.model:
        func = dpgmm

    else:
        print('Error the model does not exist')


    get_distance_for_triplets(filename_triplet_list=triplet_file, file_out=os.path.join(args.path_file_out, args.model_name + '_triplet.csv'),
                              get_func=func, distance='kl' if 'dpgmm' in args.model else 'cosine')



