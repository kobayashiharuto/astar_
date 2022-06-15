from __future__ import annotations
from copy import deepcopy
from platform import node
from pprint import pprint
from typing import List, Tuple
import abc

from heuristic import Heuristic1, Heuristic2, IHeuristic


class INode(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def h_cost(self) -> int:
        raise NotImplementedError()

    def g_cost(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def goal_check(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def equal(self, node: INode) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def generate_child_node(self) -> List[INode]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_parent(self) -> INode:
        raise NotImplementedError()

    @abc.abstractmethod
    def print_status(self):
        raise NotImplementedError()


class TwoDimPuzzleNode(INode):

    def __init__(self, tiles: List[List[int]], goal_tiles: List[List[int]], heuristic: IHeuristic, parent_node: TwoDimPuzzleNode):
        self.heuristic = heuristic
        self.parent_node = parent_node
        self._h_cost = heuristic.cost(tiles, goal_tiles)
        if parent_node != None:
            self._g_cost = parent_node.g_cost() + 1
        else:
            self._g_cost = 0
        self.tiles = tiles
        self.goal_tiles = goal_tiles
        pass

    def h_cost(self) -> int:
        return self._h_cost

    def g_cost(self) -> int:
        return self._g_cost

    def goal_check(self) -> bool:
        for (current_tile_rows, goal_tile_rows) in zip(self.tiles, self.goal_tiles):
            for (curr, goal) in zip(current_tile_rows, goal_tile_rows):
                if curr == None:
                    continue
                if curr != goal:
                    return False
        return True

    def equal(self, node: TwoDimPuzzleNode) -> bool:
        for (current_tile_rows, node_tile_rows) in zip(self.tiles, node.tiles):
            for (curr, goal) in zip(current_tile_rows, node_tile_rows):
                if curr == None:
                    continue
                if curr != goal:
                    return False
        return True

    def generate_child_node(self) -> List[TwoDimPuzzleNode]:
        empty_col_index = 0
        empty_row_index = 0
        child_nodes = []
        for (row_index, title_row) in enumerate(self.tiles):
            for (col_index, tile) in enumerate(title_row):
                if tile == None:
                    empty_row_index = row_index
                    empty_col_index = col_index
                    break

        # 上
        target_row_index = empty_row_index - 1
        target_col_index = empty_col_index
        child_node = self._generate_next_tiles_node(
            empty_row_index, empty_col_index, target_row_index, target_col_index)
        if child_node != None:
            child_nodes.append(child_node)

        # 下
        target_row_index = empty_row_index + 1
        target_col_index = empty_col_index
        child_node = self._generate_next_tiles_node(
            empty_row_index, empty_col_index, target_row_index, target_col_index)
        if child_node != None:
            child_nodes.append(child_node)

        # 左
        target_row_index = empty_row_index
        target_col_index = empty_col_index - 1
        child_node = self._generate_next_tiles_node(
            empty_row_index, empty_col_index, target_row_index, target_col_index)
        if child_node != None:
            child_nodes.append(child_node)

        # 右
        target_row_index = empty_row_index
        target_col_index = empty_col_index + 1
        child_node = self._generate_next_tiles_node(
            empty_row_index, empty_col_index, target_row_index, target_col_index)
        if child_node != None:
            child_nodes.append(child_node)

        return child_nodes

    def _generate_next_tiles_node(self, empty_row_index, empty_col_index, target_row_index, target_col_index) -> TwoDimPuzzleNode:
        if target_row_index < 0 or target_col_index < 0:
            return None
        try:
            target_tile = self.tiles[target_row_index][target_col_index]
            next_tiles = deepcopy(self.tiles)
            next_tiles[target_row_index][target_col_index] = None
            next_tiles[empty_row_index][empty_col_index] = target_tile
            return TwoDimPuzzleNode(next_tiles, self.goal_tiles, self.heuristic, self)
        except IndexError:
            return None

    def get_parent(self):
        return self.parent_node

    def print_status(self):
        pprint(self.tiles, width=20)


def main():
    goal_tiles = [
        [1, 2, 3],
        [8, None, 4],
        [7, 6, 5],
    ]
    start_tiles = [
        [5, 7, 8],
        [3, 4, None],
        [2, 6, 1],
    ]
    heuristic = Heuristic1()
    node = TwoDimPuzzleNode(start_tiles, goal_tiles, heuristic, None)
    child_nodes = node.generate_child_node()
    for child_node in child_nodes:
        child_node.print_status()


if __name__ == '__main__':
    main()
