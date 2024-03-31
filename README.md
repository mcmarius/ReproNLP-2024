# ReproNLP-2024

This repository provides all the necessary code and data for the reproduction of our experiments.

There is only one script for code which contains a CLI interface.

All data files reside in the `data` directory.

Next, we show how to process the files. Use `python main.py -h` for help with the script.

### 1. Write files for labellers

```sh
python main.py write-files-for-labellers
```

### 2. Move (or add) newly labelled files to data/ directory

The files should be named `received_stories_{labeller_number}.xlsx`.

### 3. Remove any personal data from the received files

```sh
python main.py anonymize-labellers-files
```

### 4. Merge received files and combine the results from both studies into one file

If you skip step 3, please name the files as `new_stories_{labeller_number}.xlsx`.

```sh
python main.py merge-labellers_files
python main.py combine-labelled_files
```

### 5. Extract examples for which labellers assigned radically different scores

We compare labeller 0 from the original study with labeller 0 from our reproduction study (and so on). This means that another combination of labellers might have agreed on some of these examples, but they were assigned a different labeller ID. The converse is also true.

Still, we use this approach to analyze divergent examples because this is how labellers were assigned to examples in the original experiment.

```sh
python main.py extract-divergent_examples 4
python main.py extract-divergent_examples 3
```

### 6. Show mean and standard deviation scores

```sh
python main.py stories-stats --system Ours
python main.py stories-stats --system PAQ
python main.py stories-stats --system groundtruth

python main.py stories-stats --system Ours --skip-labellers 1
python main.py stories-stats --system PAQ --skip-labellers 1
python main.py stories-stats --system groundtruth --skip-labellers 1
```

### 7. Show the results of statistical significance tests comparing the systems

```sh
python main.py stats-significance
python main.py stats-significance --skip-labellers 1
```

### 8. Show the annotator agreement between pairs of labellers

```sh
python main.py annotator-agreement
python main.py annotator-agreement --label-source1 new --label-source2 new
python main.py annotator-agreement --label-source1 new
python main.py annotator-agreement --system Ours --label-source1 new --label-source2 new
python main.py annotator-agreement --labeller1 0 --labeller1 1
```
