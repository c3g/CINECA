# CINECA HPC README

## Splitting a multi-sample VCF

**WARNING:** scripts are hard-coded to David L's home directory right now (sorry)

To start jobs on Beluga to split the multi-sample VCF, follow these steps (roughly):

1. Place the scripts in your Beluga home directory and edit any paths to match your username
2. Copy the VCF to your scratch directory and make sure the VCF name is correct in the script
3. From your home directory, run `bash ./cineca_split.bash`. This will submit up to 1000 jobs (one for each sample.)
   You will probably run out of quota for running jobs; wait for all 1000 to finish and then run the script
   again to submit the remaining jobs.
4. VCFs will end up in `scratch/cineca_vcfs`.


## Transferring VCFs to Bento

From the Bento instance, run the following commands:

```bash
source ~/globus-env/bin/activate
cd /data/bento_data/drop-box/data-x/
mkdir -p sample_vcfs
cd sample_vcfs
scp '<beluga username>@beluga.computecanada.ca:/project/rrg-bourqueg-ad/cineca/sample_vcfs/*.vcf.gz' .
```

This will use `scp` to copy all the VCFs to the local directory.
