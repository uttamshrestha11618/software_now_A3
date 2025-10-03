from transformers import pipeline
from PIL import Image
from utils import timer, logger  # Import custom decorators

class BaseModel:
    def __init__(self, model_name, task):
        self._model_name = model_name  # Encapsulation: private attribute
        self._task = task
        self._pipeline = pipeline(task, model=model_name)  # Encapsulation: private pipeline

    @property
    def model_name(self):  # Encapsulation: getter for private attribute
        return self._model_name

    def run(self, input_data):
        raise NotImplementedError("Subclasses must implement run method")  # For polymorphism

class TextGenerationModel(BaseModel):
    def __init__(self, model_name='distilgpt2'):
        super().__init__(model_name, 'text-generation')

    @timer  # Multiple decorators
    @logger
    def run(self, input_data):  # Method overriding and polymorphism
        result = self._pipeline(input_data, max_length=50, num_return_sequences=1)
        return result[0]['generated_text']  # Override to extract generated text

class ImageClassificationModel(BaseModel):
    def __init__(self, model_name='google/vit-base-patch16-224'):
        super().__init__(model_name, 'image-classification')

    @timer  # Multiple decorators
    @logger
    def run(self, input_data):  # Method overriding and polymorphism
        image = Image.open(input_data)  # input_data is file path
        result = self._pipeline(image)
        return "\n".join([f"{res['label']}: {res['score']:.2f}" for res in result])  # Override to format classifications

