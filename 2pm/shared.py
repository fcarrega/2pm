# Formatting methods
def output_string(elements):
    output = ''
    for element in elements[:-1]:
        output += element + ', '
    output += elements[-1]
    print(output)
