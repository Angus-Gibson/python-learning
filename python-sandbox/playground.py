def add(*args):
    results = 0
    for n in args:
        results += n
    return results

# print(add(5, 5, 10))



def calculate(n, **kwargs):
    print(kwargs)
    # for key, value in kwargs.items():
    #     print(key)
    #     print(value)

    # print(kwargs["add"])
    n += kwargs["add"]
    n *= kwargs["multiply"]
    print(n)

calculate(2, add = 3, multiply = 5)

# class Car:

#     def __init__(self, **kw):
#         self.make = kw.get("make")
#         self.model = kw.get("model")
#         self.color = kw.get("seats")
#         self.color = kw.get("color")
#         # The get function of kwargs prevents keyerror crash went attempting to
#         # call an attribute with no argument

# my_car = Car(make="Nissan")
# print(my_car.model)
# print(my_car.make)

