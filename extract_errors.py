from collections import Counter

ERRORS_TO_AGGREGATE = [
    ["Message: element click intercepted: Element", "is not clickable at point"],
    ["Message: timeout: Timed out receiving message from renderer"],
    ["Message: unknown error: unhandled inspector error", "Unable to capture screenshot"],
    ["Message: element click intercepted"],
    ["Failed to parse:", "label empty or too long"],
    ["Failed to establish a new connection", "No address associated with hostname"],
    ["Command 'clean-html", "returned non-zero exit status 1"],
    ["Connection broken: ConnectionResetError","Connection reset by peer"],
    ["Connection aborted.", "Transport endpoint is not connected"],
    ["Received response with content-encoding: br, but failed to decode it.", "Error", "Decompression error"],
    ["ConnectionPool", "Read timed out."],
    ["Caused by SSLError", "doesn't match"],
    ["Caused by SSLError", "certificate verify failed: unable to get local issuer certificate"],
    ["Caused by SSLError", "certificate verify failed: self signed certificate"],
    ["Caused by SSLError", "certificate verify failed: certificate has expired"],
    ["Caused by SSLError", "unrecognized name"],
    ["Caused by SSLError", "wrong version number"],
    ["Caused by SSLError", "alert internal error"],
    ["Caused by SSLError", "alert handshake failure"],
    ["Caused by ConnectTimeoutError", "Connection to", "timed out."],
    ["Caused by NewConnectionError", "Failed to establish a new connection:", "No route to host"],
    ["Caused by NewConnectionError", "Failed to establish a new connection", "Temporary failure in name resolution"],
    ["Caused by NewConnectionError", "Failed to establish a new connection", "Name or service not known"],
    ["Caused by NewConnectionError", "Failed to establish a new connection", "Connection timed out"],
    ["Caused by NewConnectionError", "Failed to establish a new connection", "Connection refused"],
    ["Caused by NewConnectionError", "Failed to establish a new connection", "No address associated with hostname"],
    ["Connection aborted", "ConnectionResetError", "Connection reset by peer"],
    ["Connection aborted", "OSError", "Error"]
]


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

    filtered_list_errors = [
        string for string in list_errors if not string.startswith("Exception")]
    counted_list = Counter(filtered_list_errors)
    reduced_list = [
        f"{counted_list[string]} {string}" for string in counted_list]
    #sorted_list = sorted(reduced_list, key=lambda x: int(x.split()[0]), reverse=True)
    # return sorted_list
    return reduced_list


def aggregate_errors(list_errors):
    dict_error_lines = {}
    # with open("experiments/errors_summary_80000.txt", "r") as f:
    # for line in f.readlines():
    total_errors = 0
    for line in list_errors:
        splitted_line = line.split(" ")
        count = splitted_line[0]
        total_errors += int(count)
        error_msg = " ".join(splitted_line[1:])
        for error_msg_components in ERRORS_TO_AGGREGATE:
            if all(component in error_msg for component in error_msg_components):
                error_msg = " - ".join(error_msg_components)
                continue
        if error_msg in dict_error_lines:
            dict_error_lines[error_msg] += int(count)
        else:
            dict_error_lines[error_msg] = int(count)
    # pprint.pprint(dict_error_lines)

    list_error_lines = []
    for key in dict_error_lines.keys():
        list_error_lines.append(str(dict_error_lines[key]) + " {:.2f}% ".format(dict_error_lines[key] / total_errors * 100) + key)
    sorted_list_error_lines = sorted(
        list_error_lines, key=lambda x: int(x.split()[0]), reverse=True)
    with open("experiments/errors_summary_80000.txt", "w") as f:
        print("Total = ", total_errors, file=f)
        for line in sorted_list_error_lines:
            print(line, file=f)
    return


if __name__ == "__main__":
    list_errors = extract_errors()
    # for line in list_errors:
    #    print(line)
    aggregate_errors(list_errors)
