from cloudmesh.openapi.scikitlearn import SklearnGenerator

input_sklibrary = 'sklearn.linear_model.LogisticRegression'
model_tag = 'JonathanLogis'
SklearnGenerator.generator(input_sklibrary,model_tag)
