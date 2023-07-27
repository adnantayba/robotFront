from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
import numpy as np

dataset = [("your left hand", 'left'), ("your right hand", 'right'), ("both hands", 'both'),
           ("your hand on the left", 'left'), ("your hand on the right", 'right'), ("both hands", 'both'),
           ("put up your left hand", 'left'), ("put up your right hand", 'right'), ("both hands up", 'both'),
           ("show me your left hand", 'left'), ("show me your right hand", 'right'), ("the both hands", 'both'),
           ("point with your left hand", 'left'), ("point with your right hand", 'right'), ("point with both hands", 'both'),
           ("the left hand", 'left'), ("extend your hands together", 'right'), ("extend both hands", 'both'),
           ("give me your left hand", 'left'), ("the right hand", 'right'), ("give me both hands", 'both'),
           ("wave with your left hand", 'left'), ("wave with your right hand", 'right'), ("wave with both hands", 'both'),
           ("hold up your left hand", 'left'), ("hold up your right hand", 'right'), ("hold both hands up", 'both'),
           ("left hand up", 'left'), ("right hand up", 'right hand'), ("both hands up", 'both'),
           ("your left hand if you agree", 'left'), ("your right hand if you agree", 'right'), ("both hands if you agree", 'both'),
           ("your left hand if you disagree", 'left'), ("your right hand if you disagree", 'right'), ("both hands if you disagree", 'both'),
           ("your left hand if it's true", 'left'), ("your right hand if it's true", 'right'), ("both hands if it's true", 'both'),
           ("your left hand if it's false", 'left'), ("your right hand if it's false", 'right'), ("both hands if it's false", 'both'),
           ("raise your left hand", 'left'), ("raise your right hand", 'right'), ("raise both hands", 'both'),
]

dataset = dataset + [
    ("your left hand on your chin", 'left'), ("your right hand", 'right'), ("both hands", 'both'),
    ("scratch your left hand", 'left'), ("the right hand", 'right'), ("both", 'both'),
    ("pat your left hand on your chest", 'left'), ("right hand", 'right'), ("your both hands", 'both'),
    ("rub your left hand", 'left'), ("right", 'right'), ("your both hands", 'both'),
  
]

additional_data = [
    ("your left hand on your head", 'left'), ("your right hand on your head", 'right'), ("both hands on your head", 'both'),
    ("touch your left hand to your nose", 'left'), ("touch your right hand to your nose", 'right'), ("touch both hands to your nose", 'both'),
    ("hold a pen with your left hand", 'left'), ("hold a pen with your right hand", 'right'), ("hold a pen with both hands", 'both'),
    ("your left hand on the table", 'left'), ("your right hand on the table", 'right'), ("both hands on the table", 'both'),
    ("shake hands with your left hand", 'left'), ("shake hands with your right hand", 'right'), ("shake hands with both hands", 'both'),
    ("cover your left eye with your hand", 'left'), ("cover your right eye with your hand", 'right'), ("cover both eyes with your hands", 'both'),
    ("your left hand behind your back", 'left'), ("your right hand behind your back", 'right'), ("both hands behind your back", 'both'),
    ("your left hand on your hip", 'left'), ("your right hand on your hip", 'right'), ("both hands on your hips", 'both'),
    ("snap your fingers with your left hand", 'left'), ("snap your fingers with your right hand", 'right'), ("snap your fingers with both hands", 'both'),
    ("your left hand near your ear", 'left'), ("your right hand near your ear", 'right'), ("both hands near your ears", 'both'),
    ("swing your left hand in the air", 'left'), ("swing your right hand in the air", 'right'), ("swing both hands in the air", 'both'),
    ("clap your hands with your left hand", 'left'), ("clap your hands with your right hand", 'right'), ("clap your hands with both hands", 'both'),
]

# Append the additional data to the existing dataset
dataset += additional_data

# Splitting into sentences and labels
sentences, labels = zip(*dataset)

# Create a label encoder
label_encoder = LabelEncoder()

# Assigning values to X and y
X = list(sentences)
y = list(labels)

y_encoded = label_encoder.fit_transform(y)  # Convert labels to numerical values

# Set the random seed for reproducibility
random_seed = 42
np.random.seed(random_seed)

from sklearn.feature_extraction.text import TfidfVectorizer
tf_idf = TfidfVectorizer()

X = tf_idf.fit_transform(X)
x_train_embedding, x_test_embedding, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=random_seed)

svm_model = SVC()
svm_model.fit(x_train_embedding, y_train)