from itertools import count
from pprint import pprint
from typing import List
from node import INode


class AStarSearcher:
    def __init__(self, init_node: INode):
        # step1: 出発のノードをOpenリストに追加
        self.open_list: List[INode] = [init_node]
        self.closed_list: List[INode] = []

    def search(self) -> INode:
        count = 0
        print('次の初期設定からスタートします')
        self.open_list[0].print_status()
        while(True):
            count += 1
            # step2: Openリストから経路コストg+予想経路コストhが最小の要素をひとつ選択する
            if len(self.open_list) == 0:
                return None
            min_node = min(
                self.open_list, key=lambda x: x.h_cost() + x.g_cost())
            if min_node.goal_check():
                print(f'{count}回目に見つかりました')
                return min_node
            self.open_list.remove(min_node)
            # min_node.print_status()

            # step3: ノードを展開して子ノードの集合を作る。min_nodeをCLOSEDリストに追加する。
            min_node_children = min_node.generate_child_node()
            self.closed_list.append(min_node)

            # step4: cloedリストに含まれないノードに対してOpenリストに追加する
            # CLOSEDリストに既に含まれている/含まれていないnew_nodeのリストを作成する
            already_closed_list_included_new_nodes: List[INode] = []
            not_already_closed_list_included_new_nodes: List[INode] = []
            for min_node_child in min_node_children:
                for closed_node in self.closed_list:
                    if closed_node.equal(min_node_child):
                        already_closed_list_included_new_nodes.append(
                            min_node_child)
                        break
                else:
                    not_already_closed_list_included_new_nodes.append(
                        min_node_child)

            # CLOSEDリストに含まれていないnew_nodeの場合
            for not_already_closed_new_node in not_already_closed_list_included_new_nodes:
                status_equal_node = [
                    open_node for open_node in self.open_list if open_node.equal(not_already_closed_new_node)]
                # Openリストに同じステータスのものが入っていたら、経路コストを比較し低い方を採用する
                if len(status_equal_node) == 1:
                    status_equal_node = status_equal_node[0]
                    if not_already_closed_new_node.g_cost() < status_equal_node.g_cost():
                        self.open_list.remove(status_equal_node)
                        self.open_list.append(not_already_closed_new_node)
                # Openリストに同じステータスのものが入っていなければ、Openリストに追加する
                else:
                    self.open_list.append(not_already_closed_new_node)

            # すでにClosedリストに同じステータスのものが入っていたら、経路コストを比較し低い方を採用する
            for already_closed_new_node in already_closed_list_included_new_nodes:
                status_equal_node = [
                    open_node for open_node in self.closed_list if open_node.equal(already_closed_new_node)]
                if len(status_equal_node) == 1:
                    status_equal_node = status_equal_node[0]
                    if already_closed_new_node.g_cost() < status_equal_node.g_cost():
                        self.closed_list.remove(status_equal_node)
                        self.open_list.append(already_closed_new_node)
