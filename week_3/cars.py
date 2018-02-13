# task 2, week 3

import csv
import sys
import os


class CarBase:
    """This class describes base types of machines"""
    def __init__(self, car_type, brand, photo_file_name, carrying):
        self.car_type = car_type
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying

    def get_photo_file_ext(self):
        """This method returns a format of a photo (.jpeg, .png, etc)"""
        tmp = os.path.splitext(str(self.photo_file_name))
        return tmp[1]

    def print_type(self):
        print(self.car_type)


class Car(CarBase):
    def __init__(self, car_type, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):

    def __init__(self, car_type, brand, photo_file_name, carrying, body_whl=""):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.body_whl = body_whl
        self.body_length = 0.0
        self.body_width = 0.0
        self.body_height = 0.0
        if self.body_whl:
            self._get_bodies_parameters()

    def _get_bodies_parameters(self):
        if self.body_whl:
            str_tmp = str(self.body_whl)
            parameters = str_tmp.split('x')
            self.body_length = float(parameters[0])
            self.body_width = float(parameters[1])
            self.body_height = float(parameters[2])

    def get_body_volume(self):
        if self.body_length and self.body_width and self.body_height:
            return self.body_length * self.body_width * self.body_height
        else:
            return 0.0


class SpecMachine(CarBase):
    def __init__(self, car_type, brand, photo_file_name, carrying, extra):
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        try:
            reader = csv.reader(csv_fd, delimiter=';')
            next(reader)  # пропускаем заголовок
            for row in reader:
                if row:
                    if row[0] == 'car':
                        if row[1] and row[2] and row[3] and row[5]:
                            car = Car(car_type=row[0],
                                      brand=row[1],
                                      passenger_seats_count=row[2],
                                      photo_file_name=row[3],
                                      carrying=row[5])
                            car_list.append(car)
                    elif row[0] == 'truck':
                        if row[1] and row[3] and row[5]:
                           truck = Truck(car_type=row[0],
                                         brand=row[1],
                                         photo_file_name=row[3],
                                         body_whl=row[4],
                                         carrying=row[5])
                           car_list.append(truck)
                    elif row[0] == 'spec_machine':
                        if row[1] and row[3] and row[5] and row[6]:
                            spec_machine = SpecMachine(car_type=row[0],
                                                       brand=row[1],
                                                       photo_file_name=row[3],
                                                       carrying=row[5],
                                                       extra=row[6])
                            car_list.append(spec_machine)
                    else:
                        pass
        except FileNotFoundError:
            print(csv_filename, "doesn't exists")
    return car_list


if __name__ == "__main__":
    csv_filename = sys.argv[1]
    cars = get_car_list(csv_filename)
    # print(len(cars))
    # for car in cars:
    #     car.print_type()
