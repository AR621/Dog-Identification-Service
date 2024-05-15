from django.apps import AppConfig
import os
from dogidentificationapp.dog_classifier import DogClassifier


class ApplicationConfig(AppConfig):
    name = 'dogidentificationapp'

    def ready(self):
        # define paths for model import
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, 'models', 'model.pth')
        class_names_path = os.path.join(current_dir, 'models', 'class_names.txt')

        # load the model        
        self.model = DogClassifier(model_path, class_names_path)
