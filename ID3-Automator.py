import urllib.request
import sys
import eyed3


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
    end_string = string[start + len(start_target): end]
    return start_string + end_string


# Extract all the garbage from a given output.
def extract_garbage(output, contents):
    extract_tasks = ["</td>", "<td style=\"vertical-align:top\">", "\"", "\n"]
    for i in range(len(output)):
        string = output[i]
        for j in range(len(extract_tasks)):
            string = extract(string, extract_tasks[j])

        string = extract_first_usage_between(string, " <span", "</span>")
        string = extract_title_from_link_tag(string, contents)
        output[i] = string
    return output


# Generate the [song_name, song_number] pairs.
def generate_pairs(output):
    result = list()
    for i in range(len(output)):
        string = output[i]
        pivot = string.find(".")
        result.append([string[pivot + 1: len(string)], string[0: pivot]])
    return result


# Assign id3 tags to files.
def assign_files(output, contents):
    artist = contents[0]
    album = contents[1]
    genre = contents[2]
    publisher = contents[3]
    debug = contents[4]

    for pair in output:
        # if debug == "True":
        #     print(pair)
        title = pair[0]
        number = pair[1]
        try:
            audiofile = eyed3.load(artist + " - " + title + ".mp3")
        except IOError:
            continue

        audiofile.tag.title = title
        audiofile.tag.artist = artist
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


# Returns contents: [Artist, Album, Genre, Publisher, Debug]
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
    # sys.argv.append("https://en.wikipedia.org/wiki/Young_Sinatra:_Welcome_to_Forever")
    # sys.argv.append("rules.txt")
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
    output = generate_pairs(output)
    # for item in output:
    #     print(item)
    assign_files(output, contents)


main()
