"""EmergencyHandler — subsystem emergency assessment for workflows.py.

workflows.py calls:
    is_emergency, msg = handler.assess_subsystems(
        {"fuel_pressure_psi": 45.0}, {"bus_volts": 28.0})
Thresholds follow light-aircraft norms: fuel pressure below 15 psi or
bus voltage below 22 V is treated as an emergency condition.
"""


class EmergencyHandler:
    def __init__(self, min_fuel_pressure_psi: float = 15.0, min_bus_volts: float = 22.0):
        self.min_fuel_pressure_psi = min_fuel_pressure_psi
        self.min_bus_volts = min_bus_volts

    def assess_subsystems(self, engine: dict, electrical: dict) -> tuple[bool, str]:
        fuel_pressure = engine.get("fuel_pressure_psi", 0.0)
        if fuel_pressure < self.min_fuel_pressure_psi:
            return True, f"EMERGENCY: Fuel pressure critically low ({fuel_pressure} psi)"
        bus_volts = electrical.get("bus_volts", 0.0)
        if bus_volts < self.min_bus_volts:
            return True, f"EMERGENCY: Electrical bus undervoltage ({bus_volts} V)"
        return False, "Subsystems nominal"
