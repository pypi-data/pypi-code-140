from hestia_earth.schema import TermTermType
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.model import find_term_match, filter_list_term_type
from hestia_earth.utils.tools import flatten, list_sum

from hestia_earth.validation.utils import _filter_list_errors, update_error_path, term_id_prefix
from hestia_earth.validation.validators.shared import is_value_different
from .practice import validate_excretaManagement


def _validate_previous_term(transformations: list, index: int):
    transformation = transformations[index]
    indexes = range(len(transformations))

    def _term_index(term_id: str, max_index: int):
        return next((i for i in indexes if transformations[i].get('term', {}).get('@id') == term_id), max_index)

    term_id = transformation.get('previousTransformationTerm', {}).get('@id')
    return term_id is None or _term_index(term_id, index) < index or {
        'level': 'error',
        'dataPath': f".transformations[{index}].previousTransformationTerm",
        'message': 'must point to a previous transformation in the list'
    }


def _validate_previous_product_value(transformations: list, index: int):
    transformation = transformations[index]
    share = transformation.get('previousTransformationShare', 100)
    inputs = transformation.get('inputs', [])
    previous_transformation = transformations[index - 1]
    products = previous_transformation.get('products', [])

    def validate_input(input_index: int):
        input = list_sum(inputs[input_index].get('value', [0]))
        product = list_sum(find_term_match(products, inputs[input_index].get('term', {}).get('@id')).get('value', [0]))
        return product == 0 or not is_value_different(product, input * share / 100, 0.01) or {
            'level': 'error',
            'dataPath': f".transformations[{index}].inputs[{input_index}].value",
            'message': 'must be equal to previous product multiplied by the share'
        }

    return len(products) == 0 or _filter_list_errors(flatten(map(validate_input, range(len(inputs)))))


def validate_previous_transformation(transformations: list):
    def validate(index: int):
        return list(map(lambda func: func(transformations, index), [
            _validate_previous_term,
            _validate_previous_product_value
        ]))

    return _filter_list_errors(flatten(map(validate, range(1, len(transformations)))))


def validate_first_transformation_fields(transformations: list):
    tr = transformations[0] if len(transformations) > 0 else None

    def validate(field: str):
        return tr.get(field) is None or {
            'level': 'error',
            'dataPath': f".transformations[0].{field}",
            'message': 'must not be set on the first transformation'
        }

    return not tr or _filter_list_errors(map(validate, ['previousTransformationTerm', 'previousTransformationShare']))


def validate_first_transformation_input(cycle: dict, transformations: list):
    tr = transformations[0] if len(transformations) > 0 else None

    def cycle_has_product(input: dict):
        term_id = input.get('term', {}).get('@id')
        return find_term_match(cycle.get('products', []), term_id, None) is not None

    return not tr or any([cycle_has_product(i) for i in tr.get('inputs', [])]) or {
        'level': 'error',
        'dataPath': '.transformations[0]',
        'message': 'at least one Input must be a Product of the Cycle'
    }


def validate_transformation_excretaManagement(transformations: list):
    def validate(values: tuple):
        index, transformation = values
        practices = transformation.get('practices', []) + [{'term': transformation.get('term')}]
        error = validate_excretaManagement(transformation, practices)
        return error is True or update_error_path(error, 'transformations', index)

    return _filter_list_errors(map(validate, enumerate(transformations)))


def validate_linked_emission(cycle: dict, list_key: str):
    emissions = cycle.get('emissions', [])

    def validate_emission(transformation_index: int, transformation: dict):
        def validate(values: tuple):
            index, emission = values
            term_id = emission.get('term', {}).get('@id')
            same_emissions = list(filter(lambda e: e.get('term', {}).get('@id') == term_id, emissions))
            linked_emission = next((e for e in same_emissions if all([
                e.get('transformation', {}).get('@id') == transformation.get('term', {}).get('@id')
            ])), None)
            return len(same_emissions) == 0 or linked_emission is not None or {
                'level': 'warning',
                'dataPath': f".{list_key}[{transformation_index}].emissions[{index}]",
                'message': 'should be linked to an emission in the Cycle',
                'params': {
                    'term': emission.get('term', {})
                }
            }

        return validate

    def validate(values: tuple):
        index, transformation = values
        return _filter_list_errors(
            map(validate_emission(index, transformation), enumerate(transformation.get('emissions', [])))
        )

    return len(emissions) == 0 or _filter_list_errors(flatten(map(validate, enumerate(cycle.get(list_key, [])))))


def _is_generic_excreta(term_id: str): return len((download_hestia(term_id) or {}).get('subClassOf', [])) == 0


def validate_excreta_inputs_products(transformations: list):
    def validate_product(transformation_index: int, input_prefix_ids: list[str]):
        def validate(values: tuple):
            index, product = values
            term = product.get('term', {})
            term_id = term.get('@id', '')
            is_excreta = term.get('termType', '') == TermTermType.EXCRETA.value
            return not is_excreta or _is_generic_excreta(term_id) or term_id_prefix(term_id) in input_prefix_ids or {
                'level': 'error',
                'dataPath': f".transformations[{transformation_index}].products[{index}]",
                'message': 'must be included as an Input',
                'params': {
                    'term': term,
                    'expected': input_prefix_ids
                }
            }
        return validate

    def validate(values: tuple):
        index, transformation = values
        excreta_inputs = filter_list_term_type(transformation.get('inputs', []), TermTermType.EXCRETA)
        input_prefix_ids = list(set([term_id_prefix(v.get('term', {}).get('@id')) for v in excreta_inputs]))
        return len(input_prefix_ids) == 0 or _filter_list_errors(
            map(validate_product(index, input_prefix_ids), enumerate(transformation.get('products', [])))
        )

    return _filter_list_errors(flatten(map(validate, enumerate(transformations))))
