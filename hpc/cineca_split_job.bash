#!/bin/bash
#SBATCH --mem=1G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=2:00:00
#SBATCH --account=rrg-bourqueg-ad

mkdir -p cineca_vcfs

# -c1 requires a minimum of 1 non-ref allele

module load bcftools
bcftools view -c1 -Oz -s "$SAMPLE" -o "./cineca_vcfs/${SAMPLE}.vcf.gz" "$VCF"
