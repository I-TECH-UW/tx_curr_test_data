import os
import json
import pandas as pd
import argparse
from pathlib import Path
from fhir_generator import generate_patient_bundle
from fhirclient import send_to_fhir_server

def main(input_file, start_date, end_date, output_mode, fhir_server_url):
    df = pd.read_excel(input_file, sheet_name=0)  # Adjust sheet_name as necessary

    # Create the output directory if it does not exist and if local output is needed
    if output_mode in ['local', 'both'] and not os.path.exists('output'):
        os.makedirs('output')

    for i, row in df.iterrows():
        patient_bundle = generate_patient_bundle(row.to_dict(), start_date, end_date)

        if output_mode in ['local', 'both']:
            # Output each patient bundle as a separate JSON file
            Path(f'output/patient_bundle_{i+1}.json').write_text(patient_bundle.json())

        if output_mode in ['server', 'both']:
            # Send each patient bundle to the FHIR server
            send_to_fhir_server(patient_bundle, fhir_server_url)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate FHIR patient bundles from an Excel file.')
    parser.add_argument('input_file', help='The Excel file containing the patient data.')
    parser.add_argument('--start_date', help='The start of the measurement period (inclusive).')
    parser.add_argument('--end_date', help='The end of the measurement period (inclusive).')
    parser.add_argument('--output', help='Output mode: local, server, both', default='local')
    parser.add_argument('--fhir-server-url', help='FHIR server URL', default='http://localhost:8080/fhir/')
    
    args = parser.parse_args()
    main(args.input_file, args.start_date, args.end_date, args.output, args.fhir_server_url)
