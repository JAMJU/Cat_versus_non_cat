# Cat_versus_non_cat

The individual triphones stimuli used during the discrimination and assimilation experiments are available on https://docs.cognitive-ml.fr/perceptimatic/Downloads/downloads.html#perceptimatic-dataset-files the name WorldVowels. We used this sound files to extract predictions from self-supervised models.

## Performing the experiments

### Assimilation task
The complete LMEDs code and experiment materials are available in the folder Assimilation_task

### Discrimination task
The complete LMEDs code and experiment materials are available in the folder Discrimination_task


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
We used the fairseq implementation of wav2vec, using its base version, see https://github.com/pytorch/fairseq/tree/main/examples/wav2vec for installation and training details. We used a subset of the English and French CommonVoice (converted to 16000hz using sox). The lists of the files used are available in the training_data folder.

The pretrained multilingual model we used is available in https://github.com/facebookresearch/voxpopuli/ (use the one trained on 23 languages).

#### Extracting representations
Follow the extraction instruction in https://github.com/JAMJU/Sel_supervised_models_perception_biases for the wav2vec model.

### DPGMM

We use the models and the extraction methods provided in https://github.com/geomphon/CogSci-2019-Unsupervised-speech-and-human-perception

### MFCCs

To compute mfccs and save their representations, we use the source files of the World Vowels dataset. You can use the following command line:

`python compute_mfccs.py $folder_wav $folder_out mfccs`


### Computing delta values

To compute delta values, go into computing_noncat_pred and do:
`python compute_distances_from_rep.py $model_name $path_to_representations $path_to_folder_to_put_results $triplet_list_file`

$triplet_list_file is in data/triplet_data.csv

Then you need to combine delta values with other predictors and human data. To do that,  go into computing_noncat_pred and do:
`python add_value_on_humans.py $folder_delta $discrimination_file.csv $file_produced.csv`  

## Combine category-driven and non categorical predictors
To combine wav2vec and distAssim, do:

`python combine_values.py $file_with_discrimination_results_and_predictors $file_out`

## Evaluate predictors

### Predict human discrimination behaviour

#### Log likelihood metric
`python bootstrap_probit_model.py $predictor_file $out_file $nb_it $french $english`

with `nb_it` the number of iteration of bootstrapping you want to do.
You need to precise in the file how many cpu are available for the computation. $out_file will contain the log likelihood results, one line per sampling


#### Spearman correlation metric

`python bootstrap_spearman_correlation.py $predictor_file $nb_it $outfile`

You need to precise the number of iteration needed by choosing `$nb_it`
You need to precise in the file how many cpu are available for the computation. $out_file will contain the log likelihood results, one line per sampling

### Native language effect

`python bootstrap_native_effect.py $predictor_file`
This only works with a complete file of predictors (containing the distassim, wav2vec delta values and dpgmm delta values)
