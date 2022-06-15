import json
from collections import defaultdict
import re


class BusException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class Bus:
    buses = set()
    stops = defaultdict(int)  # stop_name: number of buses that use the stop

    def __init__(self, bus_id):
        self.id = bus_id
        self.start = None
        self.transfer = []
        self.finish = None
        self.current_arrival_time = (0, 0)
        Bus.buses.add(bus_id)

    def set_current_stop(self, stop_name, arrival_time):
        arrival_time = arrival_time.split(':')
        arrival_time = int(arrival_time[0]), int(arrival_time[1])

        if arrival_time < self.current_arrival_time:
            raise BusException(f"bus_id line {self.id}: wrong time on station {stop_name}")

        self.current_arrival_time = arrival_time

    def set_start(self, stop_name):
        if self.start:
            raise BusException
        self.start = stop_name

    def set_finish(self, stop_name):
        if self.finish:
            raise BusException(f"There is not start or end stop for the line: {self.id}.")
        self.finish = stop_name

    def add_stop(self, stop_name):
        Bus.stops[stop_name] += 1

    def is_proper(self):
        return bool(self.start and self.finish)


error_dict = defaultdict(int)


def error_check(data):
    for obj in data:
        if type(obj['bus_id']) != int:
            error_dict['bus_id'] += 1
        if type(obj['stop_id']) != int:
            error_dict['stop_id'] += 1
        if type(obj['stop_name']) != str or not re.match('^[A-Z].*((Road)|(Avenue)|(Boulevard)|(Street))$', obj['stop_name']):
            error_dict['stop_name'] += 1
        if type(obj['next_stop']) != int:
            error_dict['next_stop'] += 1
        if type(obj['stop_type']) != str or not re.match('^[SOF]?$', obj['stop_type']):
            error_dict['stop_type'] += 1
        if type(obj['a_time']) != str or not re.match(r'^(([01]\d)|(2[0123])):[012345]\d$', obj['a_time']):
            error_dict['a_time'] += 1


def stage4():
    start_stops = set()
    finish_stops = set()
    bus_line = {}

    data = json.loads(input())
    for field in data:
        bus_id = field['bus_id']
        stop_name = field['stop_name']
        stop_type = field['stop_type']

        if bus_id not in Bus.buses:
            bus_line[bus_id] = Bus(bus_id)

        if stop_type == 'S':
            try:
                bus_line[bus_id].set_start(stop_name)
            except BusException as e:
                print(e)
                break
            start_stops.add(stop_name)

        elif stop_type == 'F':
            try:
                bus_line[bus_id].set_finish(stop_name)
            except BusException as e:
                print(e)
                break
            finish_stops.add(stop_name)

        bus_line[bus_id].add_stop(stop_name)

    else:
        for bus_id in bus_line:
            if not bus_line[bus_id].is_proper():
                print(f"There is no start or end stop for the line: {bus_id}.")
                quit()

    transfer_stops = set()
    for stop in Bus.stops:
        if Bus.stops[stop] > 1:
            transfer_stops.add(stop)

    print(f"Start stops: {len(start_stops)} {sorted(start_stops)}")
    print(f"Transfer stops: {len(transfer_stops)} {sorted(transfer_stops)}")
    print(f"Finish stops: {len(finish_stops)} {sorted(finish_stops)}")


def stage5():
    bus_line = {}
    error_messages = defaultdict(str)

    data = json.loads(input())
    for field in data:
        bus_id = field['bus_id']
        stop_name = field['stop_name']
        arrival_time = field['a_time']

        if bus_id not in Bus.buses:
            bus_line[bus_id] = Bus(bus_id)

        try:
            bus_line[bus_id].set_current_stop(stop_name, arrival_time)
        except BusException as e:
            if error_messages[bus_id] == '':
                error_messages[bus_id] = str(e)
            continue

    print("Arrival time test:")
    if len(error_messages):
        print(*error_messages.values(), sep='\n')
    else:
        print('OK')


def stage6():
    on_demand_stops = set()

    data = json.loads(input())
    for field in data:
        stop_type = field['stop_type']
        stop_name = field['stop_name']

        Bus.stops[stop_name] += 1

        if stop_type == 'O':
            on_demand_stops.add(stop_name)

    transfer_stops = []
    for stop in Bus.stops:
        if Bus.stops[stop] > 1:
            transfer_stops.append(stop)

    illegal_stops = []  # both on demand and transfer
    for stop in transfer_stops:
        if stop in on_demand_stops:
            illegal_stops.append(stop)

    print("On demand stops test:")
    if len(illegal_stops):
        print(f"Wrong stop type: {sorted(illegal_stops)}")
    else:
        print("OK")


if __name__ == '__main__':
    stage6()

