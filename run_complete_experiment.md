# **Run Complete Experiment Guide**

Follow the steps below to run the entire experiment.

## **Prerequisites: Installation**

1. **Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Node Modules**:
    ```bash
    npm install
    ```

3. **Clean HTML Tool** (Global Installation):
    ```bash
    npm install clean-html -g
    ```

## **1. Screenshot Classifier Setup**

### 1.1 Dataset Creation
Run the following command to create the dataset for the screenshot classifier:
```bash
python3 create_dataset.py
```

### 1.2 Classifier Notebook
Open and run the notebook:
**screenshot_classifier/screenshot_classifier.ipynb**

## **2. Website Screenshot & Code Retrieval**

### 2.1 Chrome Driver Installation
Follow the installation instructions for Chrome Driver...

### 2.2 Generating Website List
Generate a list of website.

Example:
Use this command to create a list of websites from the `majestic_million.csv` file:
```bash
python read_websites_majestic.py --input_file $PATH_TO_FILE$/majestic_million.csv --output_file websites_majestic_million.txt --n_websites 100 --n_skipped 0
```

### 2.3 Retrieving Code & Screenshots
Run the script with the following command:
```bash
python main.py --website_list websites_majestic_million.txt --task code --just_new --task all --batch 100
```

### 2.4 Filter Results
Filter the included/excluded results using:
```bash
python find_included_websites.py --results_folder results_websites_majestic_million
```

### 2.5 Classification of Results
Use the screenshot classifier to determine the quality of the results and generate a final list:
```bash
python screenshot_classifier/classify_new_images.py --results_folder results_websites_majestic_million
```

### 2.6 Organize Results
Move the good results to a designated folder:
```bash
python move_good_results.py --results_folder results_websites_majestic_million_big
```

### 2.7 Statistics Calculation
Compute relevant statistics using:
```bash
python stats.py --results_folder results_websites_majestic_million_big
```

