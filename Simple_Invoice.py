import json
import sys


class Invoice:
    total = 0
    output = ""


    def __init__(self, json_dict):
        if not json_dict:
            return

        for payment in json_dict:
            if not payment["optional"]:
                self.add_payment_to_output(payment)
        self.add_total_to_output("required")

        changed = False
        for payment in json_dict:
            if payment["optional"]:
                if not changed:
                    changed = True
                self.add_payment_to_output(payment)
        if changed:
            self.add_total_to_output("required + optional")


    def add_payment_to_output(self, payment):
        self.total += payment["price"]

        if payment["price"] < 0:
            self.output += "-"
        else:
            self.output += "+"

        self.output += " %06.2f  %s  %s\n" % \
                (
                    abs(payment["price"]),
                    payment["date"],
                    payment["place"]
                )


    def add_total_to_output(self, message):
        self.output += ("-" * 8) + "\n"
        self.output += "= %06.2f  %s\n" % (self.total, message)


if len(sys.argv) > 1:
    fd = open(sys.argv[1], 'r')
    json_data = json.load(fd)
    invoice = Invoice(json_data["invoice"])

    print(invoice.output)
