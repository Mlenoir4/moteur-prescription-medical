from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Patient:
    id: str
    white_blood_cells: float
    genetic_markers: List[str]
    relapse_date: Optional[datetime] = None

@dataclass
class Medication:
    code: str
    name: str
    stock_level: int
    emergency_reserve: int = 3
    weekend_safety_margin: float = 0.2

@dataclass
class Protocol:
    code: str
    name: str
    special_conditions: dict

@dataclass
class Prescription:
    id: str
    patient_id: str
    medications: List[str]
    protocol_code: Optional[str]
    prescription_date: datetime
    is_weekend: bool = False