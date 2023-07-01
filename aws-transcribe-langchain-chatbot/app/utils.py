from langchain.vectorstores import FAISS
from langchain import PromptTemplate, OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
import os


INDEX_PATH = './embeddings'
os.environ["OPENAI_API_KEY"] = "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"
openai_llm = OpenAI(max_tokens=800, temperature=0.8, streaming=True)
openai_embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
prompt_template = """Answer the questions like Pastor Poju Oyemade, a renown teacher of God's Word and founder of Covenant Christian Centre, based on context:\n\n{context}\n\n{question}"""
prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
chain = load_qa_chain(llm=openai_llm, prompt=prompt)


def load_faiss_index():
    """
    Load saved FAISS embeddings
    """
    return FAISS.load_local(INDEX_PATH, openai_embeddings)


def get_prompt_results(question):
    """
    Function to load 
    """
    vector_db = load_faiss_index()
    results = vector_db.similarity_search(question, k=10)
    response = chain({"input_documents": results, "question": question}, return_only_outputs=True)
    return response['output_text']
