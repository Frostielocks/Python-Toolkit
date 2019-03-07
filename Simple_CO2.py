import urllib.request
import sys
import time


def get_substring_between(string, start_target, end_target):
    start = string.rfind(start_target) + len(start_target)
    string = string[start: len(string)]
    return string[0: string.find(end_target)]


def write_to_file(filepath, ip_addres):
    file = open(filepath, 'a+')
    file.write("Date: %s  -  IP: %s\n" % (time.strftime("%d/%m/%Y"), ip_addres))
    return


def main():
    del sys.argv[0]

    html = urllib.request.urlopen('https://www.esrl.noaa.gov/gmd/ccgg/trends/monthly.html').read()
    co2 = get_substring_between(html.decode("utf-8"),
        "&nbsp;&nbsp; </td><td> ",
        "</td></tr>")
    print("Daily co2 is: %s" % co2)
    if len(sys.argv) == 1:
        write_to_file(sys.argv[0], ip_adress)
    return


main()
