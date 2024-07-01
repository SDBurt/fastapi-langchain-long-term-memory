from langchain_community.memory.kg import ConversationKGMemory
from langchain_openai import OpenAI
from langchain.chains.conversation.base import ConversationChain
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.messages import BaseMessage

from app.models.memory import Memory
from app.utils.database import SessionLocal
from app.services.base_service import BaseService
from app.core.config import settings

class LangChainService(BaseService):
    def __init__(self):
        llm = OpenAI(temperature=0, api_key=settings.OPENAI_API_KEY)
        self.memory = ConversationKGMemory(llm=llm, memory_key="history", input_key="input")
        
        agent1_prompt_template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. 
        If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.

        Relevant Information:

        {history}

        Conversation:
        Human: {input}
        AI:
        """

        self.agent1 = ConversationChain(
            llm=llm,
            prompt=PromptTemplate(input_variables=["history", "input"], template=agent1_prompt_template),
            memory=self.memory,
            input_key="input",
            output_key="response"
        )

        agent2_prompt_template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. 
        If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.

        Relevant Information:

        {history}

        Analyze the response for potential memory

        Conversation:
        Human: {input}
        AI:
        """
        
        self.agent2 = ConversationChain(
            llm=llm,
            prompt=PromptTemplate(input_variables=["history", "input"], template=agent2_prompt_template),
            memory=self.memory,
            input_key="input",
            output_key="response"
        )

        agent3_prompt_template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. 
        If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section and does not hallucinate.

        Relevant Information:

        {history}

        Confirm if the memory should be saved.

        Conversation:
        Human: {input}
        AI:
        """
        
        self.agent3 = ConversationChain(
            llm=llm,
            prompt=PromptTemplate(input_variables=["history", "input"], template=agent3_prompt_template),
            memory=self.memory,
            input_key="input",
            output_key="response"
        )

    def ask_question(self, question: str):
        response = self.agent1.predict(input=question, history=[])
        analysis = self.analyze_response(question, response)
        if analysis:
            self.confirm_memory(analysis, question, response)
        return response

    def analyze_response(self, question: str, response: str):
        analysis = self.agent2.predict(input=f"Question: {question}\nResponse: {response}\nShould this be remembered?", history=[])
        return analysis

    def confirm_memory(self, analysis: str, question: str, response: str):
        confirmation = self.agent3.predict(input=f"Analysis: {analysis}\nIs this a valid memory?", history=[])
        if "yes" in confirmation.lower():
            self.save_memory(question, response, long_term=True)

    def save_memory(self, question: str, response: str, long_term: bool):
        db = SessionLocal()
        try:
            memory = Memory(question=question, response=response, long_term=long_term)
            db.add(memory)
            db.commit()
            db.refresh(memory)
            return memory
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def load_memory(self, query: str):
        memory_data = self.memory.load_memory_variables({"input": query})
        return memory_data
