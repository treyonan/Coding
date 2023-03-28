class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        
class LinkedList:
    def __init__(self):
        self.head = None
        
    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
    
    def add_node_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
    
    def swap_nodes(self, node1_data, node2_data):
        if node1_data == node2_data:
            return
        
        prev_node1 = None
        node1 = self.head
        while node1 is not None and node1.data != node1_data:
            prev_node1 = node1
            node1 = node1.next
        
        prev_node2 = None
        node2 = self.head
        while node2 is not None and node2.data != node2_data:
            prev_node2 = node2
            node2 = node2.next
        
        if node1 is None or node2 is None:
            return
        
        if prev_node1 is None:
            self.head = node2
        else:
            prev_node1.next = node2
            
        if prev_node2 is None:
            self.head = node1
        else:
            prev_node2.next = node1
        
        temp = node1.next
        node1.next = node2.next
        node2.next = temp
    
    def remove_node(self, data):
        current = self.head
        prev_node = None
        
        while current is not None and current.data != data:
            prev_node = current
            current = current.next
        
        if current is None:
            return
        
        if prev_node is None:
            self.head = current.next
        else:
            prev_node.next = current.next
    
    def print_list(self):
        current = self.head
        while current is not None:
            print(current.data)
            current = current.next


my_list = LinkedList()
my_list.add_node(1)
my_list.add_node(2)
my_list.add_node(3)
my_list.add_node(4)
my_list.swap_nodes(2,3)
my_list.print_list()  # Output: 1 2 3

'''
Node Class:

__init__(self, data=None, next=None): This is the constructor method for the Node class. It takes two arguments, data and next, both of which default to None if no arguments are provided. It creates a new Node object with a data attribute and a next attribute, which is a reference to the next node in the linked list.
LinkedList Class:

__init__(self): This is the constructor method for the LinkedList class. It initializes the linked list with a head attribute that is set to None, indicating that the list is initially empty.
add_node(self, data): This method takes a single argument, data, which is the data to be stored in the new node. It creates a new Node object with this data, and then checks if the linked list is empty. If it is, it sets the new node as the head of the list. Otherwise, it traverses the list until it reaches the end, and then sets the next attribute of the last node to the new node, effectively adding it to the end of the list.
print_list(self): This method prints out the data stored in each node in the linked list. It starts by setting the current node to the head of the list, and then loops through the list, printing out the data of each node and updating the current node to the next node in the list. It continues doing this until it reaches the end of the list.
swap_nodes(self, key1, key2): This method takes two arguments, key1 and key2, which are the data values of the nodes to be swapped. It first checks if the list is empty, or if the two keys are the same, in which case there's nothing to be done. Otherwise, it initializes four variables: node1, node2, prev1, and prev2. node1 and node2 will eventually store the nodes to be swapped, and prev1 and prev2 will store the nodes that come before node1 and node2, respectively. It then traverses the list, keeping track of both the current node and the previous node, until it finds the nodes with keys matching key1 and key2. If either key isn't found in the list, the function returns without making any changes. Once both nodes are found, the next step is to actually swap them. If either node is the head of the list, we need to update the head attribute of the linked list to point to the other node. Otherwise, we need to update the next attribute of the previous node to point to the other node, effectively swapping their positions in the list. Finally, we swap the next attributes of the two nodes themselves, completing the swap.
remove_node(self, key): This method takes a single argument, key, which is the data value of the node to be removed. It first checks if the list is empty, or if the head of the list is the node to be removed. If either of these is true, it updates the head attribute of the linked list to the next node (if there is one), effectively removing the node from the list. Otherwise, it initializes two variables: current and prev. current starts at the head of the list, and prev starts as None. It then traverses the list, updating prev to be the current node before updating current to be the next node. If it finds a node with data matching key,
'''