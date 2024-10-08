# -*- coding: utf-8 -*-
"""LIME.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dRmZqC9RLa0QVOWSM7E58AzQs2cviN_W
"""

pip install lime

"""**1. Using Decision Tree (Transparent Method)**"""

import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from lime import lime_tabular

data = load_breast_cancer()
X,y = data['data'], data['target']

print(data['feature_names'])

print(data['target_names']) #0 -> malignant and 1-> benign

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
tree_clf = DecisionTreeClassifier()
tree_clf.fit(X_train, y_train)

print(tree_clf.score(X_test,y_test))

plt.figure(figsize=(20,10))
plot_tree(tree_clf,filled=True,feature_names=data['feature_names'],class_names=data['target_names'], rounded=True)
plt.show()

"""**2. Using Random Forest Classifier (Post-Hoc Method)**"""

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)
forest_clf = RandomForestClassifier()
forest_clf.fit(X_train, y_train)
print(forest_clf.score(X_test,y_test))

print(dict(zip(data['feature_names'],forest_clf.feature_importances_)))

"""**Using LIME to Explain Random Forest's Decisions**"""

explainer = lime_tabular.LimeTabularExplainer(
    training_data = X_train,
    feature_names = data['feature_names'],
    class_names = data['target_names'],
    mode = 'classification'
)

#Explain individual instances
for i in range(20):
  print('Correct: ' , 'benign' if y_test[i] else 'malignant')
  prediction = forest_clf.predict([X_test[i]])
  print('Model Classification: ', 'benign' if prediction else 'malignant')
  print(dict(zip(data['feature_names'],X_test[i])))

  instance = X_test[i]
  explanation = explainer.explain_instance(
      data_row = instance,
      predict_fn = forest_clf.predict_proba,
      num_features=30
  )

  fig = explanation.as_pyplot_figure()
  plt.tight_layout()
  plt.show()

"""**1. Y-Axis (Feature and Thresholds):**
The y-axis lists the features used in the model's prediction, along with specific threshold values or conditions for each feature. For example:

"worst area > 1041.00" means the value of the feature "worst area" for this particular instance is greater than 1041.00.
"texture error ≤ 0.84" means the value of the feature "texture error" is less than or equal to 0.84.
Each of these rows represents a feature and its contribution in the local explanation for why the model predicted the benign class for this specific case.

**2. Bar Colors:**
The colors of the bars indicate whether a feature pushes the prediction towards the benign or malignant class:

Red Bars: These features push the prediction towards malignant. In other words, these feature values align more with instances classified as malignant by the model.
Green Bars: These features push the prediction towards benign. These feature values are more typical of instances classified as benign by the model.

**3. Bar Length and Direction:**
The length of the bars indicates the magnitude of the contribution of each feature to the prediction. *Longer bars mean that the feature had a stronger influence on the model's decision.*
The direction of the bars also matters:
Bars pointing left (negative direction): These contribute to the prediction of benign.
Bars pointing right (positive direction): These contribute towards the prediction of malignant.

**Example Breakdown:**
"worst area > 1041.00": The large red bar indicates that this feature is a strong factor pushing the model towards predicting malignant. However, since the final prediction is benign, other factors (with green bars) outweighed it.
"texture error ≤ 0.84": This green bar indicates that this feature strongly pushes the prediction towards benign.
"""