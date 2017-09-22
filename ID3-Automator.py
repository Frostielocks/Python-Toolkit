import urllib.request
import sys
import eyed3


# Program that automates id3 tag writing to .mp3 files.
# The programs assumes that all the .mp3 files are initialized with their publishing years.
# ssy.argv[0] contains the wikipedia link to the album of the files.
# sys.argv[1] contains the path to the rule-contents (see documentation assign_contents).

# Get all substrings of a string that are located between two targets (start and end).
def get_all_substrings_between(string, start_target, end_target):
    result = list()
    start = string.find(start_target)
    while start != -1:
        string = string[start + len(start_target): len(string)]
        # former_string = former_string[0, start] + former_string[start, start + len(start_target)] + string

        # Correct for the second usage of end_target, this is done bcs of wikipedia's html layout.
        # Find the first usage:
        end1 = string.find(end_target)
        # Find the second usage:
        end2 = string[end1 + len(end_target): len(string)].find(end_target) + len(end_target)
        end = end1 + end2

        # Add the sub string to result and set-up for the next loop.
        result.append(string[0: end])
        string = string[end + len(end_target): len(string)]
        start = string.find(start_target)
    return result


# Extract all the targets from a string.
def extract(string, target):
    start = string.find(target)
    while start != -1:
        start_string = string[0: start]
        end_string = string[start + len(target): len(string)]
        string = start_string + end_string
        start = string.find(target)
    return string


# Extracts everything between the first usage of start_target to end_target (including targets).
def extract_first_usage_between(string, start_target, end_target):
    start = string.find(start_target)
    if start == -1:
        return string
    start_string = string[0: start]
    end = string.find(end_target) + len(end_target)
    end_string = string[end: len(string)]
    return start_string + end_string


# Extract song title name from a link tag.
def extract_title_from_link_tag(string, contents):
    start_target = "<a href="
    start = string.find(start_target)
    if start == -1:
        return string
    start_string = string[0: start]

    start_target = "title="
    start = string.find(start_target)
    end_target = " (" + contents[0] + " song)"
    end = string.find(end_target)

    flag = False
    if end == -1:
        flag = True
        end_target = ">"
        end = string.find(end_target)
    end_string = string[start + len(start_target): end]

    if flag:
        true_end_target = "</a>"
        true_end = string.find(true_end_target)
        end_string += string[true_end + len(true_end_target): len(string)]

    return start_string + end_string


# Substitute all the original targets with the new targets.
def substitute(string, og_target, new_target):
    start = string.find(og_target)
    while start != -1:
        start_string = string[0: start]
        end_string = string[start + len(og_target): len(string)]
        string = start_string + new_target + end_string
        start = string.find(og_target)
    return string


# Extract all the garbage from a given output.
def extract_garbage(output, contents):
    extract_tasks = ["</td>", "<td style=\"vertical-align:top\">", "\"", "\n",
                     "<span style=font-size:85%>", "</span>", "</span"]
    substitute_tasks = [[" / ", " "], [" : ", " "], ["&amp;", "&"]]
    for i in range(len(output)):
        string = output[i]
        for j in range(len(extract_tasks)):
            string = extract(string, extract_tasks[j])
        for j in range(len(substitute_tasks)):
            string = substitute(string, substitute_tasks[j][0], substitute_tasks[j][1])

        # string = extract_first_usage_between(string, " <span", "</span>")
        string = extract_title_from_link_tag(string, contents)
        output[i] = string
    return output


def extract_artist(string):
    string = extract(string, " (featuring ")
    string = extract(string, ")")
    string = substitute(string, " and ", ";")
    return string


# Generate the [song_name, song_number] pairs.
def generate_pairs(output, contents):
    result = list()
    for i in range(len(output)):
        temp = ["Song","Number", "Artists"]
        string = output[i]
        pivot1 = string.find(".")
        temp[1] = string[0: pivot1]

        pivot2 = string.find(" (featuring ")
        if pivot2 == -1:
            temp[0] = string[pivot1 + 1: len(string)]
            temp[2] = contents[0]
        else:
            temp[0] = string[pivot1 + 1: pivot2]
            temp[2] = string[pivot2: len(string)]
            temp[2] = "Logic;" + extract_artist(temp[2])

        result.append(temp)
    return result


# Assign id3 tags to files.
def assign_files(output, contents):
    artist = contents[0]
    album = contents[1]
    genre = contents[2]
    publisher = contents[3]
    debug = contents[4]

    for item in output:
        title = item[0]
        number = item[1]
        all_artists = item[2]
        try:
            audiofile = eyed3.load(artist + " - " + title + ".mp3")
        except IOError:
            continue

        audiofile.tag.title = title
        audiofile.tag.artist = all_artists
        audiofile.tag.album_artist = artist
        audiofile.tag.album = album
        audiofile.tag.track_num = int(number)
        audiofile.tag.genre = genre
        audiofile.tag.publisher = publisher
        audiofile.tag.save()

        if debug == "True":
            print(audiofile.tag.title)
            print(audiofile.tag.artist)
            print(audiofile.tag.album_artist)
            print(audiofile.tag.album)
            print(audiofile.tag.track_num)
            print(audiofile.tag.genre)
            print(audiofile.tag.publisher)


# Returns contents from file path: [artist, album, genre, publisher, debug]
def assign_contents(path):
    file = open(path, "r")
    contents = file.readlines()
    file.close()
    if len(contents) < 5:
        raise SyntaxError

    for i in range(len(contents)):
        contents[i] = contents[i].rstrip()
    return contents


def main():
    del[sys.argv[0]]
    if dev_debug:
        sys.argv.append("https://en.wikipedia.org/wiki/Young_Sinatra_(mixtape)")
        sys.argv.append("rules.txt")
    html = urllib.request.urlopen(sys.argv[0]).read()
    contents = assign_contents(sys.argv[1])

    color1 = "<tr style=\"background-color:#fff\">\n"
    color2 = "<tr style=\"background-color:#f7f7f7\">\n"
    garbage = "<td style=\"padding-right:10px;text-align:right;vertical-align:top\">"
    end_target = "<td style=\"vertical-align:top\">"

    list1 = get_all_substrings_between(html.decode("utf-8"), color1 + garbage, end_target)
    list2 = get_all_substrings_between(html.decode("utf-8"), color2 + garbage, end_target)
    output = list1 + list2

    output = extract_garbage(output, contents)
    output = generate_pairs(output, contents)
    if dev_debug:
        for item in output:
            print(item)
    assign_files(output, contents)


dev_debug = False
main()
