#!/usr/bin/python3

from collections import defaultdict

##############
# Load input #
##############


with open("input.txt", "r") as f:
    input_data = [int(n) for n in f.read().strip().split(' ')]

class Node:
    def __init__(self, num_children, num_metadata):
        self.num_children = num_children
        self.num_metadata =[]
        self.children = []
        self.metadata = []

    def total_metadata(self):
        return sum(self.metadata) + sum([c.total_metadata() for c in self.children])

    def value(self):
        if len(self.children) == 0:
            return sum(self.metadata)
        else:
            value = 0
            for idx in self.metadata:
                if idx > 0 and idx <= len(self.children):
                    value += self.children[idx-1].value()
            return value

##############
# Solution 1 #
##############

def recursive_search(input_data, position, num_siblings):
    siblings = []
    while num_siblings > 0:
        # Load info and move to next numbers to process
        children_num = input_data[position]
        metadata_num = input_data[position+1]
        node = Node(children_num, metadata_num)
        position += 2  # Start of first child, metadata, or next sibling
        # Load children
        if children_num > 0:
            children, position = recursive_search(input_data, position, children_num)
            node.children = children
        # Load metadata
        if metadata_num > 0:
            node.metadata = input_data[position: position + metadata_num]
            position += metadata_num
        
        siblings.append(node)
        num_siblings -= 1

    return siblings, position

root_list, position = recursive_search(input_data, 0, 1)
root = root_list[0]

answer = root.total_metadata()
print(f"Solution to part 1 is {answer}")

##############
# Solution 2 #
##############

answer = root.value()
print(f"Solution to part 2 is {answer}")
