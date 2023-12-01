from typing import Literal


def scan_object(bucket: str, key: str) -> Literal['NOT_INFECTED', 'INFECTED', None]:
    if key.endswith('.jpeg'):
        return 'NOT_INFECTED'

    if key.endswith('.png'):
        return 'INFECTED'

    return None
