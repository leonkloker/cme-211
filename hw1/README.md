CME 211 Homework 1

$ python3 generatedata.py 1000 600 50 "ref_1.txt" "reads_1.txt"
reference length: 1000
number reads: 600
read length: 50
aligns 0: 0.13
aligns 1: 0.7883333333333333
aligns 2: 0.08166666666666667

$ python3 generatedata.py 10000 6000 50 "ref_2.txt" "reads_2.txt"
reference length: 10000
number reads: 6000
read length: 50
aligns 0: 0.14866666666666667
aligns 1: 0.7471666666666666
aligns 2: 0.10416666666666667

$ python3 generatedata.py 100000 60000 50 "ref_3.txt" "reads_3.txt"
reference length: 100000
number reads: 60000
read length: 50
aligns 0: 0.14916666666666667
aligns 1: 0.7517166666666667
aligns 2: 0.09911666666666667

The handwritten test data set should include reads with 0, 1 and 2 alignments
to cover as many different cases as possible. Moreover, all 4 different base
pairs should appear in at least one of the reads. Nevertheless, correct results
on this very small test data set dont immediately imply that the programm
will work in all cases.

As the choice of the amount fo alignments for a read is determined by a 
random number, the underlying distribution is only approximated in the limit
of large amount of reads. Moreover, a read that is supposed to appear only once
could by chance also appear a second time in the reference data. Hence, the
probability for a read to appear twice is slightly higher than expected.

Time spent: 3.5 hours

--------------------------------------

$ python3 processdata.py "ref_1.txt" "reads_1.txt" "align_1.txt"
reference length: 1000
number reads: 600
aligns 0: 0.13
aligns 1: 0.7866666666666666
aligns 2: 0.08333333333333333
elapsed time: 0.0065839290618896484

$ python3 processdata.py "ref_2.txt" "reads_2.txt" "align_2.txt"
reference length: 10000
number reads: 6000
aligns 0: 0.14866666666666667
aligns 1: 0.7471666666666666
aligns 2: 0.10416666666666667
elapsed time: 0.27434825897216797

$ python3 processdata.py "ref_1.txt" "reads_1.txt" "align_1.txt"
reference length: 100000
number reads: 60000
aligns 0: 0.14916666666666667
aligns 1: 0.7516833333333334
aligns 2: 0.09915
elapsed time: 28.01693606376648

As expected, when the data is analyzed with processdata.py the amount of reads
with two alignments is slightly higher than generatedata.py claims and the amount
of reads with one alignment decreases by the same amount. This is due to the fact
that a read appearing in the first 50% of the reference, which is supposed to be a 
single-alignment read, can also randomly appear again in the second part of 
the reference.

The runtime of the program seems to scale quadratically, i.e. O(n^2), when both reads and reference
length n are increased by the same factor simultaneously. As the human genome consists of
3 billion base pairs and we assume a coverage of 30x, i.e. 1.8 billion reads with
length 50, both reference length and amount of reads is 30000x higher than the largest
test data set used. Hence, the runtime scales with 30000^2 which would result in 
roughly 800 years of runtime. Thus, this is approach is obviously not feasible
when trying to analyze the human genome.

Time spent: 1.5 hours
