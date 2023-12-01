# Cloud Engineer Automation Test

## Setup

```shell
git clone https://github.com/acodeninja/pairing-interview-tagging-function.git
cd pairing-interview-tagging-function
pip install poetry
poetry install
```

## Completing the assignment

The file [object_scanner.py](./object_scanner/object_scanner.py) contains the skeleton lambda function you are expected to implement.

```python
from object_scanner.scan import scan_object

EVENT_TYPE = None


def object_scanner(event, context):
   scan_response = scan_object('bucket-name', 'object-key')
```

1. Ensure your environment is set up by running (this will fail at first):
    ```shell
    poetry run pytest
    ```
2. Decide on the event type your function is going to accept, and set `EVENT_TYPE` in [object_scanner.py](./object_scanner/object_scanner.py).
    - S3 Event `EVENT_TYPE = 'S3'`
    - SQS Event `EVENT_TYPE = 'SQS'`
3. Implement a lambda function in [object_scanner.py](./object_scanner/object_scanner.py) that calls `scan_object` with the S3 object's bucket name and object key, then applies tags with the following rules:
    - All objects must be tagged with `ScanDate` set to today's date in ISO format.
    - If `scan_object` returns `NOT_INFECTED` tag the S3 object with `ScanState: clean`.
    - If `scan_object` returns `INFECTED` tag the S3 object with `ScanState: infected`.
    - If `scan_object` returns `None` do not add the `ScanState` tag to the object.
    - Any existing tags on the S3 object must remain.
