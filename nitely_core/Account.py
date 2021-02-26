class account:
    """
    account object stores the user account - will be extended for user db
    """
    def __init__(self, name, telephone):
        self.__name = name
        self.__telephone = telephone

    @property
    def get_name(self):
        return self.__name

    @property
    def get_telephone(self):
        return self.__telephone

