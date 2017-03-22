#!/usr/bin/python3
import time
import os
__author__ = 'adamkoziol, paulmanninger'


class Centrifuge(object):

    def runner(self):
        """
        Runs the appropriate methods in the appropriate order. Appropriately.
        """
        # Run the fastq finding method
        self.findfastq()
        #
        self.runcentrifuge()

    def findfastq(self):
        """
        Creates lists of .fastq files to be entered in to the centrifuge system call
        """
        from glob import glob
        self.forwardfastq = ','.join(sorted(glob('{}*R1*.gz'.format(self.sequencepath))))
        self.reversefastq = ','.join(sorted(glob('{}*R2*.gz'.format(self.sequencepath))))

    def runcentrifuge(self):
        self.basename = 'placeholder'
        self.outputfile = 'placeholder'
        centrifugecall = 'centrifuge -x {} -1 {} -2 {} -S {}'\
            .format(self.basename, self.forwardfastq, self.reversefastq, self.outputfile)
        print (centrifugecall)

    def __init__(self, args, startingtime):
        """
        :param args: command line arguments
        :param startingtime: time the script was started
        """
        import multiprocessing
        # Initialise variables
        self.start = startingtime
        # Define variables based on supplied arguments
        self.path = os.path.join(args.path, '')
        assert os.path.isdir(self.path), u'Supplied path is not a valid directory {0!r:s}'.format(self.path)
        self.sequencepath = os.path.join(args.sequencepath, '')
        assert os.path.isdir(self.sequencepath), u'Sequence path  is not a valid directory {0!r:s}' \
            .format(self.sequencepath)
        self.databasepath = os.path.join(args.databasepath, '')
        self.reportpath = os.path.join(self.path, 'reports')
        assert os.path.isdir(self.databasepath), u'Target path is not a valid directory {0!r:s}' \
            .format(self.databasepath)
        # Use the argument for the number of threads to use, or default to the number of cpus in the system
        self.cpus = int(args.numthreads if args.numthreads else multiprocessing.cpu_count())
        #
        self.forwardfastq = str()
        self.reversefastq = str()
        self.basename = str()
        self.outputfile = str()
        self.devnull = open(os.devnull, 'wb')
        # Run the analyses
        self.runner()


if __name__ == '__main__':
    # Argument parser for user-inputted values, and a nifty help menu
    from argparse import ArgumentParser
    # Parser for arguments
    parser = ArgumentParser(description='Automates centrifuge metagenomics program')
    parser.add_argument('path',
                        help='Specify input directory')
    parser.add_argument('-s', '--sequencepath',
                        required=True,
                        help='Path of .fastq(.gz) files to process.')
    parser.add_argument('-d', '--databasepath',
                        required=True,
                        help='Path of database files to use.')
    parser.add_argument('-n', '--numthreads',
                        help='Number of threads. Default is the number of cores in the system')
    # Get the arguments into an object
    arguments = parser.parse_args()

    # Define the start time
    start = time.time()

    # Run the script
    Centrifuge(arguments, start)

    # Print a bold, green exit statement
    print ('\033[92m' + '\033[1m' + "\nElapsed Time: %0.2f seconds" % (time.time() - start) + '\033[0m')
