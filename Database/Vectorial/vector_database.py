import pinecone
import pandas as pd
import os
from AI.embeddings import Embeddings
from Database.MySQL.Control.Others import Chunks
import json


class Pinecone:

    def __init__(self):
        pinecone.init(
                api_key=os.getenv('PINECONE_API_KEY'),
                environment=os.getenv('PINECONE_ENV')
        )
        self.pinecone = pinecone.Index(index_name=os.getenv('PINECONE_INDEX'))

    def insert_data(self, data: pd.DataFrame, metadata: bool):
        if metadata:
            self.pinecone.upsert(vectors=zip(data.id, data.embedding, data.metadata))
        else:
            self.pinecone.upsert(vectors=zip(data.id, data.embedding))

    def query_data(self, embedding: list, filter: dict = None, top_k: int = 2):
        if filter is None:
            return self.pinecone.query(vector=embedding, top_k=top_k, include_metadata=True)
        else:
            return self.pinecone.query(vector=embedding, filter=filter, top_k=top_k,
                                       include_metadata=True)

    def delete_data(self, ids: list):
        self.pinecone.delete(ids=ids)


class FullControl(Pinecone):

    def __init__(self, student_info: dict = None):
        super().__init__()
        self.database = Chunks()
        self.student_info = student_info

    def insert(self, text: str, metadata: dict = None):
        emb = Embeddings(text)
        id = self.database.add(text)
        embedding = emb.get_embedding()
        data = pd.DataFrame([{'id': str(id), 'embedding': embedding, 'metadata': metadata}])
        self.insert_data(data, metadata is not None)

    def delete(self, text: str):
        id = self.database.get_id(text)
        self.delete_data([str(id)])
        self.database.delete_by_id(id)

    def delete_by_id(self, id: int):
        self.delete_data([str(id)])
        self.database.delete_by_id(id)

    def delete_by_ids(self, ids: list):
        self.delete_data([str(i) for i in ids])
        for i in ids:
            self.database.delete_by_id(i)

    def query(self, text: str, filter: dict = None, top_k: int = 2):
        emb = Embeddings(text, self.student_info)
        embedding = emb.get_embedding()
        query_result = self.query_data(embedding, filter, top_k)
        query_result = json.loads(str(query_result).replace("'", '"'))

        for i in query_result['matches']:
            i['text'] = self.database.get_chunk(int(i['id']))

        return query_result

