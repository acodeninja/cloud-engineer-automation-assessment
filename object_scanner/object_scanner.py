from object_scanner.scan import scan_object

EVENT_TYPE = 'S3'


def object_scanner(event, context):
    scan_response = scan_object('bucket-name', 'object-key')
