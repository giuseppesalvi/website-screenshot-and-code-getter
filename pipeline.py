#results_folder

# 1. Create websites list
## python3 read_websites_majestic.py --input_file ~/Desktop/Tesi/materiale/majestic_million.csv --output_file websites_majestic_million_big.txt --n_websites 2 --n_skipped 0

# 2. Run script to get websites code and screenshots
## python3 main.py --website_list websites_majestic_million_big.txt --task code --just_new --task all --batch 1000

# Find included / excluded results
## python3 find_included_excluded --results_folder results_websites_majestic_million_big.txt

# Use screenshot classifier to check if included results are good or bad
# And write final list of good results
## python3 screenshot_classifier/classify_new_images --results_folder results_websites_majestic_million_big

# Move good results in folder
## python3 move_good_results --results_folder results_websites_majestic_million_big

# Run script to calculate stats
## python3 stats.py --results_folder results_websites_majestic_million_big