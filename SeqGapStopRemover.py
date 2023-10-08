#!/usr/bin/env python3
"""
SeqGapStopRemover.py: A script to remove gaps and stop codons from FASTA sequences.
It can be run on a single file or on multiple files in a directory.

Options:
  --loop        Run the script on multiple fasta files in a directory.
  --prefix      Use the original filename as a prefix for the output file (only with --loop).
  --output_dir  Specify the directory to save output files (only with --loop).
  --threads     Number of threads for parallel processing (only with --loop).

Usage:
  Single file:  python SeqGapStopRemover.py input.fasta > output.fasta
  Multiple files: python SeqGapStopRemover.py --loop input_directory/

Run `python SeqGapStopRemover.py -h` for more details.
"""

import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor

def show_help():
    help_text = '''Usage: python SeqGapStopRemover.py [OPTIONS] <input_file_or_directory>
    
Options:
    --loop        Run the script on multiple files in the specified directory.
    --prefix      Use the original file name as a prefix for the output file (only works with --loop).
    --output_dir  Specify the directory where output files will be saved (only works with --loop).
    --threads     Number of threads to use for parallel processing (only works with --loop).

Examples:
    Single file:  python SeqGapStopRemover.py inputfilename.fasta > outputfilename.fasta
    Multiple files without prefix:  python SeqGapStopRemover.py --loop input_directory/
    Multiple files with prefix:  python SeqGapStopRemover.py --loop --prefix input_directory/
    '''
    print(help_text)
    print("For further help============>>>>>>>>>>>> shoot a message Aqib.")

def is_fasta(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        return first_line.startswith(">")

if '-h' in sys.argv or '--help' in sys.argv:
    show_help()
    sys.exit(0)

def remove_gaps_and_stop_codons_from_fasta(input_file, output_file=None):
    stop_codons = {"TAA", "TGA", "TAG"}
    
    with open(input_file, 'r') as infile:
        sequence = []
        header = None

        if output_file:
            outfile = open(output_file, 'w')
            close_outfile = True
        else:
            outfile = sys.stdout
            close_outfile = False

        try:
            for line in infile:
                line = line.strip()
                if line.startswith(">"):
                    if header is not None:
                        seq_str = ''.join(sequence).replace("-", "")
                        if seq_str[-3:] in stop_codons:
                            seq_str = seq_str[:-3]
                        outfile.write(f"{header}\n{seq_str}\n")
                    header = line
                    sequence = []
                else:
                    sequence.append(line)

            if header is not None:
                seq_str = ''.join(sequence).replace("-", "")
                if seq_str[-3:] in stop_codons:
                    seq_str = seq_str[:-3]
                outfile.write(f"{header}\n{seq_str}\n")

        finally:
            if close_outfile:
                outfile.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("input_path", help="Input file or directory path")
    parser.add_argument("--loop", action="store_true", help="Run the script on multiple files in the specified directory")
    parser.add_argument("--prefix", action="store_true", help="Use the original file name as a prefix for the output file (only works with --loop)")
    parser.add_argument("--output_dir", help="Specify the directory where output files will be saved (only works with --loop)")
    parser.add_argument("--threads", type=int, default=1, help="Number of threads to use for parallel processing (only works with --loop)")

    args = parser.parse_args()

    if args.output_dir and not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    def process_file(fasta_file):
        input_file = os.path.join(args.input_path, fasta_file)
        output_file = None
        if args.output_dir:
            if args.prefix:
                output_file = os.path.join(args.output_dir, f"{os.path.splitext(fasta_file)[0]}_output.fasta")
            else:
                output_file = os.path.join(args.output_dir, fasta_file)
        else:
            if args.prefix:
                output_file = os.path.join(args.input_path, f"{os.path.splitext(fasta_file)[0]}_output.fasta")
            else:
                output_file = os.path.join(args.input_path, fasta_file)
        remove_gaps_and_stop_codons_from_fasta(input_file, output_file)

    if args.loop:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            all_files = [f for f in os.listdir(args.input_path) if os.path.isfile(os.path.join(args.input_path, f))]
            fasta_files = [f for f in all_files if is_fasta(os.path.join(args.input_path, f))]
            executor.map(process_file, fasta_files)
    else:
        remove_gaps_and_stop_codons_from_fasta(args.input_path)

    if args.loop or (not args.loop and sys.stdout.isatty()):
        print("AJG4U======>>>>>>>>>>>>Process completed successfully!: Wishes from Aqib.")
