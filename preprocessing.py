import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

def preprocess_text(text):
    # replacing function names with a generic term - 'method'
    r'\b[a-zA-Z_]\w*\b'
    # tokenization
    tokens = word_tokenize(text)
    # lowercasing
    tokens = [token.lower() for token in tokens]
    # replacing function names with a generic term - 'method'
    tokens = [re.sub(r'\b[a-zA-Z_]\w*[_]*\(\)', 'method', token) for token in tokens]
    # removing special characters
    tokens = [re.sub(r'[^a-zA-Z0-9]', '', token) for token in tokens]
    # removing stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    # lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    # joining the tokens back into a single string
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text

# test
raw_text = "this IS a dummy prompt with a function name my_Function_For_Work another myFunctionForWork that I am doing"
processed_text = preprocess_text(raw_text)
print("Original Text:", raw_text)
print("Processed Text:", processed_text)