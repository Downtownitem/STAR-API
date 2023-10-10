# Welcome to STAR API 🚀🤖
Hello and thank you for visiting us! In this repository, we present to you STAR API, a project that aims to bring the vast universe of astronomical and spatial data closer through an interactive and intuitive experience.

## 🌌 About the Project
STAR API is an API that utilizes LLMs (Large Language Models), embeddings and AI Agents to provide a chatbot focused on delivering answers and suggestions grounded in official NASA data. Our goal is to facilitate access to information in a user-friendly and conversational manner, allowing users to obtain accurate and quick answers to their inquiries about space, planets, space missions, and much more.

## 🚀 Technology and Data
LLM: We implement the gpt-3.5-turbo-0613 model as main LLM in the project.

Embeddings: We use embeddings to capture the semantics of words and phrases, enabling the chatbot to make relations with the official information and the asks of the user.

AI Agents: One of the principal objectives of this project is to minimize the occurrence of hallucinations in the chatbot's responses. To achieve this, various AI agents are assigned specific, small tasks. These tasks include generating questions related to the primary inquiry and establishing recommended procedures to be followed.

Pinecone Database: A vector database, to enable efficient similarity search and matching for our linguistic embeddings, enhancing the chatbot's ability to understand and generate relevant, semantically-aligned responses.

MySQL Database: Employ a MySQL database to store, manage, and retrieve the extensive and rich data from NASA, ensuring the chatbot provides information that is not only reliable and accurate but also quickly accessible.

## 🛰️ API Usage
🛰️ API Usage
STAR API is designed to be effortlessly accessible to developers and space enthusiasts alike. Through straightforward endpoints, you can integrate the chatbot's functionalities into your applications, websites, or research projects.

🚨 Important Note on Usage: While this repository provides the base code, launching it directly from the project is not feasible as it requires specific credentials for the database and APIs used, which cannot be shared publicly. However, we have deployed this database, and it's possible to test its functionalities through a dedicated endpoint which you can access and explore at: https://daniel-martinez.onrender.com/docs

Usage Process:
1. Create a new conversation in the endpoint /start-conversation
2. Get the id and send it together with the message in the endpoint /response
3. When you want the end the conversation send the id in the endpoint /close-conversation
