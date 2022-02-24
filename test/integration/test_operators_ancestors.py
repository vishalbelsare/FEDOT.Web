from app.api.analytics.service import composer_history_for_case
from app.api.composer.history_convert_utils import _clear_tmp_fields, _create_edges, _create_operators_and_nodes


def test_correct_operator_ancestors_count(client):
    case_id = 'scoring'
    history = composer_history_for_case(case_id)
    all_nodes = _create_operators_and_nodes(history)

    all_nodes, edges = _create_edges(all_nodes)
    all_nodes = _clear_tmp_fields(all_nodes)

    operators = [(node['uid'], node['name']) for node in all_nodes if node['type'] == 'evo_operator']
    for operator_uid, operator_name in operators:
        ancestors = [edge['source'] for edge in edges if edge['target'] == operator_uid]
        if operator_name == 'mutation':
            assert len(ancestors) == 1, 'mutation operators must have only one ancestor'
        else:
            assert len(ancestors) == 2, 'crossover operators must have only two ancestors'
