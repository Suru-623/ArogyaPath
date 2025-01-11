import pickle
import numpy as np
import pandas as pd
from constant.diseases_list import diseases_list
from constant.symptoms_dict import symptoms_dict

sym_des = pd.read_csv("datasets/symtoms_df.csv")
precautions = pd.read_csv("datasets/precautions_df.csv")
workout = pd.read_csv("datasets/workout_df.csv")
description = pd.read_csv("datasets/description.csv")
medications = pd.read_csv('datasets/medications.csv')
diets = pd.read_csv("datasets/diets.csv")

svc = pickle.load(open('models/svc.pkl', 'rb'))

def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    med = medications[medications['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    die = diets[diets['Disease'] == dis]['Diet']
    die = [die for die in die.values]

    wrkout = workout[workout['disease'] == dis]['workout']

    return desc, pre, med, die, wrkout


def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    print(f'line 50:------------> {patient_symptoms}')

    # Flag to track if any valid symptom was found
    valid_symptom_found = False
    valid_symptoms = []

    for item in patient_symptoms:
        # Check if the symptom is in the dictionary
        if item.lower() in symptoms_dict:
            input_vector[symptoms_dict[item.lower()]] = 1
            valid_symptoms.append(item)
            valid_symptom_found = True
        else:
            print(f"************* Symptom '{item}' not found in symptoms_dict")

    # If no valid symptoms were found, return None
    if not valid_symptom_found:
        return None, None

    # Return predicted disease if valid symptoms were found
    return diseases_list[svc.predict([input_vector])[0]], valid_symptoms
