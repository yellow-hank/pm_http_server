class QueryNotFound(Exception):
    """ If the size of the cursor returned from a query is 0 """
    def __init__(self):
        default = "The query find nothing"
        super().__init__(default)
