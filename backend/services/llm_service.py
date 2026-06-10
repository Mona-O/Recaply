from config.get_LLM_key import MISTRAL_API_KEY
from mistralai.client import Mistral

class LLMService: 
    def __init__(self):
        self.client = Mistral(api_key=MISTRAL_API_KEY)
        
    def build_prompt(self,text):
        return f"""
    Tu es un assistant de réunion.

    TRANSCRIPTION de la réunion est:
    {text}

    Donne un compte rendu structuré , en markdown, pour une gestion de connaissance d'entreprise, adapté à des ingenieurs logiciels.

    """

    def generate_report_LLM(self,transcript):
        prompt = self.build_prompt(transcript)
        response = self.client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content