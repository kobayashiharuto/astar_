from typing import List, Tuple
import abc


class IHeuristic(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def cost(self, current_tiles: List[List[int]], goal_tiles: List[List[int]]) -> int:
        raise NotImplementedError()


class Heuristic0(IHeuristic):
    def cost(self, current_tiles: List[List[int]], goal_tiles: List[List[int]]) -> int:
        return 0


class Heuristic1(IHeuristic):
    def cost(self, current_tiles: List[List[int]], goal_tiles: List[List[int]]) -> int:
        result = 0
        for (current_tile_rows, goal_tile_rows) in zip(current_tiles, goal_tiles):
            for (curr, goal) in zip(current_tile_rows, goal_tile_rows):
                if curr == None:
                    continue
                if curr != goal:
                    result += 1
        return result


class Heuristic2(IHeuristic):
    def cost(self, current_tiles: List[List[int]], goal_tiles: List[List[int]]) -> int:
        result = 0
        for (row_index, current_tile_rows) in enumerate(current_tiles):
            for (col_index, current_tile) in enumerate(current_tile_rows):
                if current_tile == None:
                    continue
                (goal_row_index, goal_col_index) = self._search_row_col(
                    current_tile, goal_tiles)
                result += abs(goal_row_index - row_index)
                result += abs(goal_col_index - col_index)
        return result

    def _search_row_col(self, target: int, tiles: List[List[int]]) -> Tuple[int, int]:
        for (row_index, tile_rows) in enumerate(tiles):
            for (col_index, tile) in enumerate(tile_rows):
                if target == tile:
                    return (row_index, col_index)
