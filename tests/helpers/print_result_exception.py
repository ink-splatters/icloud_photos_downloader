import traceback

def print_result_exception(result):
    ex = result.exception
    if ex:
        # This only works on Python 3
        if hasattr(ex, '__traceback__'):
            traceback.print_exception(type(ex),
                value=ex, tb=ex.__traceback__)
        else:
            print(ex)
