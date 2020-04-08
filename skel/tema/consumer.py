"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
from time import sleep

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

        self.name = kwargs['name']


    def run(self):
        cart_id = self.marketplace.new_cart()

        for index in range(len(self.carts)):
            for dictionary in self.carts[index]:
                operation = dictionary['type']
                product = dictionary['product']
                quantity = dictionary['quantity']

                if operation == "add":
                    #add products in cart
                    for _ in range(quantity):
                        result = self.marketplace.add_to_cart(cart_id, product)
                        while not result:
                            sleep(self.retry_wait_time)
                            result = self.marketplace.add_to_cart(cart_id, product)
                elif operation == "remove":
                    #remove products from cart
                    for _ in range(quantity):
                        self.marketplace.remove_from_cart(cart_id, product)

        #place order
        products_list = self.marketplace.place_order(cart_id)
        for prod in products_list:
            print(self.name + " bought " + str(prod))
         