from datetime import datetime
from prescription_validator.models import Patient, Prescription
from prescription_validator.validator import PrescriptionValidator
from prescription_validator.exceptions import ValidationError

def main():
    validator = PrescriptionValidator()
    
    patient = Patient(
        id="P001",
        white_blood_cells=2500,
        genetic_markers=["BRCA1"],
        relapse_date=None
    )
    
    prescription = Prescription(
        patient_id="P001",
        medications=["X", "Y"],
        protocol_code="GAMMA",
        prescription_date=datetime.now(),
        is_weekend=False
    )
    
    try:
        is_valid = validator.validate_prescription(patient, prescription)
        print(f"Prescription validée avec succès: {is_valid}")
        
    except ValidationError as e:
        print(f"Erreur de validation: {str(e)}")

if __name__ == "__main__":
    main()