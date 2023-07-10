from model import Model, create_model
import dataclasses
import user_interaction
import json

if __name__ == "__main__":

    user_interaction.introduction()
    m = create_model()
    with open(m.get_storage_file_path(), 'w') as f:
        json.dump(m.dict(), f, indent=4)

    ##load model from json
    # with open("data/model/Model1.json", 'r') as f:
    #     model_dict = json.load(f)

    # print(model_dict)
    # m = Model.parse_obj(model_dict)
    # print(m)

    # for p in m.parameters:
    #     print(p)
    #     print(p.normalizer_type)
