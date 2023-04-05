# Run Complete Experiment
The following are the steps to run a complete experiment

## 0. Install Requirements 

```
pip3 install -r requirements.txt
```

```
npm install
```

```
npm install clean-html -g
```

## 1. Screenshot Classifier

### 1.1 Create dataset

```
python3 create_dataset.py
```

### 1.2 Run notebook screenshot Classifier

```
screenshot_classifier/screenshot_classifier.ipynb
```

## 2. Website Screenshot and Code Getter

### 2.1 Install Chrome Driver
...

### 2.2 Create websites list

```
python3 read_websites_majestic.py --input_file majestic_million.csv --output_file websites_majestic_million_big7.txt --n_websites 10000 --n_skipped 40000 
```

### 2.3 Run script to get websites code and screenshots

```
python3 main.py --website_list websites_majestic_million_big7.txt --just_new --task all --batch 10000
```

### 2.4 Find included / excluded results

```
python3 find_included_websites.py --results_folder results_websites_majestic_million_big6
```

### 2.5 Use screenshot classifier to check if included results are good or bad and write final list of good results

```
python3 screenshot_classifier/classify_new_images.py --results_folder results_websites_majestic_million_big5
```

### 2.6 Move good results in folder

```
python3 move_good_results.py --results_folder results_websites_majestic_million_big
```

### 2.7 Run script to calculate stats

```
python3 stats.py --results_folder results_websites_majestic_million_big5
```