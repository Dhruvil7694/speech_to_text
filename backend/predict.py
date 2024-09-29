import pickle
import sys  # To read command line arguments


# Load the model
loaded_model = pickle.load(open('CV_BestModel.sav', 'rb'))

# Load the vectorizer
with open('vectorizer.pkl', 'rb') as file:
    loaded_vectorizer = pickle.load(file)

# Function to clean the text (implement this function based on your preprocessing steps)
def text_cleaner(text):
    # Add your text cleaning logic here
    return text.lower()  # Example: converting to lowercase

# Prediction function
def predict(text):
    clean_text = text_cleaner(text)
    vectorized_text = loaded_vectorizer.transform([clean_text]).toarray()
    prediction_proba = loaded_model.predict_proba(vectorized_text)
    prediction = loaded_model.predict(vectorized_text)[0]
    output = {0: "No Depression", 1: "Depression"}
    return output[prediction], prediction_proba


if __name__ == "__main__":
    # Read the input from command line arguments
    input_text = ' '.join(sys.argv[1:])  # Combine all arguments as input
    result = predict(input_text)
    print(result)
