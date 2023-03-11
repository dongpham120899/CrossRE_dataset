import os
import json
# from src.preprocessing import read_json_file
import numpy as np

relation_mapping = {"compare":"Compare", "usage":"Used-for", "part-of":"Part-of", "type-of":"Feature-of", "cause-effect":"Evaluate-for", "named":"Hyponym-of"}

def convert_format(path, saved_path, mapping=True):
    data = []
    with open(path, "r") as file:
        list_entity_types = []
        list_rel_type = []

        for json_elem in file:
            document = json.loads(json_elem)
            # print(document)

            new_entities = []
            entities_dic = {}
            for idx,entity in enumerate(document['ner']):
                if mapping:
                    new_entity = dict(type="OtherScientificTerm", start=entity[0], end=entity[1])
                else:
                    new_entity = dict(type=entity[2], start=entity[0], end=entity[1])
                new_entities.append(new_entity)
                entities_dic[str(entity[0])+"-"+str(entity[1])] = idx
                # print(entity)
                list_entity_types.append(entity[2])

            new_relations = []
            for relation in document['relations']:
                # print(relation)
                # en
                entity_1 = entities_dic[str(relation[0])+"-"+str(relation[1])]
                entity_2 = entities_dic[str(relation[2])+"-"+str(relation[3])]
                rel_type = relation[4]
                if mapping:
                    if rel_type in relation_mapping.keys():
                        new_relation = dict(type=relation_mapping[rel_type], head=entity_1, tail=entity_2)
                    else:
                        continue
                        
                else:
                    new_relation = dict(type=rel_type, head=entity_1, tail=entity_2)
                new_relations.append(new_relation)
                list_rel_type.append(rel_type)
            new_doc = dict(tokens=document['sentence'], entities=new_entities, relations=new_relations, orig_id=document["doc_key"])


            data.append(new_doc)
            # break

        print("Entity types/:", np.unique(list_entity_types))
        print("Relation types:", np.unique(list_rel_type))
        print("****************************")

    if saved_path:
        with open(saved_path, "w") as file:
            json.dump(data, file)
    
    return data


if __name__ == "__main__":
    # label_types = {label: idx for idx, label in enumerate(os.getenv(f"RELATION_LABELS").split())}

    ai_train_path = "crossre_data/ai-train.json"
    ai_train_saved_path = "spert_format/ai-train.json"

    ai_dev_path = "crossre_data/ai-dev.json"
    ai_dev_saved_path = "spert_format/ai-dev.json"

    ai_test_path = "crossre_data/ai-test.json"
    ai_test_saved_path = "spert_format/ai-test.json"
    # sentences, entities_1, entities_2, relations = read_json_file(ai_train_path, label_types)
    # print(sentences[0], entities_1[0], entities_2[0], relations[0])
    train_data = convert_format(ai_train_path, ai_train_saved_path)
    dev_data = convert_format(ai_dev_path, ai_dev_saved_path)
    test_data = convert_format(ai_test_path, ai_test_saved_path)
    # print(train_data[0])