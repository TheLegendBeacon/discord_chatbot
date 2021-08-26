import chatterbot
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.response_selection import get_first_response
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from aioify import aioify

class AsyncPredictChatBot(ChatBot):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
    
    @aioify
    def generate_response(self, input_statement, additional_response_selection_parameters):
        return super().generate_response(input_statement, additional_response_selection_parameters=additional_response_selection_parameters)

## initialize chatter bot
bot = AsyncPredictChatBot(
    'Chatty Botty',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
    ],
    database_uri='sqlite:///database.db',
    read_only=True
)
