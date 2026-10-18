class Company:
    
    def __init__(self, name="", products=None):
        self.name = name
        self.products = products if products is not None else []