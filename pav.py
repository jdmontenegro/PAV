#!/usr/bin/python3

import os
import sys
import pysam
import argparse

# Get the real Path of the script to import the modules
realpath = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(realpath)

import Feature
import GffIO                

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse a sorted bam file and examine gene PAV')
    parser.add_argument('-i', '--inbam', required=True, help='coordinate sorted bam file')
    parser.add_argument('-g', '--gff', required=True, help='gene annotation in gff format')
    parser.add_argument('-mf', '--min_frac', required=False, type=float, default=0.3, help='minimum fraction of gene covered by <min_cov> reads (0.3)')
    parser.add_argument('-mc', '--min_cov', required=True, type=int, default=2, help='minimum coverage per base to be considered covered (2)')
    parser.add_argument('-o', '--out', required=False, default='genes_pav.tsv', help='output table')
    args=parser.parse_args()
    gff = GffIO.GffIO(args.gff)
    samfile = pysam.AlignmentFile(args.inbam, "rb")
    genes = {}
    for gene in gff.nextGene():
        ID = gene.ID
        coords = gene.extractCoords("exon")
        contig = gene.seqid
        genes[ID] = {"tot":0, "pass":0}
        for i in range(len(coords["starts"])):
            region=contig+":"+coords["starts"][i]+"-"+coords["ends"][i]
            for pos in pysam.depth('-aa', '-r', region, args.inbam):
                print(pos)
#                genes[ID]["tot"] += 1
#                depth = pos.split("\t")[2]
#                if depth >= args.min_cov:
#                    genes[ID]["pass"] += 1
#            for column in samfile.pileup(contig, int(coords["starts"][i]), int(coords["ends"][i]), truncate=True):
#                genes[ID]["tot"] += 1
#                if column.nsegments >= args.min_cov:
#                    genes[ID]["pass"] += 1
    log="Analyzed "+str(len(genes))+" genes in file "+args.inbam+"\n"
    print("log")
    samfile.close()
    outfile = open(args.out, "w")
    header = "Gene\tPresence\tPassed\tTotal\n"
    outfile.write(header)
    for gene in genes.keys():
        state = 0
        if genes[gene]["tot"] > 0 and genes[gene]["pass"] / genes[gene]["tot"] >= args.min_frac:
            state = 1
        line = str(gene)+"\t"+str(state)+"\t"+str(genes[gene]["pass"])+"\t"+str(genes[gene]["tot"])+"\n"
        outfile.write(line)
    outfile.close()