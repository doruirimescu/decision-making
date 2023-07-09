from model import Model, create_model
import dataclasses
import user_interaction

if __name__ == "__main__":
    user_interaction.introduction()
    m = create_model()
    import json
    with open(m.get_storage_file_path(), 'w') as f:
        json.dump(dataclasses.asdict(m), f, indent=4)
