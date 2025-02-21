from abc import ABC, abstractmethod
from typing import Dict, Optional, Protocol
from .models import Patient, Prescription, Medication, Protocol
from ..application.exceptions import ValidationError

class Rule(ABC):
    def __init__(self, rule_id: str, description: str):
        self.rule_id = rule_id
        self.description = description
    
    @abstractmethod
    def validate(self, patient: Patient, prescription: Prescription,
                protocol: Optional[Protocol], inventory: Dict[str, Medication]) -> bool:
        pass

class WhiteBloodCellsRule(Rule):
    def __init__(self):
        super().__init__("801", "Validation du taux de globules blancs")
        
    def validate(self, patient: Patient, prescription: Prescription,
                protocol: Optional[Protocol], inventory: Dict[str, Medication]) -> bool:
        if "X" not in prescription.medications:
            return True
            
        threshold = 1500 if protocol and protocol.code == "GAMMA" else 2000
        
        if patient.relapse_date and patient.relapse_date.year >= 2019:
            return True
            
        if patient.white_blood_cells <= threshold:
            raise ValidationError(
                f"Règle 801: Taux de globules blancs insuffisant ({patient.white_blood_cells}/mm3 < {threshold}/mm3)"
            )
        return True

class DrugInteractionRule(Rule):
    def __init__(self):
        super().__init__("327", "Validation des interactions Y-Z")
        
    def validate(self, patient: Patient, prescription: Prescription,
                protocol: Optional[Protocol], inventory: Dict[str, Medication]) -> bool:
        has_y = "Y" in prescription.medications
        has_z = "Z" in prescription.medications
        
        if has_y and has_z:
            if "BRCA1" not in patient.genetic_markers:
                if not (prescription.prescription_date.weekday() == 2 and 
                       protocol and "IRM_SURVEILLANCE" in protocol.special_conditions):
                    raise ValidationError("Règle 327: Combinaison Y-Z non autorisée")
        return True

class EmergencyStockRule(Rule):
    def __init__(self):
        super().__init__("666", "Validation des stocks d'urgence")
        
    def validate(self, patient: Patient, prescription: Prescription,
                protocol: Optional[Protocol], inventory: Dict[str, Medication]) -> bool:
        if "W" in prescription.medications:
            med = inventory["W"]
            required_reserve = med.emergency_reserve
            if prescription.is_weekend:
                required_reserve *= (1 + med.weekend_safety_margin)
                
            if med.stock_level - 1 < required_reserve:
                raise ValidationError(
                    f"Règle 666: Stock insuffisant pour maintenir la réserve d'urgence"
                )
        return True