from datetime import datetime
from typing import Dict, Optional
from .models import Patient, Prescription, Protocol, Medication
from .rules import RuleEngine
from .exceptions import ValidationError

class PrescriptionValidator:
    def __init__(self):
        self.rule_engine = RuleEngine()
        self.inventory: Dict[str, Medication] = {}
        self.protocols: Dict[str, Protocol] = {}
        
    def validate_prescription(self, patient: Patient, prescription: Prescription) -> bool:
        protocol = self.protocols.get(prescription.protocol_code) if prescription.protocol_code else None
        for med in prescription.medications:
            if med not in self.inventory:
                raise ValidationError(f"Medication {med} not found in inventory")
            try:
                return self.rule_engine.validate_prescription(
                    patient=patient,
                    prescription=prescription,
                    protocol=protocol,
                    inventory=self.inventory
                )
            except ValidationError as e:
                raise
        