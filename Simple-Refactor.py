import sys


def refactor(contents, old, new):
    for count in range(len(contents)):
        line = contents[count]
        start = 0
        while start < len(line):
            index = line[start: len(line)].find(old)
            if index == -1:
                break
            line = line[0: index] + new + line[index + len(old): len(line)]
            start += index + len(old)
        contents[count] = line


def handler(path, old, new):
    file = open(path, "r")
    contents = file.readlines()
    file.close()

    refactor(contents, old, new)

    file = open(path, "w")
    contents = "".join(contents)
    print(contents)
    file.write(contents)
    file.close()


def extract_from_file(path):
    file = open(path, "r")
    contents = file.readlines()
    file.close()
    if len(contents) < 3:
        raise SyntaxError

    files = []
    for number in range(len(contents) - 2):
        files.append(contents[number + 2].rstrip())
    return [files, contents[0].rstrip(), contents[1].rstrip()]


def main():
    result = sys.argv
    del result[0]

    if len(result) == 3:
        handler(result[0], result[1], result[2])
    elif len(result) == 1:
        result = extract_from_file(result[0])
        for path in result[0]:
            handler(path, result[1], result[2])
    else:
        print("Invalid amount of command line arguments!")


main()
