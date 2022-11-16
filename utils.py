def website2domain(website):
    """ Return domain of the given website URL """

    if "//www." in website:
        domain = website.split("//www.")[-1].split("/")[0]
    else:
        domain = website.split("//")[-1].split("/")[0]
    return domain


def sort_websites_by_nodes(filepath):
    """ Sort website names in log file by ascending number of nodes """

    print("\nSorting websites by number of nodes in ascending order...")
    websites = []

    # Read list of websites and nodes from file
    with open(filepath, "r") as f:
        for line in f:
            websites.append(
                (line.strip().split(" ")[0], int(line.strip().split(" ")[1])))

    # Write the list of websites and nodes sorted by number of nodes
    websites.sort(key=lambda tup: tup[1])
    with open(filepath, "w") as f:
        last = ""
        for website in websites:
            if website != last:  # Remove duplicates from the list
                f.write(website[0] + " " + str(website[1]) + "\n")
            last = website


def sort_websites_by_image_aspect_ratio(filepath):
    """ Sort website names in log file by ascending screenshot image aspect ratio"""

    print("\nSorting websites by ascending screenshot image size...")
    websites = []

    # Read list of websites and nodes from file
    with open(filepath, "r") as f:
        for line in f:
            websites.append(
                (line.strip().split(" ")[0], line.strip().split(" ")[1], line.strip().split(" ")[2]))

    # Write the list of websites and nodes sorted by aspect ratio
    websites.sort(key=lambda tup: (float(tup[2])), reverse=True)
    with open(filepath, "w") as f:
        last = ""
        for website in websites:
            if website != last:  # Remove duplicates from the list
                f.write(website[0] + " " + str(website[1]) +
                        " " + str(website[2]) + "\n")
            last = website
