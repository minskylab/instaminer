from typing import Callable, Generator

from entities.post import InstaminerPost

RelevanceFunction = Callable[[int, int], float]
SearchResult = Generator[InstaminerPost, None, None]
