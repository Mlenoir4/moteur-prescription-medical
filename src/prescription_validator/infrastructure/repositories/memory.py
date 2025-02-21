from typing import Dict, Optional, List
from ...domain.models import Patient, Medication, Protocol, Prescription
from ...domain.ports.repositories import (
    PatientRepository,
    MedicationRepository,
    ProtocolRepository,
    PrescriptionRepository
)

class InMemoryPatientRepository(PatientRepository):
    def __init__(self):
        self.patients: Dict[str, Patient] = {}
        
    def get_by_id(self, patient_id: str) -> Optional[Patient]:
        return self.patients.get(patient_id)
        
    def save(self, patient: Patient) -> None:
        self.patients[patient.id] = patient

class InMemoryMedicationRepository(MedicationRepository):
    def __init__(self):
        self.medications: Dict[str, Medication] = {}
        
    def get_by_code(self, code: str) -> Optional[Medication]:
        return self.medications.get(code)
        
    def update_stock(self, code: str, new_stock: int) -> None:
        if code in self.medications:
            med = self.medications[code]
            med.stock_level = new_stock
            
    def get_all(self) -> List[Medication]:
        return list(self.medications.values())

class InMemoryProtocolRepository(ProtocolRepository):
    def __init__(self):
        self.protocols: Dict[str, Protocol] = {}
        
    def get_by_code(self, code: str) -> Optional[Protocol]:
        return self.protocols.get(code)

class InMemoryPrescriptionRepository(PrescriptionRepository):
    def __init__(self):
        self.prescriptions: Dict[str, Prescription] = {}
        
    def save(self, prescription: Prescription) -> None:
        self.prescriptions[prescription.id] = prescription
        
    def get_by_id(self, prescription_id: str) -> Optional[Prescription]:
        return self.prescriptions.get(prescription_id)