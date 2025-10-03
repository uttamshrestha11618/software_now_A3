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
