#!/usr/bin/env python
# coding: utf-8

# In[3]:


#install faker package
get_ipython().system(' pip install faker')


# In[3]:


from faker import Faker
import pandas as pd
fake = Faker()


# In[22]:


#fake word
print(fake.word())


# In[24]:


#fake job
print(fake.job())


# In[30]:


#fake number
print(fake.random_number(digits=4))


# In[23]:


#fake sentence
print(fake.sentence())


# In[28]:


#fake paragrpah
def generate_fake_paragraph():
    paragraph = ""
    for x in range(8):
        sentence = fake.sentence()
        paragraph += sentence + " "
    return paragraph
print(generate_fake_paragraph())


# In[4]:


#fake email
def generate_email():
    email = ""
    name = fake.name()
    number = str(fake.random_number(digits=2))
    email += name.replace(" ", "") + number + "@gmail.com"
    return email
print(generate_email())


# In[31]:


Faker.seed()
seed_value = 1234
fake.seed_instance(seed_value)

def generate_mid_sentence():
    mid_sentence = ""
    for x in range(2):
        sentence = fake.sentence()
        mid_sentence += sentence + " "
    return mid_sentence

def generate_fake_paragraph():
    paragraph = ""
    for x in range(8):
        sentence = fake.sentence()
        paragraph += sentence + " "
    return paragraph

def Riskscore():
    #Inherent Risk
    In_Likelihood = fake.random_element(elements=(1, 2, 3, 4, 5))
    In_Impact = fake.random_element(elements=(1, 2, 3, 4, 5))
    In_RiskScore = In_Likelihood * In_Impact
    In_Likelihood_Worded = map_likelihood(In_Likelihood)
    In_Impact_Worded = map_impact(In_Impact)
    
    #Residual Risk
    Re_Likelihood = fake.random_element(elements = range(1, In_Likelihood+1)) 
    Re_Impact = fake.random_element(elements = range(1, In_Impact+1)) 
    Re_RiskScore = Re_Likelihood * Re_Impact  
    Re_Likelihood_Worded = map_likelihood(Re_Likelihood)
    Re_Impact_Worded = map_impact(Re_Impact) 
    
    #Control Effectiveness
    Control_effect = In_RiskScore - Re_RiskScore
    Control_effect_Worded = map_Control(Control_effect)
    
                                    
    return In_Likelihood_Worded, In_Impact_Worded, In_RiskScore, Re_Likelihood_Worded, Re_Impact_Worded, Re_RiskScore, Control_effect_Worded

#Mapping score to words
def map_likelihood(score):
    if score == 1:
        return "1 - Rare"
    elif score == 2:
        return "2 - Unlikely"
    elif score == 3:
        return "3 - Possible"
    elif score == 4:
        return "4 - Likely"
    elif score == 5:
        return "5 - Almost Certain"
    
def map_impact(score):
    if score == 1:
        return "1 - Insignificant"
    elif score == 2:
        return "2 - Minor"
    elif score == 3:
        return "3 - Moderate"
    elif score == 4:
        return "4 - Major"
    elif score == 5:
        return "5 - Extreme"
    
def map_Control(score):
    if score <= 1:
        return "1 - None"
    elif score <= 4:
        return "2 - Mostly Ineffective"
    elif score <= 6:
        return "3 - Partially Effective"
    elif score <= 8:
        return "4 - Mostly Effective"
    elif score >= 9:
        return "5 - Fully Effective"

#Generate point form sentences
def generate_pointform():
    sentence1 = fake.sentence()
    sentence2 = fake.sentence()
    sentence3 = fake.sentence()
    sentence4 = fake.sentence()
    formatted_sentences = f" • {sentence1.capitalize()}\n • {sentence2.capitalize()}\n • {sentence3.capitalize()}\n • {sentence4.capitalize()}"
    return formatted_sentences

#Generate action plan sentence 
def generate_actionplan():
    sentence1 = fake.sentence()[0].lower() + fake.sentence()[1:]
    sentence2 = fake.sentence()[0].lower() + fake.sentence()[1:]
    formatted_sentences = f" • Additional {sentence1.capitalize()}\n • Additional {sentence2.capitalize()}"
    return formatted_sentences

#Generate the fake risk register
def create_risk(num_risk):
    risk_list = []
    for i in range(num_risk):
        risk = {}
        risk["Objective Category"] = fake.word()
        risk["Objective ID #"] = fake.random_number(digits=4) 
        risk["Objective/Goal"] = generate_mid_sentence()
        risk["Risk Rank"] = fake.random_element(elements=(1, 2, 3, 4, 5))
        risk["Risk Name"] = generate_mid_sentence()
        risk["Risk Description"] = generate_fake_paragraph()
        risk["Risk ID #"] = fake.random_number(digits=5) 
        risk["Risk Category"] = fake.random_element(elements=("Strategic", "Operational", "Financial", "Regulatory"))
        risk["Risk Sub-Category"] = fake.word() 
        risk["Risk Owner"] = fake.name()
        In_Likelihood_Worded, In_Impact_Worded, In_RiskScore, Re_Likelihood_Worded, Re_Impact_Worded, Re_RiskScore, Control_effect_Worded = Riskscore()
        risk["Inherent Likelihood"] = In_Likelihood_Worded
        risk["Inherent Impact"] = In_Impact_Worded
        risk["Inherent Risk Score"] = In_RiskScore
        risk["Control Effectiveness"] = Control_effect_Worded
        risk["Residual Likelihood"] = Re_Likelihood_Worded
        risk["Residual Impact"] = Re_Impact_Worded
        risk["Residual Risk Score"] = Re_RiskScore
        risk["Residual Within Appetite?"] = fake.random_element(elements=("Within", "Above", "Below"))
        risk["Root Causes"] = generate_pointform()
        risk["Pre-Event Mitigations (Controls)"] = generate_pointform()
        risk["Post-Event Mitigations"] = generate_pointform()
        risk["Consequences"] = generate_pointform()
        risk["Needed Action Plans"] = generate_actionplan()
        risk["Additional Notes"] = generate_fake_paragraph()
        risk_list.append(risk)
    return pd.DataFrame(risk_list)

#Number of risk in the fake risk register
risk_df = create_risk(300)  

# Save the DataFrame to a CSV file with explicit UTF-8 encoding
risk_df.to_csv('Fake_Risk_Register.csv', encoding='utf-8-sig', index=False)  # Use 'utf-8-sig' to ensure correct encoding for Excel

print("Data saved")

