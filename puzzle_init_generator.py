from copy import deepcopy
from pprint import pprint
import random
import tracemalloc
from turtle import distance
from typing import List
import numpy as np

from node import TwoDimPuzzleNode


# この手のパズルは完全ランダムだと不可能な構造があるので、それを避けて初期値を生成する
# 参考: https://manabitimes.jp/math/979
class PuzzleInitGenerator:
    def __init__(self):
        pass

    def random_generate(self, goal: List[List[int]]) -> List[List[int]]:
        size = len(goal)
        flatten_goal = np.array(goal).flatten()
        while(True):
            # 配列をランダム生成
            result = list(range(1, size * size))
            result.append(None)
            random.shuffle(result)

            # 何回スワップしたら答えになるか
            swap_count = 0
            swap_result = deepcopy(result)
            for (index, goal_num) in enumerate(flatten_goal):
                result_num = swap_result[index]
                if result_num == goal_num:
                    continue
                result_index = swap_result.index(goal_num)
                swap_result[index] = goal_num
                swap_result[result_index] = result_num
                swap_count += 1

            # 2次元化
            result = [i.tolist() for i in list(np.array_split(result, size))]
            # Noneの位置関係はどれだけ離れているか
            goal_none_row = 0
            goal_none_col = 0
            for (index, goal_row) in enumerate(goal):
                if None in goal_row:
                    goal_none_row = index
                    goal_none_col = goal_row.index(None)

            result_none_row = 0
            result_none_col = 0
            for (index, result_row) in enumerate(result):
                if None in result_row:
                    result_none_row = index
                    result_none_col = result_row.index(None)

            distance = abs(goal_none_row - result_none_row) + \
                abs(goal_none_col - result_none_col)

            # 偶奇が一致していればOK
            if distance % 2 == swap_count % 2:
                break
        return result

    def count_generate(self, count: int, goal: List[List[int]]) -> List[List[int]]:
        nodes = []
        parent_node = TwoDimPuzzleNode(goal, goal, None)
        nodes.append(parent_node)
        for _ in range(count):
            children_node = parent_node.generate_child_node()
            random.shuffle(children_node)
            for child_node in children_node:
                for node in nodes:
                    if node.equal(child_node):
                        break
                else:
                    nodes.append(child_node)
                    parent_node = child_node
                    break
            else:
                nodes.pop()
                parent_node = nodes[-1]
        return parent_node.tiles


def main():
    goal_tiles = [
        [1, 2, 3],
        [8, None, 4],
        [7, 6, 5],
    ]
    generator = PuzzleInitGenerator()
    for _ in range(10):
        pprint(generator.count_generate(40, goal_tiles))


if __name__ == '__main__':
    main()
