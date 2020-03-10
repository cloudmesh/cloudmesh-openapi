import sklearn



def KMeans(n_clusters=8,
           init='k-means++',
           n_init=10,
           max_iter=300,
           tol=0.0001,
           precompute_distances='auto',
           verbose=0,
           random_state=None,
           copy_x=True,
           n_jobs=None,
           algorithm='auto'):

    # fix params
    sklearn.cluster.KMeans(n_clusters=n_clusters,
                           init='k-means++',
                           n_init=10,
                           max_iter=300,
                           tol=0.0001,
                           precompute_distances='auto',
                           verbose=0,
                           random_state=None,
                           copy_x=True,
                           n_jobs=None,
                           algorithm='auto')
