from time import time
import logging
import io
import sys
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import fetch_lfw_people
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from cloudmesh.common.Benchmark import Benchmark

# This examples is takenfrom https://scikit-learn.org/stable/auto_examples/applications/plot_face_recognition.html#sphx-glr-auto-examples-applications-plot-face-recognition-py

def eigenfaces_svm() -> str:
    """
        run eigenfaces_svm example
        :return type: str
    """
    #print(__doc__)
    Benchmark.Start()
    # Display progress logs on stdout
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

    # #############################################################################
    # Download the data, if not already on disk and load it as numpy arrays

    lfw_people = fetch_lfw_people(min_faces_per_person=70, resize=0.4)

    # introspect the images arrays to find the shapes (for plotting)
    n_samples, h, w = lfw_people.images.shape

    # for machine learning we use the 2 data directly (as relative pixel
    # positions info is ignored by this model)
    X = lfw_people.data
    n_features = X.shape[1]

    # the label to predict is the id of the person
    y = lfw_people.target
    target_names = lfw_people.target_names
    n_classes = target_names.shape[0]

    result = "Total dataset size:\n"
    result += "n_samples: %d\n" % n_samples
    result += "n_features: %d\n" % n_features
    result += "n_classes: %d\n" % n_classes

    # #############################################################################
    # Split into a training set and a test set using a stratified k fold

    # split into a training and testing set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42)


    # #############################################################################
    # Compute a PCA (eigenfaces) on the face dataset (treated as unlabeled
    # dataset): unsupervised feature extraction / dimensionality reduction
    n_components = 150

    result += "Extracting the top %d eigenfaces from %d faces\n" \
              % (n_components, X_train.shape[0])
    t0 = time()
    pca = PCA(n_components=n_components, svd_solver='randomized',
              whiten=True).fit(X_train)
    result += "done in %0.3fs\n" % (time() - t0)

    eigenfaces = pca.components_.reshape((n_components, h, w))

    result += "Projecting the input data on the eigenfaces orthonormal basis\n"
    t0 = time()
    X_train_pca = pca.transform(X_train)
    X_test_pca = pca.transform(X_test)
    result += "done in %0.3fs\n" % (time() - t0)

    # #############################################################################
    # Train a SVM classification model

    result += "Fitting the classifier to the training set\n"
    t0 = time()
    param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5],
                  'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], }
    clf = GridSearchCV(
        SVC(kernel='rbf', class_weight='balanced'), param_grid
    )
    clf = clf.fit(X_train_pca, y_train)
    result += "done in %0.3fs\n" % (time() - t0)
    result += "Best estimator found by grid search:\n"
    result += "%s\n" % clf.best_estimator_


    # #############################################################################
    # Quantitative evaluation of the model quality on the test set

    result += "Predicting people's names on the test set\n"
    t0 = time()
    y_pred = clf.predict(X_test_pca)
    result += "done in %0.3fs\n" % (time() - t0)

    result += "%s\n" % str(classification_report(y_test, y_pred, target_names=target_names))
    result += "%s\n" % str(confusion_matrix(y_test, y_pred, labels=range(n_classes)))

    Benchmark.Stop()
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    Benchmark.print()
    result += new_stdout.getvalue()
    sys.stdout = old_stdout
    print(result)
    return result

#eigenfaces_svm()

    # #############################################################################
    # Qualitative evaluation of the predictions using matplotlib



    #prediction_titles = [title(y_pred, y_test, target_names, i)
                         #for i in range(y_pred.shape[0])]

    #plot_gallery(X_test, prediction_titles, h, w)

    # plot the gallery of the most significative eigenfaces

    #eigenface_titles = ["eigenface %d" % i for i in range(eigenfaces.shape[0])]
    #plot_gallery(eigenfaces, eigenface_titles, h, w)

    #plt.show()
