"""
## Card
Attributes: 
- name
- category
Methods: 
- __str__?
"""


class Card(): 
    """
    Card
    """
    def __init__(self, name, category):
        self.name = name
        self.category = category

    def __str__(self):
        return "Category: " + self.category + ", Name: " + self.name
