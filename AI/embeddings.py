import openai
from typing import List, Dict
import pandas as pd
import ast
import os
import json


def fix_text(text: str) -> str:
    return text.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ',
                                                                                                                  'n')


class Embeddings:

    def __init__(self, text: str, student_info: dict = None):
        super().__init__()
        self.text = text

        with open(os.path.join(os.path.dirname(__file__), 'Resources/keys.json'), 'r') as f:
            openai.api_key = json.load(f)['OPENAI_API_KEY']

    def get_embedding(self) -> List[float]:
        request = openai.Embedding.create(
            model='text-embedding-ada-002',
            input=self.text
        )
        return request['data'][0]['embedding']

    def get_text_embeddings(self) -> Dict[str, List[float]]:
        # Split the text into paragraphs
        paragraphs = self.text.split('\n\n')

        # Purge the empty paragraphs
        paragraphs = [paragraph for paragraph in paragraphs if paragraph.strip() != '']

        # Get the embeddings
        data = {}
        for paragraph in paragraphs:
            data[fix_text(paragraph)] = self.get_embedding(paragraph)

        return data

    def get_file_embeddings(self, file: str) -> Dict[str, List[float]]:
        # Read the file
        with open(file, 'r') as f:
            text = f.read()

        # Get the embeddings
        return self.get_text_embeddings(text)

    def save_embeddings(self, embeddings: Dict[str, List[float]], file: str):
        # Convert the embeddings to a dataframe
        df = pd.DataFrame(data={
            'text': list(embeddings.keys()),
            'embedding': list(embeddings.values())
        })

        # Save the dataframe
        file = file.split('.')[0] + '.csv'
        df.to_csv(file)

    def load_embeddings(self, file: str) -> Dict[str, List[float]]:
        # Load the dataframe
        df = pd.read_csv(file)

        # Convert the embedding column to a list
        df.embedding = df.embedding.apply(lambda x: ast.literal_eval(x))

        # Convert the dataframe to a dictionary
        return dict(zip(df.text, df.embedding))

    def load_embeddings_as_dataframe(self, file: str) -> pd.DataFrame:
        # Load the dataframe
        df = pd.read_csv(file)

        # Convert the embedding column to a list
        df.embedding = df.embedding.apply(lambda x: ast.literal_eval(x))

        return df
