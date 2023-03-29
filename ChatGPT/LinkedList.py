class Node:
    def __init__(self, data=None):
        # Constructor for Node class. Sets the data and next pointer.
        self.data = data
        self.next = None
        
class LinkedList:
    def __init__(self):
        # Constructor for LinkedList class. Initializes the head pointer to None.
        self.head = None
        
    def add_node(self, data):
        # Adds a new node to the end of the list with the given data.
        new_node = Node(data)
        if self.head is None:
            # If the list is empty, set the head pointer to the new node.
            self.head = new_node
        else:
            # Otherwise, traverse the list until the last node and set its next pointer to the new node.
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
    
    def add_node_at_beginning(self, data):
        # Adds a new node to the beginning of the list with the given data.
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
    
    def swap_nodes(self, node1_data, node2_data):
        # Swaps the positions of two nodes with the given data values.
        if node1_data == node2_data:
            # If the data values are the same, do nothing and return.
            return
        
        # Find the nodes and their previous nodes.
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
        
        # If either node is not found, do nothing and return.
        if node1 is None or node2 is None:
            return
        
        # Update the head pointer if necessary.
        if prev_node1 is None:
            self.head = node2
        else:
            prev_node1.next = node2
            
        if prev_node2 is None:
            self.head = node1
        else:
            prev_node2.next = node1
        
        # Swap the next pointers of the nodes.
        temp = node1.next
        node1.next = node2.next
        node2.next = temp
    
    def remove_node(self, data):
        # Removes a node with the given data value.
        current = self.head
        prev_node = None
        
        # Traverse the list to find the node and its previous node.
        while current is not None and current.data != data:
            prev_node = current
            current = current.next
        
        # If the node is not found, do nothing and return.
        if current is None:
            return
        
        # Update the head pointer if necessary.
        if prev_node is None:
            self.head = current.next
        else:
            prev_node.next = current.next
    
    def print_list(self):
        # Prints the data of each node in the list.
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
my_list.print_list()