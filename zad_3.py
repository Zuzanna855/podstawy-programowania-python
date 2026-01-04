class Property:
    def __init__(self, area, rooms: int, price, address):
        self.area = area
        self.rooms = rooms
        self.price = price
        self.address = address
    def __str__(self):
        return (
            f'Property: \n'
            f'Area: {self.area}\n'
            f'Rooms: {self.rooms}\n'
            f'Price: {self.price}\n'
            f'Address: {self.address}\n'
        )


class House(Property):
    def __init__(self, area, rooms: int, price, address, plot: int):
        super().__init__(area, rooms, price, address)
        self.plot = plot
    def __str__(self):
        return (
            f'House: \n'
            f'Area: {self.area}\n'
            f'Rooms: {self.rooms}\n'
            f'Price: {self.price}\n'
            f'Address: {self.address}\n'
            f'Plot: {self.plot}\n'
        )


class Flat(Property):
    def __init__(self, area, rooms: int, price, address, floor):
        super().__init__(area, rooms, price, address)
        self.floor = floor
    def __str__(self):
        return (
            f'Flat: \n'
            f'Area: {self.area}\n'
            f'Rooms: {self.rooms}\n'
            f'Price: {self.price}\n'
            f'Address: {self.address}\n'
            f'Floor: {self.floor}\n'
        )


house1 = House('Los Angeles', 3, '40 000 000', 'Mulholland Dr. 37', 200)
flat1 = Flat('New York', 5, '50 000 000', '5th Avenue', '15')

print(house1)
print(flat1)


