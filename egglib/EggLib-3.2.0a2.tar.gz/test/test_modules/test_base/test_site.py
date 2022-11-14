import os, egglib, unittest
path = os.path.dirname(__file__)

class Site_test(unittest.TestCase):
    def test_modifs(self):
        aln = egglib.io.from_fasta(os.path.join(path, '..', 'test_stats', 'control_stats', 'dmi1.fas'),
                        alphabet=egglib.alphabets.DNA, labels=True)

        site = egglib.site_from_align(aln, 690)
        siteL = site.as_list()

        self.assertEqual(site[12], siteL[12])

        siteL[1] = 'A'
        del siteL[5]
        siteL.insert(len(siteL), '-')
        siteL.extend('GTA')

        with self.assertRaises(ValueError):
            site[1] = 'Z'

        site[1] = 'A'
        self.assertEqual(site[1], 'A')

        del site[5]
        site.append('-')
        site.extend('GTA')
        self.assertListEqual(site.as_list(), siteL)

    def test_from_vcf(self):

        # VCF example file found at:
        VCF_header = '''##fileformat=VCFv4.0
##fileDate=20090805
##source=myImputationProgramV3.1
##reference=1000GenomesPilot-NCBI36
##phasing=partial
##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of Samples With Data">
##INFO=<ID=AN,Number=1,Type=Integer,Description="Total number of alleles in called genotypes">
##INFO=<ID=AC,Number=.,Type=Integer,Description="Allele count in genotypes, for each ALT allele, in the same order as listed">
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
##INFO=<ID=AF,Number=.,Type=Float,Description="Allele Frequency">
##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele">
##INFO=<ID=DB,Number=0,Type=Flag,Description="dbSNP membership, build 129">
##INFO=<ID=H2,Number=0,Type=Flag,Description="HapMap2 membership">
##FILTER=<ID=q10,Description="Quality below 10">
##FILTER=<ID=s50,Description="Less than 50% of samples have data">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
##FORMAT=<ID=HQ,Number=2,Type=Integer,Description="Haplotype Quality">
##ALT=<ID=DEL-ME-ALU,Description="Deletion of ALU element">
##ALT=<ID=CNV,Description="Copy number variable region">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	NA00001	NA00002	NA00003'''

        VCF_lines = [
            '19	111	.	A	C	9.6	.	.	GT:HQ	0|0:10,10	0|0:10,10	0/1:3,3',
            '19	112	.	A	G	10	.	.	GT:HQ	0|0:10,10	0|0:10,10	0/1:3,3',
            '20	14370	rs6054257	G	A	29	PASS	NS=3;DP=14;AF=0.5;DB;H2	GT:GQ:DP:HQ	0|0:48:1:51,51	1|0:48:8:51,51	1/1:43:5:.,.',
            '20	17330	.	T	A	3	q10	NS=3;DP=11;AF=0.017	GT:GQ:DP:HQ	0|0:49:3:58,50	0|1:3:5:65,3	0/0:41:3:.,.',
            '20	1110696	rs6040355	A	G,T	67	PASS	NS=2;DP=10;AF=0.333,0.667;AA=T;DB	GT:GQ:DP:HQ	1|2:21:6:23,27	2|1:2:0:18,2	2/2:35:4:.,.',
            '20	1230237	.	T	.	47	PASS	NS=3;DP=13;AA=T	GT:GQ:DP:HQ	0|0:54:.:56,60	0|0:48:4:51,51	0/0:61:2:.,.',
            '20	1234567	microsat1	G	GA,GAC	50	PASS	NS=3;DP=9;AA=G;AN=6;AC=3,1	GT:GQ:DP	0/1:.:4	0/2:17:2	1/1:40:3',
            '20	1235237	.	T	.	.	.	.	GT	0/0	0|0	./.',
            'X	10	rsTest	AC	A,ATG	10	PASS	.	GT	0	0/1	0|2']

        VCF_ctrl = [
            ['A', 'A', 'A', 'A', 'A', 'C'],
            ['A', 'A', 'A', 'A', 'A', 'G'],
            ['G', 'G', 'A', 'G', 'A', 'A'],
            ['T', 'T', 'T', 'A', 'T', 'T'],
            ['G', 'T', 'T', 'G', 'T', 'T'],
            ['T', 'T', 'T', 'T', 'T', 'T'],
            ['G', 'GA', 'G', 'GAC', 'GA', 'GA'],
            ['T', 'T', 'T', 'T', '?', '?'],
            ['AC', 'AC', 'AC', 'A', 'AC', 'ATG']]

        vcf = egglib.io.VcfStringParser(VCF_header)
        for line, ctrl in zip(VCF_lines, VCF_ctrl):
            vcf.readline(line)
            site = vcf.get_genotypes()
            self.assertListEqual(site.as_list(), ctrl)

            site = egglib.site_from_vcf(vcf)
            self.assertListEqual(site.as_list(), ctrl)

            site = egglib.site_from_vcf(vcf, 1, None)
            self.assertListEqual(site.as_list(), ctrl[2:])

            site = egglib.site_from_vcf(vcf, 0, 2)
            self.assertListEqual(site.as_list(), ctrl[:4])

        site = egglib.Site()
        for line, ctrl in zip(VCF_lines, VCF_ctrl):
            vcf.readline(line)
            site.from_vcf(vcf)
            self.assertListEqual(site.as_list(), ctrl)

            site.from_vcf(vcf, 1, None)
            self.assertListEqual(site.as_list(), ctrl[2:])

            site.from_vcf(vcf, 0, 2)
            self.assertListEqual(site.as_list(), ctrl[:4])
