from binary_search_tree import BinarySearchTree

class Node:
    def __init__(self, key):
        self.key = key
        self.right = self.left = None
        self.height  = 0
        self.bf = 0

    def __str__(self):
        return f"{self.key, self.bf}"

class AVLTree(BinarySearchTree):
    def __init__(self):
        self.root = None

    def insertAVL(self, newKey):
        # insertBST를 이용해서 삽입을 먼저 진행함
        if self.insertBST(newKey):
            rotationType, p, q = self.checkBalance(newKey)
            # rotationType의 종류에 맞게 회전함
            self.rotateTree(rotationType, p, q)

            # 트리의 모든 노드들의 bf 갱신
            self.update_balance()
            
            # 회전의 종류와 회전 후 트리의 모양을 inorder로 출력
            node_list = self.all_nodes(self.root)
            key_bf_list = []
            print(f"{rotationType}", end = " ")
            for i in node_list:
                key_bf_list.append((i.key, i.bf))
            for i in key_bf_list:
                print(i, end = " ")
            print()

        else:                   # insert에서 False인 상황은 이미 동일한 키 값이 있을 경우
            node_list = self.all_nodes(self.root)
            key_bf_list = []
            for i in node_list:
                key_bf_list.append((i.key, i.bf))
            for i in key_bf_list:
                print(i, end = " ")
            print()


    def deleteAVL(self, deleteKey):
        return_node = self.deleteBST(deleteKey)     # return_node는 delete_node의 차수가 2 이상이었으면 대체되는 노드의 부모를, 2보다 작으면 삭제되는 노드의 부모를 리턴

        if return_node:
            rotationType, p, q = self.checkBalance_delete(return_node)
            self.rotateTree(rotationType, p, q)
            self.update_balance()

            node_list = self.all_nodes(self.root)
            key_bf_list = []
            print(f"{rotationType}", end = " ")
            for i in node_list:
                key_bf_list.append((i.key, i.bf))
            for i in key_bf_list:
                print(i, end = " ")
            print()
        
        else:               
            node_list = self.all_nodes(self.root)
            key_bf_list = []
            for i in node_list:
                key_bf_list.append((i.key, i.bf))
            for i in key_bf_list:
                print(i, end = " ")
            print()


    def checkBalance(self, newKey):
        self.update_balance()           ## 먼저 트리 안의 노드들의 BF를 모두 갱신함
        node = self.searchBST(newKey)   
        rotationType = "NO"
        p = q = None
        while node:    
            # node.bf = self.cal_height_node(node.left) - self.cal_height_node(node.right)
            if abs(node.bf) > 1:
                if node.bf > 1:   # 왼쪽 서브트리 불균형
                    if node.left.bf < 0: # 왼쪽 자식의 오른쪽 서브트리에 삽입됨
                        rotationType = "LR"
                    else:               # 왼쪽 자식의 왼쪽 서브트리에 삽입됨
                        rotationType = "LL"
                    p = node
                    q = self.parentBST(p)

                elif node.bf < -1:  # 오른쪽 서브트리 불균형
                    if node.right.bf > 0: # 오른쪽 자식의 왼쪽 서브트리에 삽입됨
                        rotationType = "RL"
                    else:
                        rotationType = "RR"
                    p = node
                    q = self.parentBST(p)
                return rotationType, p, q
                
            node = self.parentBST(node) # 문제가 없으면 노드의 부모를 확인

        return rotationType, p, q   # 다 돌았을 때 문제가 없으면 NO, None, None을 리턴c
       

    def checkBalance_delete(self, return_node):     # node부터 bf를 확인해나감
        self.update_balance()
        rotationType = "NO"
        p = q = None
        node = return_node

        if node == "clear":
            return rotationType, p, q
        while node:
            node.bf = self.cal_height_node(node.left) - self.cal_height_node(node.right)
            if abs(node.bf) > 1:
                if node.bf > 1:
                    if node.left.bf < 0:
                        rotationType = "LR"
                    else:
                        rotationType = "LL"
                    p = node
                    q = self.parentBST(p)
                elif node.bf < -1:
                    if node.right.bf > 0:
                        rotationType = "RL"
                    else:
                        rotationType = "RR"
                    p = node
                    q = self.parentBST(p)
                return rotationType, p, q
            node = self.parentBST(node)
        return rotationType, p, q
            

    def rotateTree(self, rotationType, p, q):
        if rotationType == "LL":        # LL회전 
            self.LL(p, q)
        elif rotationType == "RR":      # RR회전
            self.RR(p, q)
        elif rotationType == "LR":      # LR회전
            self.LR(p, q)
        elif rotationType == "RL":      # RL회전
            self.RL(p, q)
        elif rotationType == "NO":      # NO
            pass
        else:
            raise Exception("Invalid rotation")
        self.update_balance()
            

    def update_balance(self):
        self.update_height()
        for i in self.all_nodes(self.root):
            i.bf = self.cal_height_node(i.left) - self.cal_height_node(i.right)
            
        
    def all_nodes(self, node):
        nodes_list = []
        if node:
            nodes_list = self.all_nodes(node.left) 
            nodes_list.append(node) 
            nodes_list = nodes_list + self.all_nodes(node.right)
        return nodes_list


    def LL(self, p, q):
        b = p.left
        p.left = b.right
        b.right = p

        if p == self.root:
            self.root = b
        else:
            if p == q.left:
                q.left = b
            elif p == q.right:
                q.right = b
            else:
                raise Exception("Something is wrong with rotation")


    def RR(self, p, q):
        b = p.right
        p.right = b.left
        b.left = p
        if p == self.root:
            self.root = b
        else:
            if p == q.left:
                q.left = b
            elif p == q.right:
                q.right = b
            else:
                raise Exception("Something is wrong with rotation")


    def RL(self, p, q):
        b = p.right
        c = b.left

        b.left = c.right
        c.right = b
        p.right = c.left
        c.left = p
        if p == self.root:
            self.root = c
        else:
            if p == q.left:
                q.left = c
            elif p == q.right:
                q.right = c
            else:
                raise Exception("Something is wrong with rotation")


    def LR(self, p, q):
        b = p.left
        c = b.right

        b.right = c.left
        c.left = b
        p.left = c.right
        c.right = p

        if p == self.root:
            self.root = c
        else:
            if p == q.left:
                q.left = c
            elif p == q.right:
                q.right = c
            else:
                raise Exception("Something is wrong with rotation")


    
    
avl = AVLTree()
input_list = []

f = open("/Users/bk/Desktop/Dev/3-2/File-Process/Tree/avl/input_text.txt", 'r')
while True:
    line = f.readline()
    if not line:
        break
    input_list.append(line.split())
f.close()

for i in input_list:
    i[1] = int(i[1])


for i in input_list:
    # print(f"i : {i[1]}=>", end = " ")
    if i[0] == 'i':
        avl.insertAVL(i[1])
    elif i[0] == "d":
        avl.deleteAVL(i[1])
    else:
        raise Exception(f"Invalid input : {i[0]}")


