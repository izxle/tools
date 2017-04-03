#!/bin/env python

from reader import Check, Folder
from analysisalgs import *
from myfunctions import parse_int_set
from os import getcwd, walk
import argparse

def getArgs(argv=[]):
    kw = {'description': '',
          'formatter_class': argparse.ArgumentDefaultsHelpFormatter}
    parser = argparse.ArgumentParser(**kw)
    
    parser.add_argument('-v', action='count', help='verbosity', default=0)
    parser.add_argument('--verb', '--verbose', type=int, dest='v', default=0)
    parser.add_argument('-p', '--path', dest='f_path', default=getcwd())
    parser.add_argument('-f', '--folder', dest='f_path', default=getcwd())
    parser.add_argument('--sd', '--subdir', '--sub-directory', dest='subdir',
                        default='')
    parser.add_argument('-i', '--ignore', nargs='+', dest='i', default=[])
    parser.add_argument('-r', '--raw', action='store_true', dest='r', 
                        default=False)
    parser.add_argument('--MD', action='store_true', default=False)
    parser.add_argument('-g', '--graph', '--plot', action='store_true',
                        default=False, dest='plot')
    parser.add_argument('--ads', nargs='+', default=[],
                        help='starts the energy difference algorithm')
    parser.add_argument('--nam', '--nams', nargs='*', dest='nams',
                        help='name of exlusive directories to be read')
    parser.add_argument('-w', '--write', action='store_true', default=False)
    parser.add_argument('--free-en', action='store_true', default=False)
    
    choices = ['io_step', 'F', 'F_n', 'e_step',
               'E0', 'dE', 'Temp', 'E', 'm', 't']
    parser.add_argument('--rep', '--reps', '--report', nargs='*', dest='reps',
                        choices=choices)
    parser.add_argument('--test', action='store_true',
                        help='kyeword for testing purposes.')
    args = parser.parse_args(argv.split()) if argv else parser.parse_args()
    
    if not args.reps:
        args.reps = ['io_step', 'e_step', 'dE'] if args.reps == [] else []

    parsadd = argparse.ArgumentParser(prefix_chars='+', **kw)
    parsadd.add_argument('part', nargs='*', default=[])
    parsadd.add_argument('+b', '++bulk', default='')
    parsadd.add_argument('+a','++ads', default='')
    parsadd.add_argument('++nam', '++nams', dest='nams', nargs='*')
    parsadd.add_argument('++area', nargs='?', type=float, default=None, const=True)
    parsadd.add_argument('+v', action='count', default=0)
    
    if args.MD:
        reps = args.reps if args.reps is not None else []
        for i, rep in enumerate(["io_step", "E", "Temp"]):
            if rep not in reps:
                reps.insert(i, rep)
            elif reps.index(rep) != i:
                reps.remove(rep)
                reps.insert(i, rep)
        args.reps = reps

    if args.ads: args.ads = parsadd.parse_args(args.ads)

    if args.v > 1: printv('args:\n', args)
    return args

def main(argv=[]):
    args = getArgs(argv)
    if args.test: return printv(args)
    kw = vars(args)
    hasdirs = next(walk(args.f_path))[1]
    # get output info
    if not hasdirs:
        kw['pad'] = "  "
        info = Check(**kw)
    else:
        if not args.reps:
            args.reps = ['F', 't']
        info = Folder(**kw)
    res = info
    # data analysis
    if args.ads:
        res = Ediff(info, parts=vars(args.ads), v=args.v, freeEn=args.free_en)
    elif args.MD:
        assert isinstance(info, Folder), "Target must contain directories"
        res = MDynn(info)
    # output
    printv(res)

if __name__=='__main__':
    main()
