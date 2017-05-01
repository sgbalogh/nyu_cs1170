## To run:
##  import Nim
##  Nim.NimDFS.play("Paul","Christine",5,4,6)
##  # if 1.0, then Paul wins, if -1.0 then Christine wins

class NodeIndex:
    def __init__(self, player1, player2, a_val, b_val, c_val):
        self.player1 = player1
        self.player2 = player2
        self.a_val = a_val
        self.b_val = b_val
        self.c_val = c_val
        self.nodes = []
        self.dictionary = {}
        self.create_possible_nodes()

    def create_possible_nodes(self):
        for a in range(self.a_val,-1,-1):
            for b in range(self.b_val,-1,-1):
                for c in range(self.c_val,-1,-1):
                    self.nodes.append(Node(self.player1, self.player2, a, b, c))
                    self.nodes.append(Node(self.player2, self.player1, a, b, c))
        for node in self.nodes:
            self.dictionary[node.toString()] = node

    def grab_node(self, key):
        return self.dictionary[key]

    def grab_adjacent(self, key):
        current = self.grab_node(key)
        opponent = current.opponent
        a = current.a
        b = current.b
        c = current.c
        adjacents = []
        for i in range(a-1,-1,-1):
            key = format("%s - %d - %d - %d" % (opponent, i, b, c))
            adjacents.append(self.grab_node(key))
        for i in range(b-1,-1,-1):
            key = format("%s - %d - %d - %d" % (opponent, a, i, c))
            adjacents.append(self.grab_node(key))
        for i in range(c-1,-1,-1):
            key = format("%s - %d - %d - %d" % (opponent, a, b, i))
            adjacents.append(self.grab_node(key))
        current.adjacent = adjacents
        return adjacents

class Node:
    def __init__(self, player, opponent, a, b, c):
        self.player = player
        self.opponent = opponent
        self.parent = None
        self.a = a
        self.b = b
        self.c = c
        self.adjacent = []
        self.color = "white"
        self.score = None
        self.min_steps_to_p1_win = float('inf')
        self.min_steps_to_p2_win = float('inf')
        self.assign_value()


    def toString(self):
        return format("%s - %d - %d - %d" % (self.player, self.a, self.b, self.c))

    def assign_value(self):
        if (self.a == 0 and self.b == 0 and self.c == 0):
            if (self.player == "Paul"):
                self.score = -1.0
                self.min_steps_to_p2_win = 0.0
            else:
                self.score = 1.0
                self.min_steps_to_p1_win = 0.0
    def set_parent(self,parent_node):
        self.parent = parent_node

    def get_parent(self):
        return self.parent

class NimDFS:
    @staticmethod
    def play(player1, player2, a_val, b_val, c_val):
        index = NodeIndex(player1, player2, a_val, b_val, c_val)
        key = format("%s - %d - %d - %d" % (player1, a_val, b_val, c_val))
        root = index.grab_node(key)
        root.set_parent(root)
        root.color = "gray"
        adjacents = index.grab_adjacent(root.toString())

        for adj in adjacents:
            if adj.color == "white":
                adj.set_parent(root)
                NimDFS.visit(adj, index)
        if not len(adjacents) == 0:
            if root.player == "Paul":
                if 1.0 in list(map((lambda adj: adj.score),adjacents)):
                    root.score = 1.0
                else:
                    root.score = -1.0
            else:
                if -1.0 in list(map((lambda adj: adj.score),adjacents)):
                    root.score = -1.0
                else:
                    root.score = 1.0
            root.min_steps_to_p1_win = 1.0 + min(list(map((lambda x: x.min_steps_to_p1_win),adjacents)))
            root.min_steps_to_p2_win = 1.0 + min(list(map((lambda x: x.min_steps_to_p2_win),adjacents)))

        #depth_report = NimDFS.depth_of_win(root.score, index)
        return {'score' : root.score, 'index' : index, 'min_steps_to_p1_win': root.min_steps_to_p1_win, 'min_steps_to_p2_win': root.min_steps_to_p2_win  }

    @staticmethod
    def visit(node, index):
        node.color = "gray"
        adjacents = index.grab_adjacent(node.toString())
        for adj in adjacents:
            if adj.color == "white":
                adj.set_parent(node)
                NimDFS.visit(adj, index)
        if not len(adjacents) == 0:
            if node.player == "Paul":
                if 1.0 in list(map((lambda adj: adj.score),adjacents)):
                    node.score = 1.0
                else:
                    node.score = -1.0
            else:
                if -1.0 in list(map((lambda adj: adj.score),adjacents)):
                    node.score = -1.0
                else:
                    node.score = 1.0
            node.min_steps_to_p1_win = 1.0 + min(list(map((lambda x: x.min_steps_to_p1_win),adjacents)))
            node.min_steps_to_p2_win = 1.0 + min(list(map((lambda x: x.min_steps_to_p2_win),adjacents)))
        node.color = "black"

    @staticmethod
    def depth_of_win(winning_score, index):
        if winning_score == -1.0:
            key = "Paul - 0 - 0 - 0"
        else:
            key = "Carole - 0 - 0 - 0"
        winning_node = index.grab_node(key)
        depth = 0
        moves = []
        while winning_node.get_parent() != winning_node:
            print(winning_node.toString())
            moves.append(winning_node.toString())
            winning_node = winning_node.get_parent()
            depth += 1
        print("First move: " + winning_node.toString())
        return [depth, moves]
