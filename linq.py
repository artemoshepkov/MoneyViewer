# from Model.transaction import *

class Linq:
    @staticmethod
    def select(list, delegate):
        for item in list:
            yield delegate(item)

    @staticmethod
    def where(list, predicate):
        for item in list:
            if predicate(item):
                yield item

    @staticmethod
    def to_list(generator):
        list = []

        for item in generator:
            list.append(item)

        return list

    @staticmethod
    def sum(list, delegate):
        resSum = 0

        for item in list:
            resSum += delegate(item)

        return resSum
        
    @staticmethod
    def max(list, delegate):
        max = -100000000000

        for item in list:
            if delegate(item) > max:
                max = delegate(item)

        if max == -100000000000:
            return

        return max
