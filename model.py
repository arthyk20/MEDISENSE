from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
import chainlit as cl

DB_FAISS_PATH = 'C:/chatbot/vectorstore'

custom_prompt_template = """Use the following pieces of information to answer the user's query.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Query: {query}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'query'])
    return prompt

# Retrieval QA Chain
def retrieval_qa_chain(llm, prompt, db):
    print("Creating QA Chain...")
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=db.as_retriever(search_kwargs={'k': 2}),
        return_source_documents=True
    )

    print("Expected QA Chain input keys:", qa_chain.input_keys)  # Debugging
    print("QA Chain Ready.")
    
    return qa_chain

# Loading the model
def load_llm():
    print("Loading Llama Model...")
    llm = CTransformers(
        model="C:/chatbot/llama-2-7b-chat.ggmlv3.q8_0.bin",
        model_type="llama",
        max_new_tokens=512,
        temperature=0.5
    )
    print("Model Loaded Successfully.")
    return llm

# QA Model Function
def qa_bot():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    try:
        print("Loading FAISS Vector Store...")
        db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
        print("FAISS Loaded Successfully.")
    except Exception as e:
        print(f"Error loading FAISS: {e}")
        return None  # Stop if FAISS fails

    llm = load_llm()
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)

    return qa

# Chainlit code
@cl.on_chat_start
async def start():
    chain = qa_bot()  # Load once at startup
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Hi, Welcome to Medical Bot. What is your query?"
    await msg.update()

    cl.user_session.set("chain", chain)  # Store for reuse

@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")

    if chain is None:
        await cl.Message(content="Sorry, the chatbot failed to initialize. Please restart.").send()
        print("Error: Chatbot chain is None.")
        return  # Stop execution

    print("Chain exists. Processing query:", message.content)  # Debugging step

    try:
        print("Debug: Expected QA Chain Input Keys →", chain.input_keys)  # NEW DEBUGGING
        input_key = list(chain.input_keys)[0]  # Fetch the correct key dynamically
        print("Using input key:", input_key)

        # Use the correct input key
        res = await cl.make_async(chain.invoke)({input_key: message.content})

        print("Response received:", res)  # Debugging

        answer = res.get("result", "No result key found!")
        sources = res.get("source_documents", [])

        print("Final Answer:", answer)  # Debugging
        print("Sources:", sources)

        if sources:
            answer += f"\nSources: {str(sources)}"
        else:
            answer += "\nNo sources found"

        await cl.Message(content=answer).send()
    except Exception as e:
        print("Error:", e)  # Debugging
        await cl.Message(content="Sorry, I encountered an error.").send()
