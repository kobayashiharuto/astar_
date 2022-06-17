from __future__ import annotations
from copy import deepcopy
import hashlib
from platform import node
from pprint import pprint
from typing import List, Tuple
import abc

import numpy as np

from heuristic import Heuristic0, Heuristic1, Heuristic2, IHeuristic


class INode(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def unique_key(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def cost(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def depth(self) -> int:
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
    def __init__(self, tiles: List[List[int]], goal_tiles: List[List[int]], parent_node: TwoDimPuzzleNode):
        self.parent_node = parent_node
        if parent_node != None:
            self._cost = parent_node.cost() + 1
            self._depth = parent_node.depth() + 1
        else:
            self._cost = 0
            self._depth = 1
        self.tiles = tiles
        self.goal_tiles = goal_tiles
        self._unique_key = str(tiles)
        pass

    def unique_key(self) -> int:
        return self._unique_key

    def depth(self) -> int:
        return self._depth

    def cost(self) -> int:
        return self._cost

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
        max_index = len(self.tiles) - 1
        min_index = 0
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
        if min_index <= target_row_index <= max_index and min_index <= target_col_index <= max_index:
            child_node = self._generate_next_tiles_node(
                empty_row_index, empty_col_index, target_row_index, target_col_index)
            if child_node != None:
                child_nodes.append(child_node)

        # 下
        target_row_index = empty_row_index + 1
        target_col_index = empty_col_index
        if min_index <= target_row_index <= max_index and min_index <= target_col_index <= max_index:
            child_node = self._generate_next_tiles_node(
                empty_row_index, empty_col_index, target_row_index, target_col_index)
            if child_node != None:
                child_nodes.append(child_node)

        # 左
        target_row_index = empty_row_index
        target_col_index = empty_col_index - 1
        if min_index <= target_row_index <= max_index and min_index <= target_col_index <= max_index:
            child_node = self._generate_next_tiles_node(
                empty_row_index, empty_col_index, target_row_index, target_col_index)
            if child_node != None:
                child_nodes.append(child_node)

        # 右
        target_row_index = empty_row_index
        target_col_index = empty_col_index + 1
        if min_index <= target_row_index <= max_index and min_index <= target_col_index <= max_index:
            child_node = self._generate_next_tiles_node(
                empty_row_index, empty_col_index, target_row_index, target_col_index)
            if child_node != None:
                child_nodes.append(child_node)

        return child_nodes

    def _generate_next_tiles_node(self, empty_row_index, empty_col_index, target_row_index, target_col_index) -> TwoDimPuzzleNode:
        target_tile = self.tiles[target_row_index][target_col_index]
        next_tiles = deepcopy(self.tiles)
        next_tiles[target_row_index][target_col_index] = None
        next_tiles[empty_row_index][empty_col_index] = target_tile
        return TwoDimPuzzleNode(next_tiles, self.goal_tiles, self)

    def get_parent(self):
        return self.parent_node

    def print_status(self):
        pprint(self.tiles, width=20)


class TwoDimPuzzleHeuristicNode(TwoDimPuzzleNode):
    def __init__(self, tiles: List[List[int]], goal_tiles: List[List[int]], heuristic: IHeuristic, parent_node: TwoDimPuzzleHeuristicNode):
        self.heuristic = heuristic
        self.parent_node = parent_node
        self._h_cost = heuristic.cost(tiles, goal_tiles)
        if parent_node != None:
            self._g_cost = parent_node._g_cost + 1
            self._depth = parent_node.depth() + 1
        else:
            self._g_cost = 0
            self._depth = 1
        self.tiles = tiles
        self.goal_tiles = goal_tiles
        self._unique_key = str(tiles)
        pass

    def cost(self) -> int:
        return self._h_cost + self._g_cost

    def _generate_next_tiles_node(self, empty_row_index, empty_col_index, target_row_index, target_col_index) -> TwoDimPuzzleHeuristicNode:
        if target_row_index < 0 or target_col_index < 0:
            return None
        try:
            target_tile = self.tiles[target_row_index][target_col_index]
            next_tiles = deepcopy(self.tiles)
            next_tiles[target_row_index][target_col_index] = None
            next_tiles[empty_row_index][empty_col_index] = target_tile
            return TwoDimPuzzleHeuristicNode(next_tiles, self.goal_tiles, self.heuristic, self)
        except IndexError:
            return None


def main():
    goal_tiles = [
        [1, 2, 3],
        [8, None, 4],
        [7, 6, 5],
    ]
    goal_tiles2 = [
        [1, 2, 3],
        [8, None, 4],
        [7, 6, 5],
    ]
    start_tiles = [
        [5, 7, 8],
        [3, 4, None],
        [2, 6, 1],
    ]
    heuristic = Heuristic2()
    node = TwoDimPuzzleHeuristicNode(start_tiles, goal_tiles, heuristic, None)
    child_nodes = node.generate_child_node()
    for child_node in child_nodes:
        print(child_node.unique_key())


if __name__ == '__main__':
    main()
