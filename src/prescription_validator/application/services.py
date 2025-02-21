from ..domain.models import Prescription
from ..domain.ports.repositories import (
    PatientRepository,
    MedicationRepository,
    ProtocolRepository,
    PrescriptionRepository
)
from ..domain.rules import WhiteBloodCellsRule, DrugInteractionRule, EmergencyStockRule
from .exceptions import ValidationError

class PrescriptionValidationService:
    def __init__(
        self,
        patient_repository: PatientRepository,
        medication_repository: MedicationRepository,
        protocol_repository: ProtocolRepository,
        prescription_repository: PrescriptionRepository
    ):
        self.patient_repository = patient_repository
        self.medication_repository = medication_repository
        self.protocol_repository = protocol_repository
        self.prescription_repository = prescription_repository
        self.rules = [
            WhiteBloodCellsRule(),
            DrugInteractionRule(),
            EmergencyStockRule()
        ]
    
    def validate_prescription(self, prescription: Prescription) -> bool:
        patient = self.patient_repository.get_by_id(prescription.patient_id)
        if not patient:
            raise ValidationError(f"Patient {prescription.patient_id} non trouvé")
            
        protocol = None
        if prescription.protocol_code:
            protocol = self.protocol_repository.get_by_code(prescription.protocol_code)
            
        inventory = {
            med.code: med for med in self.medication_repository.get_all()
        }
        
        for rule in self.rules:
            rule.validate(patient, prescription, protocol, inventory)
            
        self.prescription_repository.save(prescription)
        return True