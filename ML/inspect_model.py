import pickle

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

print(f"Model type: {type(model)}")
