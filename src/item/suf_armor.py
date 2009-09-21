import random

def LesserProtection(item):
    item.full_name += ' of lesser Protection'
    item.dv += random.randint(5, 25)
