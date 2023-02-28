#!/usr/bin/python

"""
Create CINECA experiments JSON from the WP4 runs.json.

Parameters:
     filename: Path to the WP4 runs.json

Output:
    The experiments JSON file ready to be parsed by Katsu

Example run command:
    python generate_experiments_json.py ./runs.json



"""

import sys
import json
from datetime import datetime



exp_meta_file = 'experiment_metadata.json'
ontologies_desc_file = 'ontologies.json'


# The JSON objects contains 2 arrays: the list of experiments and the list of ontologies used to describe these
# experiments.
output = {
    'experiments': [],
    'resources': []
}


def main(argv):
    #Load individual and biosamples JSON to be merged
    runs_input_filename = argv[0]
    print("Reading", runs_input_filename)
    runs_input_file = open(runs_input_filename)
    runs_json = json.load(runs_input_file)

    print("Importing experiments metadata from", exp_meta_file)
    f = open(exp_meta_file)
    expmeta = json.load(f)

    print("Importing ontologies descriptors from", ontologies_desc_file)
    f2 = open(ontologies_desc_file)
    ontologies_desc = json.load(f2)
    output['resources'].append(ontologies_desc["OBI"])
    output['resources'].append(ontologies_desc["EFO"])


    for run in runs_json:
        #Prepare additional metadata that's not in the original runs.json
        ref_exp_metadata = expmeta[run["libraryStrategy"]]

        experiment = {
            "id": run['id'],
            "study_type": ref_exp_metadata["study_type"],
            "experiment_type": ref_exp_metadata["experiment_type"],
            "experiment_ontology": ref_exp_metadata["experiment_ontology"],
            "molecule": ref_exp_metadata["molecule"],
            "library_strategy": ref_exp_metadata["library_strategy"],
            "library_source": ref_exp_metadata["library_source"],
            "library_selection": run["librarySelection"].capitalize(),
            "library_layout": run["libraryLayout"].capitalize(),
            "biosample": run['biosampleId'],
            "instrument": {
                "identifier": "unknown",
                "platform": run["platform"],
                "description": run["platform"],
                "model": run["platformModel"]["label"]
            },
            "extra_properties": {
                "run_date": run["runDate"]
            }
        }

        if run["libraryStrategy"] == "Genotyping microarray":
            experiment["experiment_results"] = [
                {
                    "identifier": run['biosampleId'] + "_vcf",
                    "creation_date": datetime.now().isoformat(),
                    "created_by": "C3G",
                    "extra_properties": {
                        "target": "Unknown"
                    },
                    "description": "VCF file",
                    "filename": run['biosampleId'] + ".vcf.gz",
                    "file_format": "VCF",
                    "data_output_type": "Derived data",
                    "usage": "Downloaded"
                }
            ]

        output['experiments'].append(experiment)


    today = datetime.today().strftime('%Y-%m-%d')
    with open('experiments_cineca_%s.json' % today, 'w') as f:
        json.dump(output, f, indent=2)


if __name__ == "__main__":
    main(sys.argv[1:])
