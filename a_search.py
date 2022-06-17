from itertools import count
from pprint import pprint
from time import time
import tracemalloc
from typing import List, Tuple

import numpy as np
from memory import log_memory
from node import INode


class AStarSearcher:
    def __init__(self, init_node: INode):
        # step1: 出発のノードをOpenリストに追加
        self.init_node = init_node
        # ※ dictを使っているのは、同一ノード検索の効率化のため。
        self.open_list: dict[int, INode] = {init_node.unique_key(): init_node}
        self.closed_list: dict[int, INode] = {}
        self.open_list_cost: dict[int, INode] = {
            init_node.unique_key(): init_node.cost()}

    def search(self) -> Tuple[int, int, INode]:
        tracemalloc.start()
        count = 0
        print('次の初期設定からスタートします')
        self.init_node.print_status()
        while(True):
            count += 1
            # step2: Openリストからコストが最小の要素をひとつ選択する
            if len(self.open_list) == 0:
                return None
            open_list_cost_val = list(self.open_list_cost.values())
            open_list_cost_key = list(self.open_list_cost.keys())
            min_index = np.array(open_list_cost_val).argmin()
            min_node = self.open_list[open_list_cost_key[min_index]]
            if min_node.goal_check():
                print(f'{count}回目に見つかりました')
                memory = log_memory()
                print(f'使用メモリ: {memory}')
                return (memory, count, min_node)
            self.open_remove(min_node)

            # step3: ノードを展開して子ノードの集合を作る。min_nodeをCLOSEDリストに追加する。
            min_node_children = min_node.generate_child_node()
            self.closed_list[min_node.unique_key()] = min_node

            # step4: cloedリストに含まれないノードに対してOpenリストに追加する
            # CLOSEDリストに既に含まれている/含まれていないnew_nodeのリストを作成する
            not_already_closed_list_included_new_nodes: List[INode] = []
            for min_node_child in min_node_children:
                closed_node = self.closed_list.get(min_node_child.unique_key())
                # すでにClosedリストに同じステータスのものが入っていたら、経路コストを比較し低い方を採用する
                if closed_node != None:
                    if min_node_child.cost() < closed_node.cost():
                        del self.closed_list[closed_node.unique_key()]
                        self.open_add(new_node)
                else:
                    not_already_closed_list_included_new_nodes.append(
                        min_node_child)

            # CLOSEDリストに含まれていないnew_nodeの場合
            for new_node in not_already_closed_list_included_new_nodes:
                open_node = self.open_list.get(new_node.unique_key())
                # Openリストに同じステータスのものが入っていたら、経路コストを比較し低い方を採用する
                if open_node != None:
                    if new_node.cost() < open_node.cost():
                        self.open_remove(open_node)
                        self.open_add(new_node)
                # Openリストに同じステータスのものが入っていなければ、Openリストに追加する
                else:
                    self.open_add(new_node)

    def open_add(self, new_node: INode):
        self.open_list[new_node.unique_key()] = new_node
        self.open_list_cost[new_node.unique_key()] = new_node.cost()

    def open_remove(self, remove_node: INode):
        del self.open_list[remove_node.unique_key()]
        del self.open_list_cost[remove_node.unique_key()]
