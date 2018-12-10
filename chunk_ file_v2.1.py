#!/usr/bin/env python

"""
Written by Lucas van der Gouw
31-1-17

This script reads a .fasta file and splits the sequences in user defined sized chunks.
"""

import sys, getopt
from Bio import SeqIO

def command(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:n:m:",["ifile=","ofile=","number=","minimum="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile> -n <number> -m <minimum>'
      sys.exit(2)
   for opt, arg in opts:
    if opt == '-h':
         print 'chunker.py -i <inputfile> -o <outputfile> -n <number> -m <minimum>'
         sys.exit()
    elif opt in ("-i", "--ifile"):
         inputfile = arg
    elif opt in ("-o", "--ofile"):
         outputfile = arg
    if opt in ("-n", "--number"):
        number = int(arg)
    if opt in ("-m", "--minimum"):
        minimum = int(arg)
   return inputfile, outputfile, number, minimum
         
def open_files(inputfile):
    contigs = []
    sequences = []
    for record in SeqIO.parse(inputfile, "fasta"):
        contigs.append(record.id)
        sequences.append(record.seq)
    return sequences, contigs
    
def chunk_content(sequences, number, minimum, contigs):
    contignumber = 0 
    chunk_string = ""
    chunknumber = 1
    for contig in contigs:
        if len(sequences[contignumber]) < minimum:
            chunknumber += 1
        elif len(sequences[contignumber]) >= minimum:
            while sequences[contignumber]:
                if len(sequences[contignumber][:number]) >= minimum:
                    chunk_string += ">" + str(contigs[contignumber]) + "_chunk" + str(chunknumber) + "\n" + (sequences[contignumber][:number]) + "\n"
                    chunknumber += 1 
                sequences[contignumber] = sequences[contignumber][number:]
        contignumber += 1                  
    return chunk_string
  
def write_file(outfile, chunk_string):
    write_file = open(outfile, "w")
    write_file.write(str(chunk_string))
    write_file.close
        
def main(argv):
    inputfile, outfile, number, minimum = command(argv)
    sequences, contigs = open_files(inputfile)
    chunk_string = chunk_content(sequences, number, minimum, contigs)
    write_file(outfile, chunk_string)
    
if __name__ == "__main__":
   main(sys.argv[1:])
