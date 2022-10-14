class ParsingChecker:
    @staticmethod
    def checker(func):
        def __parsing_checker(self):
            try:
                data = func(self)
            except:
                raise Exception(f"[{func.__qualname__}]: Something wrong with the content of received_email id: {self.received_email['_id']}")
            return data
        return __parsing_checker
