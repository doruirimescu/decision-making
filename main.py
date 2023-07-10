from model import Model, create_model
import user_interaction
import pickle


if __name__ == "__main__":

    user_interaction.introduction()
    m = create_model()
    with open(m.get_storage_file_path(), 'wb') as f:
        p = pickle.dump(m, f, protocol=pickle.HIGHEST_PROTOCOL)

    ##load model from json
    with open("data/model/MO.json", 'rb') as f:
        m = pickle.load(f)

    print(m)
    for p in m.parameters:
        print(p)
        print(type(p.normalizer))
