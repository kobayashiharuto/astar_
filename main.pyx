from tkinter.tix import Tree
from typing import List
from a_search import AStarSearcher
from heuristic import Heuristic0, Heuristic1, Heuristic2
from node import TwoDimPuzzleNode
from puzzle_init_generator import PuzzleInitGenerator


def main():
    init_generator = PuzzleInitGenerator()
    goal_tiles = [
        [1, 2, 3],
        [8, None, 4],
        [7, 6, 5],
    ]
    start_tiles = init_generator.generate(goal_tiles)
    heuristic = Heuristic1()
    node = TwoDimPuzzleNode(start_tiles, goal_tiles, heuristic, None)
    astar_searcher = AStarSearcher(node)

    result = astar_searcher.search()
    nodes: List[TwoDimPuzzleNode] = []
    while(True):
        nodes.append(result)
        result = result.get_parent()
        if result == None:
            break

    print(f"\n結果: {len(nodes)}手")
    nodes.reverse()
    for node in nodes:
        node.print_status()
        print('')


if __name__ == '__main__':
    main()
