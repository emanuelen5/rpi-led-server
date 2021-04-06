from typing import Union, Tuple, List
import numpy as np
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


ND_LIKE = Union[Tuple[int, int, int], List[int], np.ndarray]


@dataclass
class LED_BaseModel(ABC):
    buffer: np.ndarray = field(init=False, repr=False)

    @abstractmethod
    def __len__(self): ...

    @abstractmethod
    def __getitem__(self, item: int): ...

    @abstractmethod
    def __setitem__(self, key: int, value: ND_LIKE): ...

    @abstractmethod
    def __iter__(self): ...

    @abstractmethod
    def fill(self, value: ND_LIKE): ...

    @abstractmethod
    def show(self): ...
