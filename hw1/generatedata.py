import random
import sys

def transform(n):
    """
    This function converts an integer between 0 and 3 to
    the corresponding base pair.

    Args:
        n: Integer between 0 and 3.

    Returns:
        base pair A, C, G or T.
    """

    if n == 0:
        return "A"
    if n == 1:
        return "C"
    if n == 2:
        return "G"
    if n == 3:
        return "T"

def generate_random_sequence(seq_len):
    """
    This function generates a random sequence of base pairs 
    with length seq_len.

    Args:
        seq_len: integer that is length of sequence

    Returns:
        String of length seq_len consisting of A, C, G and T.
    """

    sequence = []
    for i in range(seq_len):
        sequence.append(transform(random.randint(0, 3)))
    
    return "".join(sequence)

def generate_read(ref_data, read_len, nalignments):
    """
    This function generates a read of the reference ref_data
    with length read_len and nalignments alignment positions.

    Args:
        ref_data: String describing the reference sequence.
        read_len: Integer equal to length of the read to be generated.
        nalignments: Integer between 0 and 2 equal to the amount of 
        times the read should align with the reference.

    Returns:
        read: String containing the read
    """

    # create read with 0 alignments
    if nalignments == 0:
        while True:
            read = generate_random_sequence(read_len)
            if ref_data.find(read) == -1:
                return read

    # create read with 1 alignment
    if nalignments == 1:
        read_pos = random.randint(0, int(len(ref_data)/2))
        read = ref_data[read_pos:read_pos+read_len]
        return read
    
    #create read with two alignments
    if nalignments == 2:
        read_pos = random.randint(int(0.75*len(ref_data)), len(ref_data)-read_len)
        read = ref_data[read_pos:read_pos+read_len]
        return read

if __name__ == "__main__":
    if len(sys.argv) != 6:
        # not enough arguments, print usage message
        print("Usage:")
        print("$ python3 generatedata.py <ref_length> ", end ="")
        print("<nreads> <read_len> <ref_file> <reads_file>")
        sys.exit(0)
    
    # initialize parameters
    ref_length = int(sys.argv[1])
    nreads = int(sys.argv[2])
    read_len = int(sys.argv[3])
    ref_file = sys.argv[4]
    reads_file = sys.argv[5]

    # print parameters
    print("reference length: {}".format(ref_length))
    print("number reads: {}".format(nreads))
    print("read length: {}".format(read_len))

    # generate reference data
    ref_data = generate_random_sequence(int(0.75*ref_length))
    ref_data += ref_data[int(ref_length/2):]

    # generate reads
    reads = []
    nalign = [0] * 3
    for i in range(nreads):

        # random number determines amount of alignments
        u = random.random()

        # generate read with 0 alignments
        if u < 0.15:
            reads.append(generate_read(ref_data, read_len, 0))
            nalign[0] += 1

        # generate read with 1 alignments
        elif u < 0.9:
            reads.append(generate_read(ref_data, read_len, 1))
            nalign[1] += 1

        # generate read with 2 alignments
        else:
            reads.append(generate_read(ref_data, read_len, 2))
            nalign[2] += 1
    
    # print alignment distribution of reads
    print("aligns 0: {}".format(nalign[0]/nreads))
    print("aligns 1: {}".format(nalign[1]/nreads))
    print("aligns 2: {}".format(nalign[2]/nreads))

    # write reference data to file
    file = open(ref_file, "w")
    file.write(ref_data+"\n")
    file.close()

    # write reads to file
    file = open(reads_file, "w")
    for read in reads:
        file.write(read+"\n")
    file.close()
