from typing import List, Tuple

import requests


def sequential_encsr_encff(
    url: str,
    assembly: str = "GRCh38",
    file_type: str = "bed narrowPeak",
    output_type: str = "replicated peaks",
) -> Tuple[List[str], List[str]]:
    file_uris = []
    file_labels = []
    user_search = requests.get(url, allow_redirects=True).json()

    for experiment in user_search["@graph"]:
        for file in experiment["files"]:
            if file["file_type"] == file_type and file["output_type"] == output_type:
                if file["assembly"] == assembly:
                    file_uris.append(file["s3_uri"])
                    file_labels.append(
                        f'{file["accession"]} {experiment["biosample_ontology"]["term_name"]} {experiment["target"]["label"]}'
                    )

    return file_uris, file_labels
