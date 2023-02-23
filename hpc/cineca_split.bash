#!/usr/bin/env bash

VCF="OneK1K.noGP.vcf"
cd /home/dlough2/scratch || exit
for sample in `bcftools query -l $VCF`; do
  if [[ -f "./cineca_vcfs/${sample}.vcf.gz" ]]; then
    echo "Skipping $sample (already exists)"
  else
    sbatch "--export=SAMPLE=$sample,VCF=$VCF" /home/dlough2/cineca_split_job.bash
  fi
done
