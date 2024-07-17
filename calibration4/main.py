from datetime import datetime
from functools import reduce

from optapy import solver_factory_create
from optapy.types import SolverConfig, Duration

from constraints import define_constraints
from domain import DeviceSchedule, Device, generate_problem


def print_schedule(schedule: DeviceSchedule):
    technician_list = schedule.technician_list
    workstation_list = schedule.workstation_list
    task_list = schedule.device_list
    slot_task_map = dict()

    for task in task_list:
        if task.timeslot:
            if task.timeslot not in slot_task_map:
                slot_task_map[task.timeslot] = []
            slot_task_map[task.timeslot].append(task)

    # Print header row
    header_row = "| {:<10} |".format("Date")
    for tech in technician_list:
        header_row += " {:<10} |".format(tech.name)
    print("|" + "------------|" * (len(technician_list) + 1))
    print(header_row)
    print("|" + "------------|" * (len(technician_list) + 1))

    for slot in schedule.timeslot_list:
        # Extract the date and time from the start_time attribute
        start_date_time = datetime.combine(datetime(2024, 7, 1).date(), slot.start_time)
        date_str = start_date_time.strftime("%Y-%m-%d")
        time_str = start_date_time.strftime("%H:%M")
        day_str = slot.day_of_week

        # Print date
        out = "| {:<10} |".format(date_str)
        for _ in technician_list:
            out += " {:<10} |".format("")
        print(out)

        # Print time
        out = "| {:<10} |".format(time_str)
        for tech in technician_list:
            tasks = slot_task_map.get(slot, [])
            tech_tasks = [task for task in tasks if task.technician == tech]
            if len(tech_tasks) == 0:
                out += " {:<10} |".format("")
            else:
                out += " {:<10} |".format(reduce(lambda a, b: a + "," + b, map(lambda t: t.name, tech_tasks)))
        print(out)

        # Print day of week
        out = "| {:<10} |".format(day_str)
        for _ in technician_list:
            out += " {:<10} |".format("")
        print(out)

        # Print workstation
        out = "| {:<10} |".format("")
        for tech in technician_list:
            tasks = slot_task_map.get(slot, [])
            tech_tasks = [task for task in tasks if task.technician == tech]
            if len(tech_tasks) == 0:
                out += " {:<10} |".format("")
            else:
                out += " {:<10} |".format(
                    reduce(lambda a, b: a + "," + b, map(lambda t: t.workstation.name, tech_tasks)))
        print(out)

        # Print device type
        out = "| {:<10} |".format("")
        for tech in technician_list:
            tasks = slot_task_map.get(slot, [])
            tech_tasks = [task for task in tasks if task.technician == tech]
            if len(tech_tasks) == 0:
                out += " {:<10} |".format("")
            else:
                out += " {:<10} |".format(reduce(lambda a, b: a + "," + b, map(lambda t: t.type, tech_tasks)))
        print(out)

        # Print required skill
        out = "| {:<10} |".format("")
        for tech in technician_list:
            tasks = slot_task_map.get(slot, [])
            tech_tasks = [task for task in tasks if task.technician == tech]
            if len(tech_tasks) == 0:
                out += " {:<10} |".format("")
            else:
                out += " {:<10} |".format(reduce(lambda a, b: a + "," + b, map(lambda t: t.required_skill, tech_tasks)))
        print(out)

        # Print serial number
        out = "| {:<10} |".format("")
        for tech in technician_list:
            tasks = slot_task_map.get(slot, [])
            tech_tasks = [task for task in tasks if task.technician == tech]
            if len(tech_tasks) == 0:
                out += " {:<10} |".format("")
            else:
                out += " {:<10} |".format(reduce(lambda a, b: a + "," + b, map(lambda t: t.serial_number, tech_tasks)))
        print(out)

        # Print delivery date
        out = "| {:<10} |".format("")
        for tech in technician_list:
            tasks = slot_task_map.get(slot, [])
            tech_tasks = [task for task in tasks if task.technician == tech]
            if len(tech_tasks) == 0:
                out += " {:<10} |".format("")
            else:
                out += " {:<10} |".format(reduce(lambda a, b: a + "," + b, map(lambda t: t.delivery_date, tech_tasks)))
        print(out)

        print("|" + "------------|" * (len(technician_list) + 1))

    unassigned_tasks = list(filter(lambda
                                       unassigned_task: unassigned_task.timeslot is None or unassigned_task.technician is None or unassigned_task.workstation is None,
                                   task_list))
    if len(unassigned_tasks) > 0:
        print()
        print("Unassigned tasks")
        for task in unassigned_tasks:
            technician_name = task.technician.name if task.technician else "No Technician"
            workstation_name = task.workstation.name if task.workstation else "No Workstation"
            print(
                f" {task.name} - {technician_name} - {workstation_name} - {task.type} - {task.required_skill} - {task.serial_number} - {task.delivery_date}")

solver_config = SolverConfig().withEntityClasses(Device) \
    .withSolutionClass(DeviceSchedule) \
    .withConstraintProviderClass(define_constraints) \
    .withTerminationSpentLimit(Duration.ofSeconds(30))

solver = solver_factory_create(solver_config).buildSolver()

solution = solver.solve(generate_problem())

print_schedule(solution)

