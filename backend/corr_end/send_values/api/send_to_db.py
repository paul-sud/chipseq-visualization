import boto3

from ..models import Correlations
from .lambda_async_s3_uri import filter_complete


def insert_db(
    url: str, experiment_name: str, assembly: str, output_type: str, file_type: str
) -> None:
    table_values = filter_complete(
        url, experiment_name, assembly, output_type, file_type
    )

    ordered_table_values = sorted(
        table_values, key=lambda i: (i["row_num"], i["col_num"])
    )

    for value_set in ordered_table_values:
        new_value_set = Correlations.objects.create(**value_set)
        new_value_set.save()

    sqs = boto3.client("sqs")
    sqs.purge_queue(
        QueueUrl="https://sqs.us-west-2.amazonaws.com/618537831167/jaccard3-success"
    )
