#!/bin/env python

from ase.io import write, read
from os import listdir, getcwd
import argparse

def getArgs(args=None):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    nams = listdir(getcwd())
    for nam in ['CONTCAR', 'POSCAR']:
        if nam in nams: break
    parser.add_argument('file', nargs='?', default=nam, help='old name')
    parser.add_argument('format', nargs='?', default='cif', help='new format')
    parser.add_argument('new_name', nargs='?', default=None, help='new_name.format')
    parser.add_argument('-f', help='old format')
    parser.add_argument('-n', '--name', default=None, dest='name',
                        help='overwrite new name')
    if args:
        res = parser.parse_args(args.split())
    else:
        res = parser.parse_args()
    if res.name:
        res.nam = res.name
    else:
        if not res.new_name:
            res.new_name = res.file
        res.nam = '{}.{}'.format(res.new_name, res.format)
    return res

def main(argv=None):
    args = getArgs(argv)
    if args.f:
        struct = read(args.file, format=args.f)
    else:
        struct = read(args.file)
    kw = {"format": args.format}
    if args.format == 'vasp':
        kw['sort'] = True
        kw['vasp5'] = True
        kw['direct'] = True
    write(res.nam, struct, **kw)

if __name__ == '__main__':
    main()
