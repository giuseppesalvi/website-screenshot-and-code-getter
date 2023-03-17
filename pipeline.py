#results_folder

# 1. Create websites list
## python3 read_websites_majestic.py --input_file ~/Desktop/Tesi/materiale/majestic_million.csv --output_file websites_majestic_million_big.txt --n_websites 2 --n_skipped 0

# 2. Run script to get websites code and screenshots
## python3 main.py --website_list websites_majestic_million_big.txt --task code --just_new --task all --batch 2

# Find included / excluded results
#find_included_excluded(results_folder)

# Use screenshot classifier to check if included results are good or bad
# And write final list of good results

# Run script to calculate stats