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

#### 2.1.1 Add debian buster

```
%shell
cat > /etc/apt/sources.list.d/debian.list <<'EOF'
deb [arch=amd64 signed-by=/usr/share/keyrings/debian-buster.gpg] http://deb.debian.org/debian buster main
deb [arch=amd64 signed-by=/usr/share/keyrings/debian-buster-updates.gpg] http://deb.debian.org/debian buster-updates main
deb [arch=amd64 signed-by=/usr/share/keyrings/debian-security-buster.gpg] http://deb.debian.org/debian-security buster/updates main
EOF
```

#### 2.1.2 Add keys

```
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys DCC9EFBF77E11517
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 648ACFD622F3D138
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 112695A0E562B32A
```

```
apt-key export 77E11517 | gpg --dearmour -o /usr/share/keyrings/debian-buster.gpg
apt-key export 22F3D138 | gpg --dearmour -o /usr/share/keyrings/debian-buster-updates.gpg
apt-key export E562B32A | gpg --dearmour -o /usr/share/keyrings/debian-security-buster.gpg
```

#### 2.1.3 Prefer debian repo for chromium* packages only
<!-- Note the double-blank lines between entries -->

```
cat > /etc/apt/preferences.d/chromium.pref << 'EOF'
Package: *
Pin: release a=eoan
Pin-Priority: 500
```


```
Package: *
Pin: origin "deb.debian.org"
Pin-Priority: 300
```


```
Package: chromium*
Pin: origin "deb.debian.org"
Pin-Priority: 700
EOF
```

#### 2.1.4 Install chromium and chromium-driver

```
apt-get update
apt-get install chromium chromium-driver
```


### 2.2 Create websites list

```
python3 read_websites_majestic.py --input_file ~/Desktop/Tesi/materiale/majestic_million.csv --output_file websites_majestic_million_big.txt --n_websites 10000 --n_skipped 0
```

### 2.3 Run script to get websites code and screenshots

```
python3 main.py --website_list websites_majestic_million_big.txt --task code --just_new --task all --batch 1000
```

### 2.4 Find included / excluded results

```
python3 find_included_websites.py --results_folder results_websites_majestic_million_big
```

### 2.5 Use screenshot classifier to check if included results are good or bad and write final list of good results

```
python3 screenshot_classifier/classify_new_images.py --results_folder results_websites_majestic_million_big
```

### 2.6 Move good results in folder

```
python3 move_good_results.py --results_folder results_websites_majestic_million_big
```

### 2.7 Run script to calculate stats

```
python3 stats.py --results_folder results_websites_majestic_million_big
```