from datetime import datetime
import uuid
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import unittest
from prescription_validator.domain.models import Patient, Prescription, Protocol, Medication
from prescription_validator.application.services import PrescriptionValidationService
from prescription_validator.application.exceptions import ValidationError
from prescription_validator.infrastructure.repositories.memory import (
    InMemoryPatientRepository,
    InMemoryMedicationRepository,
    InMemoryProtocolRepository,
    InMemoryPrescriptionRepository
)

class TestPrescriptionValidation(unittest.TestCase):
    def setUp(self):
        self.patient_repo = InMemoryPatientRepository()
        self.medication_repo = InMemoryMedicationRepository()
        self.protocol_repo = InMemoryProtocolRepository()
        self.prescription_repo = InMemoryPrescriptionRepository()
        
        self.service = PrescriptionValidationService(
            self.patient_repo,
            self.medication_repo,
            self.protocol_repo,
            self.prescription_repo
        )
        
        self.patient = Patient(
            id="P001",
            white_blood_cells=2500,
            genetic_markers=["BRCA1"]
        )
        self.patient_repo.save(self.patient)
        
        self.medication_w = Medication(
            code="W",
            name="MedicamentW",
            stock_level=10,
            emergency_reserve=3
        )
        self.medication_repo.medications["W"] = self.medication_w
        
        self.protocol = Protocol(
            code="GAMMA",
            name="Protocole Gamma",
            special_conditions={}
        )
        self.protocol_repo.protocols["GAMMA"] = self.protocol
        
    def test_valid_prescription(self):
        prescription = Prescription(
            id=str(uuid.uuid4()),
            patient_id="P001",
            medications=["X"],
            protocol_code=None,
            prescription_date=datetime.now()
        )
        
        self.assertTrue(self.service.validate_prescription(prescription))
        
    def test_invalid_white_blood_cells(self):
        self.patient.white_blood_cells = 1800
        self.patient_repo.save(self.patient)
        
        prescription = Prescription(
            id=str(uuid.uuid4()),
            patient_id="P001",
            medications=["X"],
            protocol_code=None,
            prescription_date=datetime.now()
        )
        
        with self.assertRaises(ValidationError):
            self.service.validate_prescription(prescription)

if __name__ == '__main__':
    unittest.main()