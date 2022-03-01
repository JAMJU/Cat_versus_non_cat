# Cat_versus_non_cat

The individual triphones stimuli used during the discrimination and assimilation experiments are available on https://docs.cognitive-ml.fr/perceptimatic/Downloads/downloads.html#perceptimatic-dataset-files the name WorldVowels. We used this sound files to extract predictions from self-supervised models.

## Performing the experiments

### Assimilation task

### Discrimination task

## Compute category-driven predictors
For all category driven predictors, you need to use the results for the assimilation task. They are available in the file data/all_assimilation.csv. We present here how to compute the different category-driven predictors we use in our paper, and how to add them to the discrimination result file that you can file in data/all_discrimination.csv

### DistAssim

Go into computing_category_pred folder and do:

`python model_distassim.py $path/to/assimilation_file $path/to/discrimination_file $path/to/file_produced`

### PAM-thresold

Go into computing_category_pred folder and do:

`python model_threshold.py $path/to/assimilation_file $path/to/discrimination_file $path/to/file_produced`

### Max-predictor

Go into computing_category_pred folder and do:

`python model_max.py $path/to/assimilation_file $path/to/discrimination_file $path/to/file_produced`

### Liberman model

Go into computing_category_pred folder and do:

`python model_liberman.py $path/to/assimilation_file $path/to/discrimination_file $path/to/file_produced`

### Neg-overlap score

Go into computing_category_pred folder and do:

`python model_negoverlap.py $path/to/assimilation_file $path/to/discrimination_file $path/to/file_produced`

## Extract non categorical predictors

### Wav2vec 2.0

#### Training models

#### Extracting representations

### DPGMM

We use the models and the extraction methods provided in https://github.com/geomphon/CogSci-2019-Unsupervised-speech-and-human-perception


### Computing delta values

## Combine category-driven and non categorical predictors

## Evaluate predictors

### Predict human discrimination behaviour

#### Log likelihood metric

#### Spearman correlation metric

### Native language effect


