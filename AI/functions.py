from AI.function_execution import *


def get_function_list() -> List:
    path = os.path.join(os.path.dirname(__file__), 'Resources/functions.json')
    with open(path, 'r') as f:
        return json.load(f)


def error_function():
    yield {'type': 'function', 'content': 'Error, please try again'}
    yield {'type': 'message', 'content': 'Error, please try again'}


def execute_function(function: str, parameters: Dict) -> [bool, str]:
    if function == 'get_information':
        try:
            query_about = parameters['query_about']
        except:
            query_about = None

        try:
            suggestions_about = parameters['suggestions_about']
        except:
            suggestions_about = None
        execution = get_information_about(query_about, suggestions_about)
    else:
        execution = error_function()

    for i in execution:
        yield i
