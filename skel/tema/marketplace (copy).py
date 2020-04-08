"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""
from threading import Lock

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        
        self.producers_id = 0
        self.carts_id = 0

        #dictionary with key:producers_id and value:queue of products
        self.producers_queues = {}


        #list of lists of tuples
        #every index is a cart_id
        #every card_id has a list o tuples
        #every tuple contains a product in the cart and the producer_id
        #from which the product is taken
        self.list_of_carts = [[]] 

        self.l = Lock()


    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.producers_id += 1

        #create new entry in dictionary for the current producer
        self.producers_queues.update({self.producers_id:[]})

        return self.producers_id


    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        list_of_products = self.producers_queues[producer_id]
        if len(list_of_products) >= self.queue_size_per_producer:
            return False

        self.producers_queues[producer_id].append(product[0])

        return True


    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.carts_id += 1

        self.list_of_carts.append([])
        
        return self.carts_id


    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        for producer_id in range(1, self.producers_id + 1):
            # with self.l:
            for prod in self.producers_queues[producer_id]:
                if product == prod:
                    self.producers_queues[producer_id].remove(product)
                    self.list_of_carts[cart_id].append((product, producer_id))

                    return True

        return False


    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
     
        for pair in self.list_of_carts[cart_id]:
            if pair[0] == product:
                producer_id = pair[1]
                self.producers_queues[producer_id].append(product)
                self.list_of_carts[cart_id].remove((product, producer_id))

                return


    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """

        products_list = []

        for pair in self.list_of_carts[cart_id]:
            products_list.append(pair[0])
        
        #free the lists of products for the cart_id
        self.list_of_carts[cart_id] = []

        return products_list
