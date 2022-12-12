import sys
import time

def find_alignments(ref_data, read):
    """
    This function finds the alignment position of read
    in the reference ref_data.

    Args:
        ref_data: String containing the reference sequence.
        read: String containing the read.

    Returns:
        align_pos: List of integers corresponding to the places
        where read aligns with the reference
        Integer equal to the amount of alignments
    """

    align_pos = []
    align_pos.append(ref_data.find(read))

    # when read does not appear return -1
    if align_pos[0] == -1:
        return align_pos, 0
    
    else:
        # check if read aligns twice and return both positions
        align_pos.append(ref_data.find(read, align_pos[0]+1, len(ref_data)))
        if align_pos[1] == -1:
            align_pos.pop()
            return align_pos, 1

        else:
            return align_pos, 2


if __name__ == "__main__":
    if len(sys.argv) != 4:
        # not enough arguments, print usage message
        print("Usage:")
        print("$ python3 generatedata.py <ref_file> ", end ="")
        print("<reads_file> <align_file>")
        sys.exit(0)
    
    # initialize parameters
    ref_filename = sys.argv[1]
    reads_filename = sys.argv[2]
    align_filename = sys.argv[3]
    
    # read reference data from file
    ref_file = open(ref_filename, "r")
    ref_data = ref_file.readline().rstrip()
    ref_file.close()

    # open reads and align file for reading and writing
    reads_file = open(reads_filename, "r")
    align_file = open(align_filename, "w")

    start_time = time.time()

    # iterate through all reads and check how often they align
    naligns = [0] * 3
    for read in reads_file:
        read = read.rstrip()
        if read == "":
            break
        align_pos, nalign = find_alignments(ref_data, read)
        naligns[nalign] += 1

        align_file.write(read + " " + " ".join(map(str,align_pos))+"\n")

    align_file.close()

    end_time = time.time()

    # print the results of the data processing
    print("reference length: {}".format(len(ref_data)))
    print("number reads: {}".format(sum(naligns)))
    print("aligns 0: {}".format(naligns[0]/sum(naligns)))
    print("aligns 1: {}".format(naligns[1]/sum(naligns)))
    print("aligns 2: {}".format(naligns[2]/sum(naligns)))
    print("elapsed time: {}".format(end_time-start_time))
