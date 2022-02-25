from pathlib import Path

from app.api.analytics.service import composer_history_for_case
from app.api.composer.history_convert_utils import _clear_tmp_fields, _create_edges, _create_operators_and_nodes
from fedot.core.optimisers.opt_history import OptHistory
from utils import project_root
import os


def test_correct_operator_ancestors_count(client):
    case_path = os.path.join(project_root(), 'data/scoring/scoring_classification.json')
    history = OptHistory.load(case_path)

    all_nodes = _create_operators_and_nodes(history)

    all_nodes, edges = _create_edges(all_nodes)
    all_nodes = _clear_tmp_fields(all_nodes)

    # postprocessing of edges
    new_edges = []
    nodes_ids = [n['uid'] for n in all_nodes]
    for _, edge in enumerate(edges):
        if edge['source'] in nodes_ids and edge['target'] in nodes_ids and edge['source'] != edge['target']:
            new_edges.append(edge)

    operators = [(node['uid'], node['name']) for node in all_nodes if node['type'] == 'evo_operator']
    for operator_uid, operator_name in operators:
        ancestors = [edge['source'] for edge in edges if edge['target'] == operator_uid]
        test_status = True
        if operator_name == 'mutation':
            test_status = len(ancestors) == 1
        else:
            test_status = len(ancestors) == 2
        assert test_status, (
            f'{operator_name} operators must have exactly '
            f'{"one ancestor" if operator_name == "mutation" else "two ancestors"}: '
            f'operator_ancestors_ids={ancestors}'
        )
