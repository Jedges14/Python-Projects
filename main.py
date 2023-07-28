import re
from fuzzywuzzy import fuzz
class Symmodel:
    def __init__(self):
        self.symptom_mapping = {
            'fever': ['common cold', 'flu', 'Malaria'],
            'cough': ['common cold', 'flu', 'pneumonia'],
            'headache': ['common cold', 'flu', 'migraine', 'Malaria'],
            'fatigue': ['common cold', 'flu', 'chronic fatigue syndrome', 'Malaria'],
            'sneezing': ['common cold'],
            'sore throat': ['common cold', 'Sore throat'],
            'itchy eyes': ['conjunctivitis'],
            'red eyes': ['conjunctivitis'],
            'watery stools': ['diarrhea', 'stomach flu'],
            'loss of appetite': ['Headache', 'Fever'],
            'ear pain': ['swimmer\'s ear'],
            'high body temperature': ['Fever'],
            'stroke': ['high Cholesterol'],
            'shortness of breath': ['asthma', 'pneumonia', 'heart_failure'],
            'chest pain': ['heart_attack', 'angina', 'pneumonia'],
            'abdominal pain': ['gastritis', 'appendicitis', 'gallstones'],
            'nausea': ['gastroenteritis', 'pregnancy', 'migraine'],
            'vomiting': ['gastroenteritis', 'food_poisoning', 'appendicitis'],
            'rash': ['allergic reaction', 'eczema', 'measles'],
            'joint pain': ['arthritis', 'gout', 'fibromyalgia'],
            'stiff neck': ['meningitis', 'muscle_strain'],
            'confusion': ['dementia', 'delirium', 'stroke'],
            'memory problems': ['alzheimer\'s', 'dementia'],
            'blurred vision': ['myopia', 'cataracts', 'glaucoma'],
            'numbness or tingling': ['peripheral_neuropathy', 'multiple_sclerosis'],
            'frequent urination': ['diabetes', 'urinary_tract_infection'],
            'blood in urine': ['urinary_tract_infection', 'kidney_stones'],
            'constipation': ['constipation', 'irritable_bowel_syndrome'],
            'unintended weight gain': ['hypothyroidism', 'polycystic_ovary_syndrome'],
            'night sweats': ['menopause', 'tuberculosis'],
            'jaundice': ['hepatitis', 'liver_disease'],
            'difficulty sleeping': ['insomnia', 'sleep_apnea'],
            'excessive thirst': ['diabetes', 'dehydration'],
            'excessive hunger': ['diabetes', 'hypoglycemia'],
            'changes in menstrual_cycle': ['menopause', 'polycystic_ovary_syndrome'],
            'hair loss': ['androgenetic alopecia', 'telogen_effluvium'],
            'difficulty_concentrating': ['attention_deficit_hyperactivity_disorder', 'anxiety'],
            'skin lesions or sores': ['dermatitis', 'herpes'],
            'swollen lymph nodes': ['infection', 'lymphoma'],
            'chronic cough': ['chronic_bronchitis', 'asthma'],
            'nightmares': ['post-traumatic_stress_disorder', 'anxiety'],
            'cold hands and feet': ['raynaud\'s_phenomenon', 'hypothyroidism'],
            'frequent infections': ['immune_deficiency', 'chronic_infections'],
            'muscle weakness': ['muscular_dystrophy', 'myasthenia gravis'],
            'easy bruising or bleeding': ['hemophilia', 'thrombocytopenia'],
            'pale skin': ['anemia', 'iron_deficiency'],
            'rapid heart rate': ['anxiety', 'atrial fibrillation'],
            'high blood pressure': ['hypertension', 'stress'],
            'low_blood_pressure': ['hypotension', 'dehydration'],
            'swollen joints': ['rheumatoid arthritis', 'osteoarthritis'],
            'sensitivity to light': ['migraine', 'photophobia'],
            'sensitivity to noise': ['hyperacusis', 'hearing loss'],
            'sensitivity to smells': ['migraine', 'allergic rhinitis'],
            'sensitivity to touch': ['fibromyalgia', 'hypersensitivity'],
            'seizures': ['epilepsy', 'febrile_seizures'],
            'tremors': ['essential_tremor', 'parkinson\'s disease'],
            'uncontrolled movements': ['dyskinesia', 'tourette syndrome'],
            'hallucinations': ['schizophrenia', 'delirium'],
            'delusions': ['psychosis', 'schizophrenia'],
            'mood swings': ['bipolar disorder', 'premenstrual syndrome'],
            'irritability': ['irritable bowel syndrome', 'depression'],
            'panic attacks': ['panic disorder', 'anxiety'],
            'short term memory loss': ['concussion', 'dementia'],
            'long term memory loss': ['alzheimer\'s', 'dementia'],
            'social withdrawal': ['depression', 'social anxiety disorder'],
            'loss of interest in activities': ['depression', 'anxiety'],
            'suicidal thoughts': ['depression', 'suicidal ideation'],
            'aggression': ['intermittent explosive disorder', 'bipolar disorder'],
            'agitation': ['anxiety', 'alzheimer\'s'],
            'anxiety': ['generalized anxiety disorder', 'panic disorder'],
            'depression': ['major depressive disorder', 'dysthymia'],
            'nausea and vomiting': ['gastroenteritis', 'motion_sickness', 'Malaria'],
            'abdominal bloating': ['irritable bowel syndrome', 'gas'],
            'sensitivity_to_certain_foods': ['food_intolerance', 'food_allergy'],
            'changes in bowel movements': ['irritable bowel syndrome', 'constipation'],
            'impotence': ['erectile dysfunction', 'low testosterone'],
            'loss of libido': ['low libido', 'relationship issues'],
            'pelvic_pain': ['pelvic_inflammatory_disease', 'endometriosis'],
            'vision_problems': ['myopia', 'cataracts', 'glaucoma'],
            'hearing_loss': ['sensorineural_hearing_loss', 'conductive_hearing_loss'],
            'loss_of_balance_or_coordination': ['vertigo', 'cerebellar_ataxia'],
            'excessive_sweating': ['hyperhidrosis', 'menopause'],
            'dry_mouth': ['xerostomia', 'dehydration'],
            'excessive_salivation': ['sialorrhea', 'dysphagia'],
            'joint_stiffness': ['osteoarthritis', 'rheumatoid_arthritis'],
            'excessive_gas': ['flatulence', 'lactose_intolerance'],
            'muscle_cramps': ['muscle_spasms', 'dehydration'],
            'Tooth pain': ['Tooth decay', 'Gingivitis'],
            'jaw pain' : ['Tooth decay', 'Migraine','Salivary gland infection', 'Rheumatoid Arthritis'],
            # more symptoms and corresponding diseases
        }

        # local dictionary
        self.disease_meanings = {
            'common_cold': 'A mild viral infection of the nose and throat.',
            'flu': 'A contagious respiratory illness caused by influenza viruses.',
            'pneumonia': 'An infection that inflames the air sacs in one or both lungs.',
            'migraine': 'A severe headache that can cause throbbing pain, often on one side of the head.',
            'chronic fatigue syndrome': 'A long-term, debilitating condition that causes extreme fatigue.',
            'asthma': 'A chronic condition that narrows and inflames the airways, leading to difficulty breathing.',
            'heart failure': 'A condition where the heart can\'t pump blood effectively, causing shortness of breath and fatigue.',
            'heart attack': 'A sudden blockage of blood flow to the heart, leading to chest pain and discomfort.',
            'angina': 'Chest pain or discomfort caused by reduced blood flow to the heart muscle.',
            'gastritis': 'Inflammation of the stomach lining, leading to stomach pain and discomfort.',
            'appendicitis': 'Inflammation of the appendix, causing severe abdominal pain and tenderness.',
            'gallstones': 'Hardened deposits in the gallbladder that can cause abdominal pain and digestive issues.',
            'gastroenteritis': 'An infection or inflammation of the stomach and intestines, causing nausea, vomiting, and diarrhea.',
            'food poisoning': 'Illness caused by consuming contaminated food, leading to vomiting and diarrhea.',
            'irritable bowel syndrome': 'A chronic disorder affecting the large intestine, causing abdominal pain and changes in bowel habits.',
            'allergic reaction': 'An immune system response to allergens, causing symptoms like itching, rash, and swelling.',
            'eczema': 'A chronic skin condition characterized by itchy and inflamed patches of skin.',
            'measles': 'A highly contagious viral infection causing fever, rash, and flu-like symptoms.',
            'arthritis': 'Inflammation of one or more joints, leading to pain, stiffness, and reduced mobility.',
            'gout': 'A type of arthritis that results from the buildup of uric acid crystals in joints, causing severe pain.',
            'fibromyalgia': 'A disorder characterized by widespread muscle pain, fatigue, and tender points on the body.',
            'Gingivitis' : 'A mild form of gum disease that causes irritation, redness, and swelling around the base of your teet',
            'Salivary Gland Infection' : 'this is bacteria caused inflation of the glands, leading to pain and swelling of jaw area',
            'Rheumatoid Arthritis' : ['An autoimune disease that primarily causes inflammation, pain, and stiffnes in joints including the jaw'],
            'Sore throat': 'Inflammation and irritation of the throat causing pain and discomfort.',
            'Conjunctivitis': 'Commonly known as pink eye, it is an infection or irritation of the eye, causing redness and discharge.',
            'Swimmer\'s ear': 'Infection of the outer ear canal, often caused by water remaining in the ear after swimming.',
            'High Cholesterol': 'A condition where there is too much cholesterol in the blood, which can increase the risk of heart disease.',
            'Chronic bronchitis': 'A long-term inflammation of the airways in the lungs, leading to cough and difficulty breathing.',
            'Tuberculosis': 'A bacterial infection that mainly affects the lungs, causing persistent cough, fever, and fatigue.',
            'Liver disease': 'Damage or inflammation of the liver, affecting its normal function.',
            'Hypothyroidism': 'A condition where the thyroid gland doesn\'t produce enough thyroid hormone, leading to fatigue and weight gain.',
            'Polycystic ovary syndrome': 'A hormonal disorder in women, often causing irregular periods and fertility issues.',
            'Menopause': 'The natural process in women when menstrual periods stop, typically accompanied by hormonal changes.',
            'Motion sickness': 'A feeling of nausea and dizziness when traveling in a vehicle or experiencing motion.',
            'Food intolerance': 'Difficulty digesting certain foods, leading to digestive discomfort and other symptoms.',
            'Flatulence': 'Excessive gas in the digestive system, leading to bloating and passing gas.',
            'Lactose intolerance': 'Inability to digest lactose, a sugar found in milk and dairy products, causing digestive issues.',
            'Tooth decay': 'Damage to the structure of teeth due to acid produced by bacteria, leading to cavities.',
            'Pelvic inflammatory disease': 'Infection of the female reproductive organs, causing pelvic pain and discomfort.',
            'Sensorineural hearing loss': 'Hearing loss due to damage to the inner ear or auditory nerve.',
            'Conductive hearing loss': 'Hearing loss due to problems in the outer or middle ear, preventing sound transmission.',
            'Vertigo': 'A sensation of dizziness and spinning, often caused by issues with the inner ear.',
            'Cerebellar ataxia': 'A neurological disorder affecting coordination and balance.',
            'Hyperhidrosis': 'Excessive sweating beyond what is necessary to regulate body temperature.',
            'Xerostomia': 'Dry mouth, caused by reduced saliva production.',
            'Sialorrhea': 'Excessive drooling or salivation.',
            'Muscle spasms': 'Involuntary contractions of muscles, often causing temporary pain or discomfort.',
            'Malaria' : 'A disease transmitted through mosquito bites, causing fever, chills, and body aches. It is caused by plasmodium parasites in the blood and can become severe if not treated promptly.',




            # Add more disease meanings
        }

    def get_diseases(self, symptoms):
        diseases = [self.symptom_mapping[symptom] for symptom in symptoms if symptom in self.symptom_mapping]
        return list(set(disease for sublist in diseases for disease in sublist))

    def print_diseases(self, symptoms):
        if symptoms:
            print('Here are possible diseases based on your listed symptoms:')
            for disease in self.get_diseases(symptoms):
                print("- " + disease)
        else:
            print("No matching diseases found for the given symptoms.")

    def get_disease_meaning(self, disease_name):
        return self.disease_meanings.get(disease_name, "Disease not found or no available definition.")

    def find_matching_symptoms(self, user_input, difflib_threshold=0.8, fuzzy_threshold=80):
        user_input_to_lower = user_input.lower()
        matching_symptoms = []

        # Check for exact and substring matches in symptom_mapping
        for symptom in self.symptom_mapping.keys():
            if user_input_to_lower in symptom.lower():
                matching_symptoms.append(symptom)

        # Use fuzzywuzzy for fuzzy string matching
        for symptom in self.symptom_mapping.keys():
            similarity = fuzz.token_set_ratio(user_input_to_lower, symptom.lower())
            if similarity >= fuzzy_threshold:
                matching_symptoms.append(symptom)

        return matching_symptoms

if __name__ == "__main__" :
    User_name = input('please enter your beautiful name: ')
    age = int(input('please enter your age (14-100 years): '))
    symp_model = Symmodel()

    attempts = 5
    while age < 14 or age > 100:
        print("invalid age")
        age = int(float(input('please enter your age again (14-100): ')))

    print('Don\'t worry, ' + User_name + ' we keep everything confidential')

    matching_symptoms = []
    while attempts > 0:
        symptoms = str(input(f'Hello, {User_name}! Please tell me what symptoms you are experiencing (space-separated): '))
        matching_symptoms = symp_model.find_matching_symptoms(symptoms.lower())

        if matching_symptoms:
            symp_model.print_diseases(matching_symptoms)
            break
        else:
            attempts -= 1
            if attempts > 0:
                print(f"No matching symptoms found. You have {attempts} {'attempts' if attempts > 1 else 'attempt'} remaining.")
            else:
                print('No matching symptoms found.')
                break

    if matching_symptoms:
        found_matching_symptoms = True
        while found_matching_symptoms:
            raw_disease_name = input('Enter the name of a disease to get its meaning (e.g., common cold): ')
            cleaned_disease_name = re.sub(r'\W', '', raw_disease_name).lower()
            meaning = symp_model.get_disease_meaning(cleaned_disease_name)
            print(f"Meaning of {raw_disease_name}: {meaning}")

            retry = input("Do you want to look up another disease meaning? (yes/no): ")
            if retry.lower() != "yes":
                break
    else:
        print("No matching symptoms found.")

