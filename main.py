from model import Model, create_model
import user_interaction
import json
import jsonpickle
import pickle


if __name__ == "__main__":

    user_interaction.introduction()
    m = create_model()
    with open(m.get_storage_file_path(), 'w') as f:
        p = jsonpickle.encode(m, unpicklable=True)
        json_data = json.dumps(p, indent=4)
        f.write(json_data)

    # #load model from json
    # with open("data/model/Modeello.json", 'r') as f:
    #     m = json.load(f)
    #     m = Model.parse_obj(jsonpickle.decode(m))

    # for p in m.parameters:
    #     print(p)
    #     print(type(p.normalizer))
