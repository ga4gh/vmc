import logging

_logger = logging.getLogger(__name__)


def pjs_filter(yaml_dict):
    for message_name, message_definition in yaml_dict['definitions'].items():
        if 'anyOf' in message_definition:
            _logger.warning(f'Removing anyOf attribute from {message_name} to avoid pjs error.')
            del message_definition['anyOf']
        if 'allOf' in message_definition:
            _logger.warning(f'Removing allOf attribute from {message_name} to avoid pjs error.')
            del message_definition['allOf']
    return yaml_dict
