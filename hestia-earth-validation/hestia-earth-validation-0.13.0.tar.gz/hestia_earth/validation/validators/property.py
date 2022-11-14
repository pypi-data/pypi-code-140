from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.lookup import column_name, download_lookup, get_table_value
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import flatten, non_empty_list, safe_parse_float

from .shared import update_error_path, _filter_list_errors, value_difference, _is_value_below


PROPERTIES_KEY = 'properties'
VALUE_TYPE_MATCH = {
    'number': lambda v: not isinstance(v, bool) and (isinstance(v, int) or isinstance(v, float)),
    'boolean': lambda v: isinstance(v, bool)
}


def validate_valueType(node: dict, list_key: str):
    lookup = download_lookup('property.csv')

    def is_valid(values: tuple):
        index, property = values
        term_id = property.get('term', {}).get('@id')
        expected_value_type = get_table_value(lookup, 'termid', term_id, 'valuetype')
        value = property.get('value')
        return value is None or VALUE_TYPE_MATCH.get(expected_value_type, lambda v: True)(value) or {
            'level': 'error',
            'dataPath': f".{PROPERTIES_KEY}[{index}].value",
            'message': f"must be a {expected_value_type}"
        }

    def validate(values: tuple):
        index, blank_node = values
        errors = list(map(is_valid, enumerate(blank_node.get(PROPERTIES_KEY, []))))
        return _filter_list_errors(
            [update_error_path(error, list_key, index) for error in errors if error is not True]
        )

    return _filter_list_errors(flatten(map(validate, enumerate(node.get(list_key, [])))))


def _property_default_value(term_id: str, property_term_id: str):
    # load the term defaultProperties and find the matching property
    term = download_hestia(term_id)
    if not term:
        raise Exception(f"Term not found: {term_id}")
    return safe_parse_float(find_term_match(term.get('defaultProperties', []), property_term_id).get('value'))


def _property_default_allowed_values(term_id: str):
    lookup = download_lookup('property.csv')
    allowed = get_table_value(lookup, 'termid', term_id, column_name('validationAllowedExceptions'))
    try:
        allowed_values = non_empty_list(allowed.split(';')) if allowed else []
        return [safe_parse_float(v) for v in allowed_values]
    # failure to split by `;` as single value allowed
    except AttributeError:
        return [safe_parse_float(allowed)]


def validate_default_value(node: dict, list_key: str):
    threshold = 0.25

    def is_valid(term_id: str):
        def validate(values: tuple):
            index, prop = values
            value = safe_parse_float(prop.get('value'))
            prop_term_id = prop.get('term', {}).get('@id')
            default_value = _property_default_value(term_id, prop_term_id)
            delta = value_difference(value, default_value)
            values_allowed = _property_default_allowed_values(prop_term_id) if prop_term_id else []
            return prop.get('value') is None or delta < threshold or value in values_allowed or {
                'level': 'warning',
                'dataPath': f".{PROPERTIES_KEY}[{index}].value",
                'message': 'should be within percentage of default value',
                'params': {
                    'current': value,
                    'default': default_value,
                    'percentage': delta * 100,
                    'threshold': threshold
                }
            }
        return validate

    def validate(values: tuple):
        index, blank_node = values
        term_id = blank_node.get('term', {}).get('@id')
        errors = list(map(is_valid(term_id), enumerate(blank_node.get(PROPERTIES_KEY, []))))
        return _filter_list_errors(
            [update_error_path(error, list_key, index) for error in errors if error is not True]
        )

    return _filter_list_errors(flatten(map(validate, enumerate(node.get(list_key, [])))))


VSC_ID = 'volatileSolidsContent'
VSC_MIN = {
    'kg': 0,
    'kg Vs': 100,
    'kg N': 0
}
VSC_MAX = {
    'kg': 100,
    'kg Vs': 100,
    'kg N': None
}


def _volatileSolidsContent_error(min: float = None, max: float = None):
    return f"must be {max}" if min == max else (
        f"must be above {min}" if max is None else (
            f"must be below {max}" if min is None else f"must be between {min} and {max}"
        )
    )


def validate_volatileSolidsContent(node: dict, list_key: str):
    def is_valid(blank_node: dict):
        units = blank_node.get('term', {}).get('units')

        def validate(values: tuple):
            index, property = values
            term_id = property.get('term', {}).get('@id')
            value = property.get('value', 0)
            min = VSC_MIN.get(units)
            max = VSC_MAX.get(units)
            return term_id != VSC_ID or all([_is_value_below(value, max), _is_value_below(min, value)]) or {
                'level': 'error',
                'dataPath': f".{PROPERTIES_KEY}[{index}].value",
                'message': _volatileSolidsContent_error(min, max)
            }
        return validate

    def validate(values: tuple):
        index, blank_node = values
        errors = flatten(map(is_valid(blank_node), enumerate(blank_node.get(PROPERTIES_KEY, []))))
        return _filter_list_errors(
            [update_error_path(error, list_key, index) for error in errors if error is not True]
        )

    return _filter_list_errors(flatten(map(validate, enumerate(node.get(list_key, [])))))
