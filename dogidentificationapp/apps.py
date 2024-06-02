from django.apps import AppConfig
import os
from dogidentificationapp.dog_classifier import DogClassifier
from django.conf import settings


class ApplicationConfig(AppConfig):
    name = 'dogidentificationapp'


    def ready(self):
        # define paths for model import
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, 'models', settings.DOG_CLASSIFIER_MODEL_NAME)
        class_names_path = os.path.join(current_dir, 'models', 'class_names.txt')

        # load dog breed names
        try:
            with open(class_names_path, 'r') as f:
                dog_classes = f.read().splitlines()
                self.dog_classes = [dog_class.replace('_', ' ').title() for dog_class in dog_classes]
        except Exception as e:
            print(f"Failed to read class names: {e}")

        # load the model        
        self.dog_classifier = DogClassifier(model_path, class_names_path)
