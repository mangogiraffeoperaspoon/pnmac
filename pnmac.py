import sys
import xml.dom.minidom

WEATHER_DATA_FILE = 'w_data.dat'
SOCCER_DATA_FILE = 'soccer.dat'

def slurp(filepath):
    with open(filepath) as f:
        return f.read()

def xml_get_pre_elem_content(s):
    '''Given an xml string, return contents
    inside the first instance of the
    `pre` element as a string.'''
    dom = xml.dom.minidom.parseString(s)
    # Find pre elem, get its child nodes and call toxml on each one,
    # then join results into a single string:
    return ''.join(map(lambda x: x.toxml(),
                       dom.getElementsByTagName('pre')[0].childNodes))

def is_blank_line(line):
    return line.strip() == ''

def is_divider_line(line):
    '''Checks if line (string) is a visually horizontal
    line made of a single repeating character
    (e.g., '-' or '=').'''
    x = line.strip()
    if not x: return False
    first_char = x[0]
    return x.count(first_char) == len(x)

def parse_fixed_width_data(s, has_title_line=True,
                           ignore_blank_lines=True, ignore_divider_lines=True):
    '''Given a string representation of a
    fixed-width data table, parse it and
    return a sequence of dictionaries.'''
    found_title = False
    headers = None
    out = []
    # Single pass through everything.
    lines = s.splitlines()
    for line in lines:
        if ignore_blank_lines and is_blank_line(line): continue
        if ignore_divider_lines and is_divider_line(line): continue
        if has_title_line and not found_title:
            found_title = True
            continue
        len_line = len(line) # tiny perf opt
        if not headers:
            # One time: build headers data structure (seq of tuples
            # where tuple is (header-name, header-start-pos)
            header_names = line.split()
            header_pos = map(lambda x: line.find(x), header_names)
            headers = list(zip(header_names, header_pos))
            # Add a one-past-the-end header; helps us later when we do i+1
            headers.append( ('$EOL$', len_line) )
            continue
        row = {}
        for i, (header, pos) in enumerate(headers):
            if header == '$EOL$': continue
            next_pos = min(len_line, headers[i+1][1])
            row[header] = line[pos:next_pos].strip()
        out.append(row)
    return out

def find_smallest_temp_spread(weather_data_filepath):
    '''Takes a filepath pointing to a weather data
    file. Returns day of the month with the smallest
    temperature spread.'''
    data = parse_fixed_width_data(
                xml_get_pre_elem_content(
                    slurp(weather_data_filepath)))
    # Do some tidying of the data.
    # Might have 'month' row at the end; remove row.
    if data[len(data)-1]['Dy'] == 'mo':
        data.pop(len(data)-1)
    # Temperature values might have trailing '*'; remove.
    for row in data:
        row['MxT'] = row['MxT'].replace('*', '').strip()
        row['MnT'] = row['MnT'].replace('*', '').strip()
    # Find day of interest and return.
    comp = lambda x: float(x['MxT']) - float(x['MnT'])
    return min(data, key=comp)['Dy']

def find_smallest_soccer_score_diff(soccer_data_filepath):
    '''Takes a filepath pointing to a soccer data
    file. Returns name of team having the smallest
    difference in 'for' and 'against' goals.'''
    data = parse_fixed_width_data(
                xml_get_pre_elem_content(
                    slurp(soccer_data_filepath)),
                has_title_line=False)
    # Do some tidying of the data.
    # Data format results in 'F' values having trailing '-' char; remove.
    for row in data:
        row['F'] = row['F'].replace('-', '').strip()
    # Find team and return.
    comp = lambda x: abs(float(x['F']) - float(x['A']))
    return min(data, key=comp)['Team']

def main():
    usage = '''Usage:
Run with provided weather file:
    python3 pnmac.py weather
Run with custom weather file:
    python3 pnmac.py weather my-weather-data.dat
Run with provided soccer file:
    python3 pnmac.py soccer
Run with custom soccer file:
    python3 pnmac.py soccer my-soccer-data.dat'''
    EX_USAGE = 64 # /usr/include/sysexits.h
    if len(sys.argv) < 2:
        print(usage)
        sys.exit(EX_USAGE)
    kind = sys.argv[1]
    f = None
    if len(sys.argv) == 3:
        f = sys.argv[2]
    if kind == 'weather':
        f = WEATHER_DATA_FILE if not f else f
        print(find_smallest_temp_spread(f))
        sys.exit(0)
    elif kind == 'soccer':
        f = SOCCER_DATA_FILE if not f else f
        print(find_smallest_soccer_score_diff(f))
        sys.exit(0)
    else:
        print(usage)
        sys.exit(EX_USAGE)

if __name__ == '__main__': main()

