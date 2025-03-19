import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load the CSV dataset
data = pd.read_csv('filtered_gaming_data.csv')

# Extract features and target
X = data[['RTT_mean', 'RTT_min', 'RTT_max', 'RTT_std', 'Length_mean','Length_min','Length_max','Length_std']]
y = data['target_first']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Normalize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train the KNN classifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = knn.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'KNN Accuracy: {accuracy:.2f}')
print(classification_report(y_test, y_pred))


# Keep the code training now with random forest
from sklearn.ensemble import RandomForestClassifier

# Train the Random Forest classifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = rf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'RF - Accuracy: {accuracy:.2f}')
print(classification_report(y_test, y_pred))


# Keep the code training now with Decision Tree
from sklearn.tree import DecisionTreeClassifier

# Train the Decision Tree classifier
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = dt.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'DT - Accuracy: {accuracy:.2f}')
print(classification_report(y_test, y_pred))


# Keep the code training now with SVM
from sklearn.svm import SVC

# Train the SVM classifier
svm = SVC(kernel='rbf', random_state=42)
svm.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = svm.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'SVM - Accuracy: {accuracy:.2f}')
print(classification_report(y_test, y_pred))


