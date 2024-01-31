import json
import uuid
from pathlib import Path
from typing import Union, List


def s3_event(fixture_name: Union[str | List[str]]):
    file = Path(__file__).parent.parent.joinpath(f'fixtures/{fixture_name}')

    if isinstance(fixture_name, list):
        return {
            "Records": [s3_event(f)["Records"][0] for f in fixture_name],
        }

    return {
        "Records": [
            {
                "eventVersion": "2.0",
                "eventSource": "aws:s3",
                "awsRegion": "eu-west-2",
                "eventTime": "1970-01-01T00:00:00.000Z",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {
                    "principalId": "EXAMPLE"
                },
                "requestParameters": {
                    "sourceIPAddress": "127.0.0.1"
                },
                "responseElements": {
                    "x-amz-request-id": "EXAMPLE123456789",
                    "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "testConfigRule",
                    "bucket": {
                        "name": "test-bucket",
                        "ownerIdentity": {
                            "principalId": "EXAMPLE"
                        },
                        "arn": "arn:aws:s3:::test-bucket"
                    },
                    "object": {
                        "key": fixture_name,
                        "size": file.stat().st_size,
                        "eTag": "0123456789abcdef0123456789abcdef",
                        "sequencer": "0A1B2C3D4E5F678901"
                    }
                }
            }
        ]
    }


def sqs_event(fixture_name):
    return {
        "Records": [
            {
                "messageId": f'{uuid.uuid4()}',
                "receiptHandle": "aogfdgirubeociurbgalierlgbalergnaerhrehah",
                "body": json.dumps(s3_event(fixture_name)),
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1701419332199",
                    "SenderId": "AROA5LVVW55647YN4KVPZ:S3-PROD-END",
                    "ApproximateFirstReceiveTimestamp": "1701419332205"
                },
                "messageAttributes": {},
                "md5OfBody": "2828017fce840863d2b36d3036d9c7c7",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:eu-west-2:12345678910:s3-event-notification-queue",
                "awsRegion": "eu-west-2"
            }
        ]
    }
