# python lambda_async_s3_uri.py 'https://www.encodeproject.org/search/?searchTerm=H3K4ME3&type=Experiment&replication_type=isogenic&assembly=GRCh38&award.rfa=ENCODE4&format=json'

import json
import multiprocessing
import os
import re
import subprocess
import sys
import time
from itertools import combinations_with_replacement

import boto3
import pandas as pd
from dotenv import load_dotenv

from .s3_uri import fetch_encsr_encff, set_globals

load_dotenv()


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r"(\d+)", text)]


def format(args):
    bed_paths, bed_labels = fetch_encsr_encff(args)
    bed_files_nsort = []

    for i in range(len(bed_paths)):
        bed_files_nsort.append(bed_paths[i][-18:])

    # natural sort of bed files
    bed_files_nsort.sort(key=natural_keys)

    # generating unique pairs of bed files to correlate
    bed_pairs = list(combinations_with_replacement(bed_paths, 2))

    num_bed_pairs = len(bed_pairs)

    bed_formatted = []

    for bed_pair in bed_pairs:
        file1 = bed_pair[0][19:]
        file2 = bed_pair[1][19:]
        f_name1 = file1[-18:]
        f_name2 = file2[-18:]
        label1 = ""
        label2 = ""
        for bed_label in bed_labels:
            if f_name1 == bed_label[:18]:
                label1 = bed_label
            if f_name2 == bed_label[:18]:
                label2 = bed_label
        whole_label = (
            '{"file1": "'
            + file1
            + '", "file2": "'
            + file2
            + '", "label1": "'
            + label1
            + '", "label2": "'
            + label2
            + '"}'
        )
        print(whole_label)
        bed_formatted.append(whole_label)

    return bed_formatted, num_bed_pairs, bed_files_nsort, bed_labels


def asyncInvokeLambda(payload):
    client = boto3.client("lambda")
    response = client.invoke(
        FunctionName=os.getenv("JACCARD3"),
        InvocationType="Event",
        LogType="None",
        Payload=payload
        # Qualifier='$LATEST'
    )

    return response


def poll1():
    # Get the service resource
    sqs = boto3.resource("sqs")
    message_one = ""

    queue = sqs.get_queue_by_name(QueueName="jaccard3-success")

    for message in queue.receive_messages():
        message_one = json.loads(message.body)
        # message.delete()

    """
    if type(message_one) == str and message_one != "":
        print("aws lambda response")
        print(message_one)
    """

    print("aws lambda response")
    print(message_one)
    print(type(message_one))

    return message_one


def poll_all(num_bed_pairs):
    messages = []
    processed = []

    for x in range(num_bed_pairs):
        message_recv = poll1()
        if isinstance(message_recv, dict):
            messages.append(message_recv)

    for x in range(len(messages)):
        processed.append(messages[x]["responsePayload"])

    print(processed)
    print(len(processed))

    return processed


def bigbed_data(bigbed_labels, experiment_name):
    data = pd.read_csv("output.csv", sep="\t")
    bigbed_files = []
    table_values = []
    corr_value = 1.0

    for i in range(len(bigbed_labels)):
        bigbed_files.append(str.split(bigbed_labels[i], ".")[0])

    print("BIG BED FILES")
    print(bigbed_files)
    print("END")

    for k in range(len(bigbed_labels)):
        dataDict = dict(
            experiment_name=experiment_name,
            row_num=k,
            col_num=k,
            row_label=bigbed_labels[k],
            col_label=bigbed_labels[k],
            corr_value=corr_value,
        )
        print("data dict alert mod")
        print(dataDict)
        print("end")
        table_values.append(dataDict)

    for index, row in data.iterrows():
        row_label = row["id1"]
        print("row label")
        print(row_label)
        col_label = row["id2"]
        print("col label")
        print(col_label)
        corr_value = row["jaccard"]

        for i in range(len(bigbed_labels)):
            if row_label == str.split(bigbed_labels[i], ".")[0]:
                row_label = bigbed_labels[i]
                row_num = i
                print("ROW NUM")
                print(row_num)
                break

        for j in range(len(bigbed_labels)):
            if col_label == str.split(bigbed_labels[j], ".")[0]:
                col_label = bigbed_labels[j]
                col_num = j
                print("COL NUM")
                print(col_num)
                break

        dataDict = dict(
            experiment_name=experiment_name,
            row_num=row_num,
            col_num=col_num,
            row_label=row_label,
            col_label=col_label,
            corr_value=corr_value,
        )

        # dataDict = [experiment_name, row_num, col_num, row_label, col_label, corr_value]
        table_values.append(dataDict)
        if row_label != col_label:
            temp_label = row_label
            row_label = col_label
            col_label = temp_label
            temp_num = row_num
            row_num = col_num
            col_num = temp_num
            dataDictFlipped = dict(
                experiment_name=experiment_name,
                row_num=row_num,
                col_num=col_num,
                row_label=row_label,
                col_label=col_label,
                corr_value=corr_value,
            )
            table_values.append(dataDictFlipped)
        else:
            pass
            # not_duplicated.append(dataDict)

    return table_values


def filter_complete(args):
    start_time = time.time()
    processes = []
    table_values = []
    not_duplicated = []
    assembly = args[2]
    outputType = args[3]
    fileType = args[4]
    set_globals(assembly, outputType, fileType)
    payload_formatted, num_bed_pairs, bed_files_nsort, bed_labels = format(args[0])
    experiment_name = args[1]

    if fileType == "bed":
        for payload in payload_formatted:
            p = multiprocessing.Process(target=asyncInvokeLambda, args=(payload,))
            processes.append(p)
            p.start()

        for process in processes:
            process.join()

        print(
            "All AWS Lambda Asynchrous Invocations Triggered --- %.2f seconds ---"
            % (time.time() - start_time)
        )

        processFurther = poll_all(num_bed_pairs)

        for i in range(len(processFurther)):
            dataInter = processFurther[i]["score"]
            row_label = dataInter.split("'")[1]
            col_label = dataInter.split("'")[3]
            for i in range(len(bed_files_nsort)):
                if row_label[:18] == bed_files_nsort[i]:
                    row_num = i
                    break
            for j in range(len(bed_files_nsort)):
                if col_label[:18] == bed_files_nsort[j]:
                    col_num = j
                    break
            corr_value = dataInter.split(": ")[-1][:-1]
            dataDict = dict(
                experiment_name=experiment_name,
                row_num=row_num,
                col_num=col_num,
                row_label=row_label,
                col_label=col_label,
                corr_value=corr_value,
            )
            # dataDict = [experiment_name, row_num, col_num, row_label, col_label, corr_value]
            table_values.append(dataDict)
            if row_label != col_label:
                temp_label = row_label
                row_label = col_label
                col_label = temp_label
                temp_num = row_num
                row_num = col_num
                col_num = temp_num
                dataDictFlipped = dict(
                    experiment_name=experiment_name,
                    row_num=row_num,
                    col_num=col_num,
                    row_label=row_label,
                    col_label=col_label,
                    corr_value=corr_value,
                )
                table_values.append(dataDictFlipped)
            else:
                not_duplicated.append(dataDict)

        print(table_values)
        print(len(table_values))

        return table_values

    else:
        # assuming files are bigBed
        bash_command = "../../bigbed-jaccard/target/release/bigbed-jaccard-similarity-matrix input.txt output.csv"
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        process.communicate()
        print("BIG BED FORK REACHED")

        # to avoid confusion, a new variable bigBed labels is created as in this case bigBed files are being used
        # so these really are bigBed labels (and not bed labels) in this instance
        bigbed_labels = bed_labels

        table_values = bigbed_data(bigbed_labels, experiment_name)
        print(table_values)
        print(len(table_values))

        return table_values


def main(args):
    start_time = time.time()
    filter_complete(args)
    print("Total time --- %.2f seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main(sys.argv[1:])
