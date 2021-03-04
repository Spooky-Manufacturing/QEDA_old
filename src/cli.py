#!/usr/bin/python3
import getopt
import sys
from qeda.qeda import QEDAManager


def test():
    """Runs the test suite"""
    print(test)
    sys.exit(0)


def help():
    """Prints the help information to terminal"""
    print("\t\tQEDA")
    print("Quantum Electronic Design Automation Software")
    print("\tVersion 0.0.1 beta, 1/15/2020")
    print("Usage:\n\tqeda [flags and input files in any order]")
    print("\t -h --help\t\tprints this message")
    print("\t -o --output\t\tset output file")
    print("\t -p --proc\t\tset number of processors (default 1)")
    print("\t -v --verbose\t\tenable verbose mode")
    print("\n\nCopyright 2020 Spooky Manufacturing, LLC")
    sys.exit(0)


def run(inf, outf, proc, verbose, pcb, schema):
    """Runs QEDA"""
    print("Starting QEDA Manager")
    x = QEDAManager(inf, outf, proc, verbose, pcb, schema)
    sys.exit(0)


def main(args=None):
    """The main routine"""
    inf = ""
    outf = ""
    proc = 1
    pcb = True
    schema = True
    verbose = False
    unix_options = "hotcpsi:v"
    gnu_options = ["help", "in=", "output=", "cores=", "pcb=", "schema=", "verbose"]
    print(args)
    if args is None:
        if len(sys.argv) > 1:
            args = sys.argv[1:]
        else:
            help()
    try:
        arguments, vals = getopt.getopt(args, unix_options, gnu_options)
        for arg, val in arguments:
            print(arg, val)
            if arg in ("T", "t", "-T", "-t", "--test"):
                test()
            elif arg in ("H", "h", "-H", "-h", "--help"):
                help()
            elif arg in ("V", "v", "-V", "-v", "--verbose"):
                print("Verbose mode")
                verbose = True
            elif arg in ("O", "o", "-O", "-o", "--out", "--output"):
                outf = val
                print("Output file:", val)
            elif arg in ("P", "p", "-P", "-p", "--pcb"):
                print("Make PCB: ", val)
                pcb = val
            elif arg in ("C", "c", "-c", "-C", "--cores"):
                raise NotImplementedError("Multiprocessing has not yet been implemented.")
                proc = val
            elif arg in ("S", "s", "-S", "-s", "--schema"):
                print("Make Schema", val)
                schema = val
            elif arg in ("i", "I", "in", "IN", "in="):
                print("Setting infile to {}".format(val))
                inf = val
            else:
                print("Setting infile")
                inf = val
        #if inf == 0:
        #    raise Exception("No file specified")
        if outf == 0:
            outf = inf + '.out'
        print(inf, outf)
        run(inf, outf, proc, verbose, pcb, schema)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)


if __name__ == '__main__':
    main()
