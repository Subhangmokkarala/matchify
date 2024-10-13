from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Example Data (for illustration)
# Each row: [user's age, genre preference, top track's danceability]
X = np.array([[22, 'pop', 0.8], [25, 'rock', 0.4], [30, 'jazz', 0.6]])
y = np.array([1, 0, 1])  # Labels (e.g., match with user 1 or not)

# Encode genres and split data
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
X[:, 1] = le.fit_transform(X[:, 1])

# Train the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Predict trends (user's future music preference)
predictions = clf.predict(X_test)
