import sys
import os
import io

import json
import oyaml as yaml
import jsonpickle

from collections import OrderedDict

def to_json(filename):
    with open(filename, 'r') as infile:
        return yaml.load(infile.read(), Loader=yaml.SafeLoader)

def to_yaml(json, filename):
    with open(filename, 'w') as outfile:
        yaml.dump(json, outfile)

def access_map(m, keys):
    out = m
    for k in keys:
        if k in out:
            out = out[k]
        else:
            raise Exception(f'{".".join(keys)} not in map')
    return out

def replace_key_map(m, origkeys, keys):
    for i, k in enumerate(origkeys):
        if len(origkeys) - 1 == i:
            print(f'Replacing {".".join(origkeys)} with {".".join(keys)}')
            
            if len(keys) > len(origkeys):
                v = m[k]
                del m[k]
                remaining_new_keys = keys[i:]
                for sub_i, nk in enumerate(remaining_new_keys):
                    if sub_i == len(remaining_new_keys) - 1:
                        m[nk] = v
                        break
                    new_field = OrderedDict()
                    m[nk] = new_field
                    m = new_field
                    
                
            else:
                m[keys[i]] = m[k]
                del m[k]
        else:
            m = m[k]


def replace_json_field(json, orig, new):
    v = access_map(json, orig.split('.'))
    replace_key_map(json, orig.split('.'), new.split('.'))

def main():
    if len(sys.argv) < 2:
        print('Pass YAML file to convert to JSON')
        sys.exit(1)

    # e.g. src\main\resources\application.yml

    if not os.path.isfile(sys.argv[1]):
        print('The passed parameter is not a valid file')
        sys.exit(2)

    filename = sys.argv[1]
    outfilename = sys.argv[2]
    json = to_json(filename)

    replace_json_field(json,
     'spring.security.oauth2.client.provider.okta.user-name-attribute',
     'spring.security.oauth2.client.provider.okta.userNameAttribute')

    replace_json_field(json,
    'logging.file',
    'logging.file.name')

    replace_json_field(json,
    'spring.profiles',
    'spring.config.activate.on-profile')

    to_yaml(json, outfilename)
    with open(outfilename, 'r') as output:
        print(output.read())

def check(outfilename):
    with open(outfilename, 'r') as output:
        with open('expected.yml', 'r') as expected:
            iexpected = iter(expected)
            for i, ioutput in enumerate(output):
                expectedline = next(iexpected)
                if ioutput != expectedline:
                    print(f'Mismatch at {i}:\nExpected:{expectedline}\nWas:{ioutput}')


if __name__ == '__main__':
    main()