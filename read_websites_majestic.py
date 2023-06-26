import pandas as pd
import argparse

if __name__ == "__main__":
    input_filename = "majestic_million.csv"
    output_filename = "websites_majestic_million.txt"
    n_websites = 100
    skip_rows = 0 

    # Initialize args parser
    parser = argparse.ArgumentParser(description="get txt file with website domains from majestic million csv",
                                     usage="python3 read_websites_majestic.py --input_file {input_file} --output_file {output-file} --n_websites {n_websites} --n_skipped {n_skipped}")
    parser.add_argument("--input_file", help="path to majestic million csv file")
    parser.add_argument("--output_file", help="output txt file name")
    parser.add_argument("--n_websites", help="number of websites to use")
    parser.add_argument("--n_skipped", help="number of websites to skip from the beginning of the list")

    # Read args
    args = parser.parse_args()
    if args.input_file:
        input_filename = args.input_file
    if args.output_file:
        output_filename = args.output_file
    if args.n_websites:
        n_websites = args.n_websites
    if args.n_skipped:
        skip_rows = args.n_skipped


    df = pd.read_csv(input_filename, nrows=int(n_websites), skiprows=list(range(1, int(skip_rows)+1)))
    domains = df["Domain"].values
    with open(output_filename, "w") as f:
        for domain in domains:
            print(domain, file=f)
