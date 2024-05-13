import torch
import torchvision.models as models
import torchvision.transforms as transforms

class DogClassifier(torch.nn.Module):
    """
    Class for loading and interfacing with trained model for classification of dogs.
    """
    def __init__(self, model_path, class_names_path):
        super(DogClassifier, self).__init__()
        self.class_names = None
        self.model = None
        try:
            # load class names
            with open(class_names_path) as f:
                self.class_names = [line.strip() for line in f.readlines()]
            # laod saved trained model
            self.model = torch.load(model_path)

            print(f"Model '{model_path}' loaded sucessfully")
        except Exception as e:
            raise Exception(e)


    def classify_dog(self, input_image):
        """
        Classifies the input image and returns the predicted class name.        
        """
        # preprocess image for model
        preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])
        input_tensor = preprocess(input_image)
        # add batch dimension for proper input
        input_batch = input_tensor.unsqueeze(0)

        # classify dog breed on image
        output = self.model(input_batch)
        # Apply softmax along the class dimension to get probabilites
        output_probs = torch.nn.functional.softmax(output, dim=1)  

        # Get top 5 predictions
        probabilities, predicted_indices = output_probs.topk(5)
        probabilities = probabilities.tolist()  # Convert to list for sorting
        predicted_indices = predicted_indices.tolist()  # Convert to list for sorting
        sorted_results = sorted(zip(probabilities[0], predicted_indices[0]), reverse=True)

        # Convert class indices to class labels using the class mapping list loaded from class_names.txt
        sorted_results_with_labels = [(self.class_names[idx], prob) for prob, idx in sorted_results]

        return sorted_results_with_labels