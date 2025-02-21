from abc import ABC, abstractmethod
from typing import Optional, List
from ..models import Patient, Medication, Protocol, Prescription

class PatientRepository(ABC):
    @abstractmethod
    def get_by_id(self, patient_id: str) -> Optional[Patient]:
        pass

    @abstractmethod
    def save(self, patient: Patient) -> None:
        pass

class MedicationRepository(ABC):
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Medication]:
        pass

    @abstractmethod
    def update_stock(self, code: str, new_stock: int) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Medication]:
        pass

class ProtocolRepository(ABC):
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Protocol]:
        pass

class PrescriptionRepository(ABC):
    @abstractmethod
    def save(self, prescription: Prescription) -> None:
        pass

    @abstractmethod
    def get_by_id(self, prescription_id: str) -> Optional[Prescription]:
        pass