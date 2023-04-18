from collections import Counter

def extract_errors():
    list_errors = [] 
    print_next = False
    with open("experiments/errors_80000.txt", "r") as f:
        for line in f.readlines():
            if print_next:
                list_errors.append(line)
                print_next = False

            elif line.startswith("Exception"):
                list_errors.append(line)
                print_next = True


    filtered_list_errors = [string for string in list_errors if not string.startswith("Exception")]
    counted_list = Counter(filtered_list_errors)
    reduced_list = [f"{counted_list[string]} {string}" for string in counted_list]
    sorted_list = sorted(reduced_list, key=lambda x: int(x.split()[0]), reverse=True)
    with open("experiments/errors_summary_80000.txt", "w") as f:
        for line in sorted_list:
            print(line, file=f, end="")
    return

if __name__ == "__main__":
    extract_errors()