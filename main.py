from random import randint, random
from time import sleep, time
from tkinter.tix import Tree
from typing import List, Tuple
from a_search import AStarSearcher
from heuristic import Heuristic0, Heuristic1, Heuristic2, IHeuristic
from ids import IterativeDeepningSearcher
from node import TwoDimPuzzleHeuristicNode, TwoDimPuzzleNode
from puzzle_init_generator import PuzzleInitGenerator


def ids_search(init_slide_count: int) -> Tuple[int, float]:
    goal_tiles = [
        [1, 2, 3],
        [8, None, 4],
        [7, 6, 5],
    ]
    start_time = time()
    start_tiles = PuzzleInitGenerator().count_generate(init_slide_count, goal_tiles)
    node = TwoDimPuzzleNode(start_tiles, goal_tiles, None)
    astar_searcher = IterativeDeepningSearcher(node)

    (loop_count, result) = astar_searcher.search()
    nodes: List[TwoDimPuzzleNode] = []
    while(True):
        nodes.append(result)
        result = result.get_parent()
        if result == None:
            break
    end_time = time() - start_time
    node_count = len(nodes) - 1
    print(f"\n結果: {node_count}手")
    print(f"時間: {end_time}sec")
    print(f"試行回数: {loop_count}回")

    for node in nodes:
        node.print_status()
        print('\n')
    return (loop_count, node_count, end_time)


def astar_search(init_slide_count: int, heuristic: IHeuristic) -> Tuple[int, float]:
    goal_tiles = [
        [1, 2, 3],
        [8, None, 4],
        [7, 6, 5],
    ]
    start_time = time()
    start_tiles = PuzzleInitGenerator().count_generate(init_slide_count, goal_tiles)
    node = TwoDimPuzzleHeuristicNode(start_tiles, goal_tiles, heuristic, None)
    astar_searcher = AStarSearcher(node)

    (loop_count, result) = astar_searcher.search()
    nodes: List[TwoDimPuzzleHeuristicNode] = []
    while(True):
        nodes.append(result)
        result = result.get_parent()
        if result == None:
            break
    end_time = time() - start_time
    node_count = len(nodes) - 1
    print(f"\n結果: {node_count}手")
    print(f"時間: {end_time}sec")
    for node in nodes:
        node.print_status()
        print('\n')
    return (loop_count, node_count, end_time)


def main():
    loop = 1000
    # for i in range(loop):
    #     print(i)
    #     (loop_count, node_count, end_time) = astar_search(
    #         randint(30, 30), Heuristic2())
    #     if node_count > 25:
    #         sleep(100)
    #     with open('result/h2.csv', mode='a') as f:
    #         f.write('\n' + str(loop_count) + ',' +
    #                 str(node_count) + ',' + str(end_time))
    # for i in range(loop):
    #     print(i)
    #     (loop_count, node_count, end_time) = astar_search(
    #         randint(10, 24), Heuristic1())
    #     with open('result/h1.csv', mode='a') as f:
    #         f.write('\n' + str(loop_count) + ',' +
    #                 str(node_count) + ',' + str(end_time))
    # for i in range(loop):
    #     print(i)
    #     (loop_count, node_count, end_time) = astar_search(
    #         randint(10, 24), Heuristic0())
    #     with open('result/h0.csv', mode='a') as f:
    #         f.write('\n' + str(loop_count) + ',' +
    #                 str(node_count) + ',' + str(end_time))
    for i in range(loop):
        print(i)
        (loop_count, node_count, end_time) = ids_search(randint(10, 14))
        with open('result/ids.csv', mode='a') as f:
            f.write('\n' + str(loop_count) + ',' +
                    str(node_count) + ',' + str(end_time))


if __name__ == '__main__':
    main()
