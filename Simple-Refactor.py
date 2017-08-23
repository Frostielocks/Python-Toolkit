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


def print_exit(files, old, new):
    print("Replaced all instances of %s to %s in file(s):" % (old, new))
    for path in files:
        print(path)


def main():
    del sys.argv[0]

    if len(sys.argv) == 1:
        result = extract_from_file(sys.argv[0])
    elif len(sys.argv) == 3:
        result = sys.argv
        result[0] = [result[0]]
    else:
        print("Invalid # of arguments!")
        sys.exit()

    for path in result[0]:
        handler(path, result[1], result[2])
    print_exit(result[0], result[1], result[2])


main()
