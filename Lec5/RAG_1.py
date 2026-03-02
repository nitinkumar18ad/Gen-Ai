from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from langchain_qdrant import QdrantVectorStore

pdf_path = Path(__file__).parent / "Student.pdf"
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
     chunk_overlap=200,
)

split_docs = text_splitter.split_documents(documents=docs)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key="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"
)


print("Injection done")

retriver = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="larning_langchain",
    embedding=embeddings
)

search_result = retriver.similarity_search(
    query="What is Number System?"

)

print("relavent chunks", search_result)