import string
import re

# Formatting methods
def output_string(elements):
    output = ''
    for element in elements[:-1]:
        output += element + ', '
    output += elements[-1]
    print(output)

# Parameterize string
def parameterize(s):
    result = s.lower()
    result = result.replace('&', 'and')
    result = re.sub('[{0}]'.format(string.punctuation), '', result)
    result = re.sub('(\s+)', '_', result)
    return result

# Format date
def format_date(date):
    splitted_date = date.split('/')
    day   = splitted_date[1].zfill(2)
    month = splitted_date[0].zfill(2)
    year  = splitted_date[2].zfill(4)
    return year + month + day

# Cast value
def cast(value):
    return 0 if value == '-' else float(value)

# Merge dictionnaries
def merge(d1, d2):
    for k in d2:
        if k in d1 and isinstance(d1[k], dict) and isinstance(d2[k], dict):
            merge(d1[k], d2[k])
        else:
            d1[k] = d2[k]
