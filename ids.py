from itertools import count
from pprint import pprint
from time import time
import tracemalloc
from typing import List, Tuple
from memory import log_memory
from node import INode
from collections import OrderedDict


class IterativeDeepningSearcher:
    def __init__(self, init_node: INode):
        # step1: 出発のノードをOpenリストに追加
        self.init_node = init_node

    def search(self) -> Tuple[int, int, INode]:
        tracemalloc.start()
        count = 0
        depth_limit = 1
        print('\n次の初期設定からスタートします: ')
        self.init_node.print_status()
        while(True):
            print(f'スタートします depth_limit={depth_limit}')
            (count_, target_node_child) = self.limit_search(depth_limit)
            count += count_
            if target_node_child != None:
                memory = log_memory()
                print(f'使用メモリ: {memory}')
                return (memory, count, target_node_child)
            else:
                depth_limit += 1

    def limit_search(self, depth_limit):
        open_list: dict[str, INode] = {
            self.init_node.unique_key(): self.init_node}
        count = 0
        while(True):
            if len(open_list) == 0:
                print(
                    f'次の深さの探索が終わりましたが、見つかりませんでした: depth_limit={depth_limit}')
                return (count, None)

            target_node = list(open_list.values())[-1]
            del open_list[target_node.unique_key()]
            opened_node = open_list.get(target_node.unique_key())
            if opened_node != None:
                continue

            # ノードを展開して子ノードの集合を作る。
            # 深さがリミットを越えたら展開しない
            count += 1
            if target_node.depth() > depth_limit:
                continue

            target_node_children = target_node.generate_child_node()
            for target_node_child in target_node_children:
                if target_node_child.goal_check():
                    return (count, target_node_child)
                opened_node = open_list.get(
                    target_node_child.unique_key())
                if opened_node == None:
                    open_list[target_node_child.unique_key()
                              ] = target_node_child
