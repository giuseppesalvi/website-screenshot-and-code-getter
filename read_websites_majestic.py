import pandas as pd

if __name__ == "__main__":
    input_filename = "~/Desktop/Tesi/materiale/majestic_million.csv"
    output_filename = "websites_majestic_million.txt"
    n_websites = 100
    df = pd.read_csv(input_filename, nrows=n_websites)
    domains = df["Domain"].values
    with open(output_filename, "w") as f:
        for domain in domains:
            print(domain, file=f)
