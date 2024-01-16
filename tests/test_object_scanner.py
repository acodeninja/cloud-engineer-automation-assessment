from datetime import date
from unittest.mock import patch

import boto3
import pytest

from object_scanner import object_scanner, EVENT_TYPE
from object_scanner.scan import scan_object
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
def test_object_is_tagged_with_scan_state_tag(key, tag_value):
    object_scanner(EVENTS[EVENT_TYPE](key), AWSLambdaContext)

    tags = get_s3_object_tags('test-bucket', key)

    assert tags.get('ScanState') == tag_value


@pytest.mark.parametrize("key",
                         [
                             'liberty.jpeg',
                             'poem.txt',
                             'flame.png',
                         ])
def test_object_is_tagged_with_scan_date_tag(key):
    object_scanner(EVENTS[EVENT_TYPE](key), AWSLambdaContext)

    tags = get_s3_object_tags('test-bucket', key)

    assert tags.get('ScanDate') == date.today().isoformat()


@pytest.mark.parametrize("key",
                         [
                             'liberty.jpeg',
                             'poem.txt',
                             'flame.png',
                         ])
@patch('object_scanner.object_scanner.scan_object', wraps=scan_object)
def test_scan_object_is_called_with_expected_objects(scan_object_patch, key):
    object_scanner(EVENTS[EVENT_TYPE](key), AWSLambdaContext)

    scan_object_patch.assert_called_with('test-bucket', key)


def get_s3_object_tags(bucket: str, key: str):
    s3_client = boto3.client('s3')
    response = s3_client.get_object_tagging(Bucket=bucket, Key=key)

    return {tag['Key']: tag['Value'] for tag in response['TagSet']}


@pytest.mark.parametrize("key",
                         [
                             'liberty.jpeg',
                             'poem.txt',
                             'flame.png',
                         ])
def test_object_retains_existing_tags(key, tag_value):
    """
    Write a test that ensures scanned objects retain existing tags.
    All objects should retain the tag "ObjectType: user-id-upload".
    """
    raise NotImplementedError()
