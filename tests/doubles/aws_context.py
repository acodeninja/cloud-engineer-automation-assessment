import uuid


class AWSLambdaContext:
    function_name: str = 'object-scanner'
    function_version: str = '3'
    invoked_function_arn: str = 'arn:aws:lambda:eu-west-2:123456789012:function:object-scanner:3'
    memory_limit_in_mb: int = 128
    aws_request_id: str = f'{uuid.uuid4()}'
    log_group_name: str = '/aws/lambda/object-scanner'
    log_stream_name: str = f'/{uuid.uuid4()}'

    @classmethod
    def get_remaining_time_in_millis(cls):
        return 3000
