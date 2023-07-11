from model import Model
import user_interaction
import pickle


def load_model(model_name: str):
     with open(f"data/model/{model_name}.json", 'rb') as f:
        m = pickle.load(f)
        return m

if __name__ == "__main__":
    user_interaction.introduction()
    m = user_interaction.create_model()
    with open(m.get_storage_file_path(), 'wb') as f:
        p = pickle.dump(m, f, protocol=pickle.HIGHEST_PROTOCOL)
