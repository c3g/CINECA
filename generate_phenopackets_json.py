#!/usr/bin/python

"""
Merge CINECA OneK1K individual and biosample files into a Phenopackets v1 document.

Parameters:
     individuals_input_file: Path to the CINECA WP4 individuals JSON document.
     biosamples_input_file: Path to the CINECA WP4 biosamples JSON document.

Output:
    The Phenopackets JSON file ready to be parsed by Katsu.

Example run command:
    python generate_phenopackets_json.py ./individuals.json ./biosamples.json



"""

import sys
import json
from datetime import datetime


def main(argv):
    #Load individual and biosamples JSON to be merged
    individuals_input_file = open(argv[0])
    biosamples_input_file = open(argv[1])
    individual_json = json.load(individuals_input_file)
    sample_json = json.load(biosamples_input_file)

    #Create a dictionary to quickly find an individual when looping on biosamples
    individual_dict = {x['id']:x for x in individual_json}

    #Loop on all biosamples and add biosample object to the right individual
    for i in sample_json:
        individual_id = i['individualId']
        if individual_id in individual_dict:
            phenopacket = individual_dict[i['individualId']]

            phenopacket["subject"] = {
                "id": individual_id,
                "sex": phenopacket.pop("sex")["label"].upper()
            }

            phenopacket["biosamples"] = [
                {
                    "id": i["id"],
                    "individual_id": individual_id,
                    "sampled_tissue": {
                        "id": i["sampleOriginType"]["id"],
                        "label": i["sampleOriginType"]["label"],
                    },
                    "procedure": {
                        "code": {
                            "id": i["biosampleStatus"]["id"],
                            "label": i["biosampleStatus"]["label"],
                        }
                    },
                    "taxonomy": {
                        "id": "http://purl.obolibrary.org/obo/NCBITaxon_9606",
                        "label": "Homo sapiens"
                    }
                }
            ]


    # Add meta-information on each Phenopackets
    metadata = {
        "phenopacket_schema_version": "1.0.0-RC3",
        "created_by": "Canadian Centre for Computational Genomics",
        "submitted_by": "Canadian Centre for Computational Genomics",
        "resources": []
    }

    for i in individual_dict.keys():
        phenopacket = individual_dict[i]
        phenopacket["meta_data"] = metadata

        phenopacket["subject"]["extra_properties"] = {}
        if "measures" in phenopacket:
            for j in phenopacket["measures"]:
                measure_name = j["assayCode"]["label"]
                measure_value = j["measurementValue"]["quantity"]["value"]
                phenopacket["subject"]["extra_properties"][measure_name] = measure_value

            #Remove the old mesures object, until we can use measurements in Phenopackets v2
            phenopacket.pop("measures")




    final_json = [individual_dict[x] for x in individual_dict.keys()]

    today = datetime.today().strftime('%Y-%m-%d')
    with open('phenopackets_cineca_%s.json' % today, 'w') as f:
        json.dump(final_json, f, indent=2)


if __name__ == "__main__":
    main(sys.argv[1:])
