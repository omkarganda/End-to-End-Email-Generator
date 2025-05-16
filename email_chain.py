import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
                            model="llama-3.3-70b-versatile",
                            temperature=0,
                            groq_api_key = os.getenv("GROQ_API_KEY")
                        )
    
    def extract_job_details(self, cleaned_text):
        skills_extract_prompt = PromptTemplate.from_template(
                                                        """
                                                        ### SCRAPED TEXT FROM WEBSITE:
                                                            {page_data}
                                                            ### INSTRUCTION:
                                                            The provided text is scraped from a careers page of a website.  
                                                            Extract the job postings and format them as a JSON array, where each job includes the following keys:  
                                                            - `role` (job title)  
                                                            - `experience` (required experience level)  
                                                            - `skills` (necessary skills or qualifications)  
                                                            - `description` (job description)  

                                                            Return only valid JSON without additional text.  
                                                            ### VALID JSON (NO PREAMBLE):
                                                        """
                                                    )

        skill_extract_chain = skills_extract_prompt | self.llm
        response = skill_extract_chain.invoke(input={"page_data": cleaned_text})

        try:
            json_parser = JsonOutputParser()
            response = json_parser.parse(response.content)
        except OutputParserException:
            raise OutputParserException("Provided context is too large to parse jobs.")
        
        return response if isinstance(response, list) else [response]
    
    def write_email(self, job, links):
        write_email_prompt = PromptTemplate.from_template(
                                                    """
                                                    ### JOB DESCRIPTION:
                                                        {job_description}
                                                        
                                                        ### INSTRUCTION:
                                                        You are Omkar (full name: Omkareswara Reddy, Ganda), a current Master's student in Computer Science at University of Colorado Denver, an aspiring Data Scientist & experienced professional 
                                                        email write in professional settings. You have worked as a Data Engineer in the company Tata Consultancy Servicesfor 3 years. You are experienced 
                                                        in the cloud technologies such as AWS & Google Cloud Platform. You have deep knowledge in the programming languages Python & SQL. You have working knowledge 
                                                        in the Machine Learning related technologies like Tensorflow, PyTorch and are experience in the fields of Natural Language Processing, Reinforcement Learning, 
                                                        Generative AI. Your job is to write a cold email to the hriring manager/recruiter regarding the job mentioned above describing my capabilites and 
                                                        how I would be suitable for the job, what qualities I would bring to the job to succeed. Also add the most relevant ones from the following links to 
                                                        showcase my portfolio: {link_list}
                                                        Remember you are Omkar, an aspiring Data Scientist. 
                                                        Do not provide a preamble.
                                                        ### EMAIL (NO PREAMBLE):    
                                                    """
                                                )
        
        write_email_chain = write_email_prompt | self.llm
        response = write_email_chain.invoke({"job_description": str(job), "link_list": links})
        return response.content

if __name__ == "__main__":
    print()