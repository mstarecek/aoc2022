import re

eq = "(((4) + ((2) * (((humn)) - (3)))) / (4)) == (((32) - (2)) * (5))"

regex = re.compile(r"(?P<a>\(\d+\)) (?P<op>[\+\-\*\/]) (?P<b>\(\d+\))")

print("before:", eq)
while to_resolve := regex.findall(eq):
    for simple in to_resolve:
        orginal = " ".join(simple)
        result = eval(orginal)
        eq = eq.replace(orginal, str(result))
        print("after", eq)
