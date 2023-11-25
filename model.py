class ObjectModel:
    def __init__(self, id=None, name=None, emails=None):
        self.id = id
        self.name = name
        self.emails = emails if emails is not None else []


class ObjectListModel:
    def __init__(self, count=None, next=None, previous=None, list=None):
        self.count = count
        self.next = next
        self.previous = previous
        self.list = list if list is not None else []
