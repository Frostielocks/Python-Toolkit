import urllib.request
import sys
import time


def get_substring_between(string, start_target, end_target):
    start = string.rfind(start_target) + len(start_target)
    string = string[start: len(string)]
    return string[0: get_end_index(string, end_target)]


def get_end_index(string, end_target):
    count = 0
    for c in string:
        if c == end_target:
            return count
        count += 1


def write_to_file(filepath, ip_addres):
    file = open(filepath, 'a+')
    file.write("Date: %s  -   IP: %s\n" % (time.strftime("%d/%m/%Y"), ip_addres))


def main():
    html = urllib.request.urlopen('http://ip4.me//').read()
    ip_adress = get_substring_between(html.decode("utf-8"), "<font face=\"Arial, Monospace\" size=+3>", "<")
    print("Public IP adress is: %s" % ip_adress)
    if (len(sys.argv) == 1 and sys.argv[0] == "-log"):
        write_to_file("ip_log.txt", ip_adress)


main()
