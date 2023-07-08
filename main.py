from model import Model, create_model
import dataclasses

if __name__ == "__main__":
    m = create_model()
    import json
    with open(f'data/model/{m.name}.json', 'w') as f:
        json.dump(dataclasses.asdict(m), f, indent=4)
