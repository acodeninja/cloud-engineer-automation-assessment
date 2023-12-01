from datetime import date

import boto3
import pytest

from object_scanner import object_scanner, EVENT_TYPE
from tests.doubles.aws_context import AWSLambdaContext
from tests.doubles.aws_events import s3_event, sqs_event

EVENTS = {
    'S3': s3_event,
    'SQS': sqs_event,
}


@pytest.mark.parametrize("key,tag_value",
                         [
                             ('liberty.jpeg', 'clean'),
                             ('poem.txt', None),
                             ('flame.png', 'infected'),
                         ])
def test_object_retain_object_type_tag(key, tag_value):
    object_scanner(EVENTS[EVENT_TYPE](key), AWSLambdaContext)

    tags = get_s3_object_tags('test-bucket', key)

    assert tags.get('ObjectType') == 'user-id-upload'


@pytest.mark.parametrize("key,tag_value",
                         [
                             ('liberty.jpeg', 'clean'),
                             ('poem.txt', None),
                             ('flame.png', 'infected'),
                         ])
def test_object_is_tagged_with_scan_state_tag(key, tag_value):
    object_scanner(EVENTS[EVENT_TYPE](key), AWSLambdaContext)

    tags = get_s3_object_tags('test-bucket', key)

    assert tags.get('ScanState') == tag_value


@pytest.mark.parametrize("key",
                         [
                             ('liberty.jpeg'),
                             ('poem.txt'),
                             ('flame.png'),
                         ])
def test_object_is_tagged_with_scan_date_tag(key):
    object_scanner(EVENTS[EVENT_TYPE](key), AWSLambdaContext)

    tags = get_s3_object_tags('test-bucket', key)

    assert tags.get('ScanDate') == date.today().isoformat()


def get_s3_object_tags(bucket: str, key: str):
    s3_client = boto3.client('s3')
    response = s3_client.get_object_tagging(Bucket=bucket, Key=key)

    return {tag['Key']: tag['Value'] for tag in response['TagSet']}
