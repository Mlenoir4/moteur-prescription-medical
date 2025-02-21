from datetime import datetime
from prescription_validator.models import Patient, Prescription, Protocol, Medication
from prescription_validator.validator import PrescriptionValidator
from prescription_validator.exceptions import ValidationError
import unittest

class TestPrescriptionValidator(unittest.TestCase):
    def setUp(self):
        self.validator = PrescriptionValidator()
        self.validator.inventory = {
            "W": Medication("W", "MedicamentW", 10, emergency_reserve=3)
        }
        self.validator.protocols = {
            "GAMMA": Protocol("GAMMA", "Protocole Gamma", {})
        }
        
    def test_rule_801_normal_case(self):
        patient = Patient(
            id="P001",
            white_blood_cells=2500,
            genetic_markers=[]
        )
        prescription = Prescription(
            patient_id="P001",
            medications=["X"],
            protocol_code=None,
            prescription_date=datetime.now()
        )
        
        self.assertTrue(self.validator.validate_prescription(patient, prescription))
        
    def test_rule_801_low_wbc(self):
        patient = Patient(
            id="P001",
            white_blood_cells=1800,
            genetic_markers=[]
        )
        prescription = Prescription(
            patient_id="P001",
            medications=["X"],
            protocol_code=None,
            prescription_date=datetime.now()
        )
        
        with self.assertRaises(ValidationError):
            self.validator.validate_prescription(patient, prescription)

if __name__ == '__main__':
    unittest.main()