import pickle

# Load the model
model_file = 'CV_BestModel.sav'
with open(model_file, 'rb') as f:
    model = pickle.load(f)

# Check the model's parameters
print(model)

vectorizer_file = 'vectorizer.pkl'
with open(vectorizer_file, 'rb') as f:
    vectorizer = pickle.load(f)

# Check the vectorizer's vocabulary
print(vectorizer.vocabulary_)

sample_text = "I am feeling so happy today"
vectorized_sample = vectorizer.transform([sample_text]).toarray()
print(vectorized_sample)
