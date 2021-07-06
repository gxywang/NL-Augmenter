import random
import json

from checklist.perturb import Perturb
from interfaces.SentenceOperation import SentenceAndTargetOperation
from tasks.TaskTypes import TaskType

with open('abbrev_dict.json','r') as file:
    abbrev_dict = json.loads(file.read())
    

def abbreviate(text, seed = 0, max_outputs = 1):
    random.seed(seed)
    result = []
    for _ in range(max_outputs):
        result = []
        for word in text:
            if word in abbrev_dict:
                result.append(abbrev_dict[word])
            else:
                result.append(word)
        result = "".join(result)
        results.append(result)
    return result


class Abbreviate(SentenceAndTargetOperation):
    tasks = [TaskType.TEXT_TO_TEXT_GENERATION]
    languages = ["en"]
    tgt_languages = ["en"]

    def __init__(self, seed = 0, max_outputs = 1):
        super().__init__(seed, max_outputs = max_outputs)

    def generate(self, sentence: str, target: str):
        perturbed = abbreviate(
            text = sentence, seed = self.seed, max_outputs = self.max_outputs
        )
        return perturbed



# Sample code to demonstrate adding test cases.
if __name__ == '__main__':
    import json
    from TestRunner import convert_to_snake_case
    tf = Abbreviate()
    sentence = "Andrew finally returned the French book to Chris that I bought last week"
    test_cases = []
    src = ["Andrew finally returned the French book to Chris that I bought last week",
           "Sentences with gapping, such as Paul likes coffee and Mary tea, lack an overt predicate"
           " to indicate the relation between two or more arguments."]
    tgt = ["Andrew did not return the French book to Chris that was bought earlier",
           "Gapped sentences such as Paul likes coffee and Mary tea, lack an overt predicate!", ]
    for idx, (sentence, target) in enumerate(zip(src, tgt)):
        perturbeds = tf.generate(sentence, target)
        test_cases.append({
            "class": tf.name(),
            "inputs": {"sentence": sentence, "target": target},
            "outputs": []}
        )
        for sentence, target in perturbeds:
            test_cases[idx]["outputs"].append({"sentence": sentence, "target": target})
    json_file = {"type": convert_to_snake_case(tf.name()), "test_cases": test_cases}
    print(json.dumps(json_file))