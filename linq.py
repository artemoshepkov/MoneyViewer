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


# class Linq:
#     @staticmethod
#     def select(list, delegate):
#         newList = []

#         for item in list:
#             newList.append(delegate(item))

#         return newList

#     @staticmethod
#     def where(list, predicate):
#         newList = []

#         for item in list:
#             if predicate(item):
#                 newList.append(item)

#         return newList

#     @staticmethod
#     def sum(list, delegate):
#         resSum = 0

#         for item in list:
#             resSum += delegate(item)

#         return resSum

# # l = []
# # l.append(Transaction(0, name="shop", date="10.02.21", payment=1, type=1))
# # l.append(Transaction(0, name="shop", date="10.01.22", payment=2, type=1))
# # l.append(Transaction(0, name="health", date="11.02.22", payment=3, type=2))

# # print(Linq.select(Linq.where(l, lambda x: x.payment > 1), lambda x: x.name))
