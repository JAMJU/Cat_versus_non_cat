#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created march 2021
    by Juliette MILLET
    script to compute vote vector and note vector for each couple (language_stimuli, vowel) for one language_indiv
    from assimilation experiment
"""

phone_english = ['ɪ', 'i', 'ʊ', 'u', 'oʊ', 'eɪ', 'ɛ', 'ʌ', 'æ', 'ɑ']
phone_french = ['i' ,'y' ,'u' ,'e','ɛ', 'ø', 'œ', 'a', 'o', 'ɔ', 'ɛ̃', 'ɔ̃', 'ɑ̃']


def get_v1_vectors(file_results_assimilation):
    """
    Compute the simple version of vector note and vote, just sum along all results for each (lang_stim, vowel, lang_indiv)
    :param file_results_assimilation: list of results for assimilation in tidy
    :return:
    """
    f = open(file_results_assimilation, 'r')
    ind = f.readline().split(',')
    dico_all = {'english':{}, 'french':{}}
    for line in f:
        new_line = line.replace('\n', '').split(',')
        language_indiv = new_line[ind.index('language_indiv')]
        lang_stimuli = new_line[ind.index('language_stimuli')]
        vowel_target = new_line[ind.index('#phone')]
        vowel_chosen = int(new_line[ind.index('code_assim')])
        grade = int(new_line[ind.index('grade')])

        class_stimuli = lang_stimuli + ';' + vowel_target

        if class_stimuli not in dico_all[language_indiv]:
            list_lang_phone = phone_french if language_indiv == 'french' else phone_english
            dico_all[language_indiv][class_stimuli] = {'note_all':[0 for a in list_lang_phone], 'vote_all':[0 for a in list_lang_phone]}

        dico_all[language_indiv][class_stimuli]['note_all'][vowel_chosen] += grade + 1
        dico_all[language_indiv][class_stimuli]['vote_all'][vowel_chosen] += 1

    results = {'english': {}, 'french':{}}
    for lang in ['english', 'french']:
        for class_stim in dico_all[lang]:
            summ = sum(dico_all[lang][class_stim]['vote_all'])
            results[lang][class_stim] = {'note':[n/max(1,v) for n,v in zip(dico_all[lang][class_stim]['note_all'], dico_all[lang][class_stim]['vote_all'])],
                                      'vote': [v/summ for v in dico_all[lang][class_stim]['vote_all']],
                                      'nb_votes':summ}
            results[lang][class_stim]['product'] = [n*v for n,v in zip(results[lang][class_stim]['note'], results[lang][class_stim]['vote'])]

    return results






