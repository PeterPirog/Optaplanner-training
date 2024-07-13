import datetime
from datetime import time

import optapy
from optapy import problem_fact, planning_id, planning_entity, planning_variable, \
    planning_solution, planning_entity_collection_property, \
    problem_fact_collection_property, value_range_provider, planning_score
from optapy.types import HardSoftScore

@problem_fact
class Technician:
    id: int
    name: str
    skills: set

    def __init__(self, id, name, skills):
        self.id = id
        self.name = name
        self.skills = skills

    @planning_id
    def get_id(self):
        return self.id

    def has_skill(self, skill):
        return skill in self.skills

    def __str__(self):
        return f"Technician(id={self.id}, name={self.name}, skills={self.skills})"

@problem_fact
class Workstation:
    id: int
    name: str
    supported_device_types: set

    def __init__(self, id, name, supported_device_types):
        self.id = id
        self.name = name
        self.supported_device_types = supported_device_types

    @planning_id
    def get_id(self):
        return self.id

    def supports_device_type(self, device_type):
        return device_type in self.supported_device_types

    def __str__(self):
        return f"Workstation(id={self.id}, name={self.name}, supported_device_types={self.supported_device_types})"

@problem_fact
class Timeslot:
    id: int
    day_of_week: str
    start_time: time
    end_time: time

    def __init__(self, id, day_of_week, start_time, end_time):
        self.id = id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time

    @planning_id
    def get_id(self):
        return self.id

    def __str__(self):
        return (
            f"Timeslot("
            f"id={self.id}, "
            f"day_of_week={self.day_of_week}, "
            f"start_time={self.start_time}, "
            f"end_time={self.end_time})"
        )

@planning_entity
class Device:
    id: int
    name: str
    type: str
    required_skill: str
    serial_number: str
    technician: Technician
    workstation: Workstation
    timeslot: Timeslot

    def __init__(self, id, name, type, required_skill, serial_number, technician=None, workstation=None, timeslot=None):
        self.id = id
        self.name = name
        self.type = type
        self.required_skill = required_skill
        self.serial_number = serial_number
        self.technician = technician
        self.workstation = workstation
        self.timeslot = timeslot

    @planning_id
    def get_id(self):
        return self.id

    @planning_variable(Timeslot, ["timeslotRange"])
    def get_timeslot(self):
        return self.timeslot

    def set_timeslot(self, new_timeslot):
        self.timeslot = new_timeslot

    @planning_variable(Technician, ["technicianRange"])
    def get_technician(self):
        return self.technician

    def set_technician(self, new_technician):
        self.technician = new_technician

    @planning_variable(Workstation, ["workstationRange"])
    def get_workstation(self):
        return self.workstation

    def set_workstation(self, new_workstation):
        self.workstation = new_workstation

    def __str__(self):
        return (
            f"Device("
            f"id={self.id}, "
            f"name={self.name}, "
            f"type={self.type}, "
            f"required_skill={self.required_skill}, "
            f"serial_number={self.serial_number}, "
            f"technician={self.technician}, "
            f"workstation={self.workstation}, "
            f"timeslot={self.timeslot}"
            f")"
        )

@planning_solution
class DeviceSchedule:
    timeslot_list: list[Timeslot]
    technician_list: list[Technician]
    workstation_list: list[Workstation]
    device_list: list[Device]
    score: HardSoftScore

    def __init__(self, timeslot_list, technician_list, workstation_list, device_list, score=None):
        self.timeslot_list = timeslot_list
        self.technician_list = technician_list
        self.workstation_list = workstation_list
        self.device_list = device_list
        self.score = score

    @problem_fact_collection_property(Timeslot)
    @value_range_provider("timeslotRange")
    def get_timeslot_list(self):
        return self.timeslot_list

    @problem_fact_collection_property(Technician)
    @value_range_provider("technicianRange")
    def get_technician_list(self):
        return self.technician_list

    @problem_fact_collection_property(Workstation)
    @value_range_provider("workstationRange")
    def get_workstation_list(self):
        return self.workstation_list

    @planning_entity_collection_property(Device)
    def get_device_list(self):
        return self.device_list

    @planning_score(HardSoftScore)
    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def __str__(self):
        return (
            f"DeviceSchedule("
            f"timeslot_list={self.timeslot_list},\n"
            f"technician_list={self.technician_list},\n"
            f"workstation_list={self.workstation_list},\n"
            f"device_list={self.device_list},\n"
            f"score={self.score}"
            f")"
        )

# Function to generate a problem instance
def generate_problem():
    timeslot_list = [
        Timeslot(i, day, time(hour), time(hour + 1))
        for i, (day, hour) in enumerate(
            [(day, hour) for day in ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"] for hour in range(7, 15)], 1
        )
    ]
    technician_list = [
        Technician(1, "John", {"skill1", "skill2"}),
        Technician(2, "Doe", {"skill1"}),
        Technician(3, "Smith", {"skill1", "skill2"})
    ]
    workstation_list = [
        Workstation(1, "WS1", {"type1"}),
        Workstation(2, "WS2", {"type2"}),
        Workstation(3, "WS3", {"type1", "type2"})
    ]
    device_list = [
        Device(1, "Device1", "type1", "skill1", "SN1"),
        Device(2, "Device2", "type1", "skill1", "SN2"),
        Device(3, "Device3", "type2", "skill2", "SN3"),
        Device(4, "Device4", "type2", "skill2", "SN4"),
        Device(5, "Device5", "type1", "skill1", "SN5"),
        Device(6, "Device6", "type1", "skill1", "SN6"),
        Device(7, "Device7", "type2", "skill2", "SN7"),
        Device(8, "Device8", "type2", "skill2", "SN8"),
        Device(9, "Device9", "type1", "skill1", "SN9"),
        Device(10, "Device10", "type2", "skill2", "SN10")
    ]
    return DeviceSchedule(timeslot_list, technician_list, workstation_list, device_list)
