from dataclasses import dataclass
from typing import List, Optional, Dict, Iterable

import numpy as np
from fedot.core.optimisers.fitness import SingleObjFitness
from fedot.core.utilities.data_structures import UniqueList
from fedot.core.utils import DEFAULT_PARAMS_STUB


@dataclass
class MockIndividualGraph:
    nodes: List['MockNode']


@dataclass
class MockNode:
    def __init__(self, name: str):
        self.content: Dict[str, str] = {'name': name, 'params': DEFAULT_PARAMS_STUB}
        self._nodes_from = []

    @property
    def nodes_from(self) -> List:
        return self._nodes_from

    @nodes_from.setter
    def nodes_from(self, nodes: Optional[Iterable['MockNode']]):
        self._nodes_from = UniqueList(nodes)


@dataclass
class MockIndividual:
    fitness: SingleObjFitness
    graph: MockIndividualGraph


@dataclass
class MockOptHistory:
    individuals: List[List[MockIndividual]]


@dataclass
class MockMetaData:
    dataset_name: str = ''
    task_name: str = ''


@dataclass
class MockShowcaseItem:
    metadata: MockMetaData = MockMetaData()


@dataclass
class MockInputData:
    pass


@dataclass
class MockOutputData:
    predict: np.ndarray = None


@dataclass
class MockPipeline:
    is_fitted: bool = False
    should_return_baseline: bool = False  # non-existing field

    def fit(self, *args, **kwargs):
        self.is_fitted = True

    def predict(self, *args, **kwargs):
        if not self.is_fitted:
            raise ValueError()
        return MockOutputData()
