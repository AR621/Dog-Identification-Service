import torch
import torchvision.models as models
import torchvision.transforms as transforms

class Model(torch.nn.Module):
    """
    Class for loading and interfacing with trained model for classification of dogs.
    """
    def __init__(self, model_path, class_names_path):
        super(Model, self).__init__()
        self.class_names = None
        self.model = None
        try:
            self.model = models.resnet152(pretrained = True)
            
            self.model.fc = torch.nn.Linear(self.model.fc.in_features, 120)
            # load trained model
            self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
            # load class names
            with open(class_names_path) as f:
                self.class_names = [line.strip() for line in f.readlines()]
            print(f"Model '{model_path}' loaded sucessfully")
        except Exception as e:
            raise Exception(e)


    def classify_photo(self, input_image):
        """
        Classifies the input image and returns the predicted class name.        
        """
        # preprocess image
        preprocess = transforms.Compose([
            transforms.Resize(224),
            # transforms.CenterCrop(224),
            transforms.ToTensor(),
            # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        input_tensor = preprocess(input_image)
        # input_tensor = input_image
        input_batch = input_tensor.unsqueeze(0)
        # classify image
        output = self.model(input_batch)
        # map outputn to class names
        output_probs = torch.nn.functional.softmax(output, dim=1)  # Apply softmax along the class dimension

        probabilities, predicted_indices = output_probs.topk(5)
        probabilities = probabilities.tolist()  # Convert to list for sorting
        predicted_indices = predicted_indices.tolist()  # Convert to list for sorting

        sorted_results = sorted(zip(probabilities[0], predicted_indices[0]), reverse=True)

        # Convert class indices to class labels using the class mapping list
        sorted_results_with_labels = [(self.class_names[idx], prob) for prob, idx in sorted_results]

        return sorted_results_with_labels