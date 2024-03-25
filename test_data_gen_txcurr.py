import pandas as pd
import uuid
from random import choice, randint
from datetime import datetime, timedelta

# Define the districts of Botswana
districts = [
    "Central District",
    "Chobe District",
    "Ghanzi District",
    "Kgalagadi District",
    "Kgatleng District",
    "Kweneng District",
    "North-East District",
    "Ngamiland District",
    "South-East District",
    "Southern District"
]

# Key population abbreviations
key_population_abbreviations = {
    "Sex worker": "SW",
    "Men who have sex with men": "MSM",
    "Trans and gender-diverse people": "TGDP",
    "People who inject drugs": "PWID",
    "People living in prisons and other closed settings": "PLPCS"
}

# Gender valueset
gender_valueset = ["M", "F", "O", "U", "TM", "TF"]

# Function to generate a random date of birth
def random_dob(start_year=1920, end_year=2003):
    start = datetime(year=start_year, month=1, day=1)
    end = datetime(year=end_year, month=12, day=31)
    random_date = start + timedelta(days=randint(0, (end - start).days))
    return random_date.isoformat()[:10]

# Generate a random dataset row
def generate_random_row():
    patient_id = str(uuid.uuid4())
    gender = choice(gender_valueset)
    dob = random_dob()
    state = choice(districts)
    key_population_status = choice(list(key_population_abbreviations.values()))
    hiv_positive = choice([True, False])
    hiv_treatment = hiv_positive and choice([True, False]) # Treatment only if HIV positive
    deceased = hiv_positive and choice([True, False])
    stopped_art = hiv_positive and choice([True, False])
    return [patient_id, gender, dob, state, key_population_status, hiv_positive, hiv_treatment, deceased, stopped_art]

# Compute numerator and denominator based on the dataset
def compute_counts(df):
    df['Numerator'] = df.apply(
        lambda x: int(x['HIV_Positive'] and x['HIV_Treatment'] and not (x['Deceased'] or x['Stopped_ART'])),
        axis=1
    )
    df['Denominator (EST)'] = df.apply(
        lambda x: int(x['HIV_Positive'] and not (x['Deceased'] or x['Stopped_ART'])),
        axis=1
    )
    total_numerator = df['Numerator'].sum()
    total_denominator = df['Denominator (EST)'].sum()
    overall_indicator = total_numerator / total_denominator if total_denominator else 0
    return overall_indicator


# Main function to generate the dataset and write to an Excel file
def generate_dataset_and_excel(num_rows, file_name):
    rows = [generate_random_row() for _ in range(num_rows)]
    df = pd.DataFrame(rows, columns=[
        'Patient.ID', 'Patient.Gender', 'Patient.DOB', 'Patient.state (home)',
        'Key Population Status', 'HIV_Positive', 'HIV_Treatment', 'Deceased', 'Stopped_ART'
    ])
    overall_indicator = compute_counts(df)
    
    # Write the dataset to an Excel file
    with pd.ExcelWriter(file_name) as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
        pd.DataFrame([{'Overall Indicator': overall_indicator}]).to_excel(writer, index=False, sheet_name='Indicator')

    print(f'Dataset generated and written to {file_name}')

# Usage example
generate_dataset_and_excel(100, 'TX_CURR_Test_Data_Generated.xlsx')
