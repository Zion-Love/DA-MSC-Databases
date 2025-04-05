'''
    Custom exception to be thrown and handled explcitly during my command binding validation calls
'''
class ValidationException(Exception):
    def __init__(self, *args):
        super().__init__(*args)