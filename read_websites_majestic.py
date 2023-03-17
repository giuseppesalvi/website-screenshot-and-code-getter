import pandas as pd

if __name__ == "__main__":
    input_filename = "~/Desktop/Tesi/materiale/majestic_million.csv"
    output_filename = "websites_majestic_million2.txt"
    n_websites = 100
    skip_rows = 100
    df = pd.read_csv(input_filename, nrows=n_websites, skiprows=list(range(1, skip_rows+1)))
    domains = df["Domain"].values
    with open(output_filename, "w") as f:
        for domain in domains:
            print(domain, file=f)
