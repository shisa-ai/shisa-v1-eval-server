import os 

from pykoi import Application
from pykoi.chat import ModelFactory
from pykoi.component import Compare

# Creating an OpenAI model
api_key = os.getenv("OPENAI_API_KEY")

openai_model_1 = ModelFactory.create_model(
    model_source="openai", api_key=api_key, engine="gpt-3.5-turbo"
)
openai_model_2 = ModelFactory.create_model(
    model_source="openai", api_key=api_key, engine="gpt-4"
)
openai_model_3 = ModelFactory.create_model(
    model_source="openai", api_key=api_key, engine="gpt-4-1106-preview"
)

# pass in a list of models to compare
chatbot_comparator = Compare(models=[openai_model_1, openai_model_2])
chatbot_comparator.add(openai_model_3)

app = Application(debug=False, share=False)
app.add_component(chatbot_comparator)
app.run()
