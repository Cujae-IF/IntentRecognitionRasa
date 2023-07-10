import rasa, os, subprocess
from typing import List
from ruamel.yaml import YAML


# Set the configuration parameters
config = "nlu/config.yml"
training_files = "nlu/data/"
domain = "nlu/domain.yml"
models = "nlu/models/"


async def train_model_rasa(model_name: str = None):
    # Train the model
    command = f"rasa train -c {config} -d {domain} --out {models} --fixed-model-name {model_name} --data {training_files}"
    subprocess.run(command.split())
    print(f"Model trained. The model path is {models}{model_name}.")


def create_intent(intent_name: str, examples: List[str]):
    # Load the domain file
    yaml = YAML(typ='safe')
    with open(domain, 'r') as f:
        domain_data = yaml.load(f)

    # Add the new intent to the domain file
    if 'intents' not in domain_data:
        domain_data['intents'] = []
    domain_data['intents'].append(intent_name)

    # Save the updated domain file
    with open(domain, 'w') as f:
        yaml.dump(domain_data, f)

    # Create the training examples for the new intent
    nlu_data = f"\n\n## intent:{intent_name}\n"
    nlu_data += '\n'.join(f"- {example}" for example in examples)

    # Append the training examples to the NLU training data file
    with open(f'{training_files}nlu.yml', 'a') as f:
        f.write(nlu_data)


def update_intent(intent_name: str, new_examples: List[str]):
    # Create the new training examples for the intent
    nlu_data = f"\n\n## intent:{intent_name}\n"
    nlu_data += '\n'.join(f"- {example}" for example in new_examples)

    # Append the new training examples to the NLU training data file
    with open(f'{training_files}nlu.yml', 'a') as f:
        f.write(nlu_data)


def delete_intent(intent_name: str):
    # Load the domain file
    yaml = YAML(typ='safe')
    with open(domain, 'r') as f:
        domain_data = yaml.load(f)

    # Remove the intent from the domain file
    if 'intents' in domain_data:
        domain_data['intents'] = [intent for intent in domain_data['intents'] if intent != intent_name]

    # Save the updated domain file
    with open(domain, 'w') as f:
        yaml.dump(domain_data, f)

    # Load the NLU training data file
    with open(f'{training_files}nlu.yml', 'r') as f:
        nlu_data = yaml.load(f)

    # Remove the training examples for the intent from the NLU training data file
    nlu_data = [example for example in nlu_data['nlu'] if example['intent'] != intent_name]

    # Save the updated NLU training data file
    with open(f'{training_files}nlu.yml', 'w') as f:
        yaml.dump(nlu_data, f)


def delete_all_intents():
    # Load the domain file
    yaml = YAML(typ='safe')
    with open(domain, 'r') as f:
        domain_data = yaml.load(f)

    # Remove all intents from the domain file
    if 'intents' in domain_data:
        domain_data['intents'] = []

    # Save the updated domain file
    with open(domain, 'w') as f:
        yaml.dump(domain_data, f)

    # Load the NLU training data file
    with open(f'{training_files}nlu.yml', 'r') as f:
        nlu_data = yaml.load(f)

    # Remove all training examples from the NLU training data file
    nlu_data = []

    # Save the updated NLU training data file
    with open(f'{training_files}nlu.yml', 'w') as f:
        yaml.dump(nlu_data, f)
