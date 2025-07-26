# chat_chain.py
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from vector_store import load_vector_store

vectorstore = load_vector_store()
chat_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

qa_chain = ConversationalRetrievalChain.from_llm(
    chat_model,
    vectorstore.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True
)

chat_history = []
