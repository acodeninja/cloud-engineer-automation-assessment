from pathlib import Path

import boto3
import moto
import pytest

from object_scanner import EVENT_TYPE


@pytest.fixture(scope='session', autouse=True)
def check_event_type_selected():
    if not EVENT_TYPE or EVENT_TYPE not in ['S3', 'SQS']:
        raise ValueError('EVENT_TYPE must be set to one of "S3" or "SQS"')


@pytest.fixture(scope='function', autouse=True)
def mock_s3_client():
    with moto.mock_s3():
        s3_client = boto3.client('s3')
        s3_client.create_bucket(
            ACL='private',
            Bucket='test-bucket',
            CreateBucketConfiguration={
                'LocationConstraint': 'eu-west-2',
            },
        )
        for key in ['liberty.jpeg', 'flame.png', 'poem.txt']:
            s3_client.put_object(
                Bucket='test-bucket',
                Key=key,
                Body=Path(__file__).parent.joinpath(f'fixtures/{key}').read_bytes(),
            )
            s3_client.put_object_tagging(
                Bucket='test-bucket',
                Key=key,
                Tagging={
                    'TagSet': [
                        {
                            'Key': 'ObjectType',
                            'Value': 'user-id-upload'
                        },
                    ]
                },
            )
        yield s3_client
