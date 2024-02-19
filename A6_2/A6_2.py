# hotel.py

import os
import json
from datetime import datetime
"""
    Represents a hotel.

    Attributes:
        name (str): The name of the hotel.
        location (str): The location of the hotel.
        rooms (int): The number of rooms available
       in the hotel.
        reservations (list): A list of reservations made 
        at the hotel.
"""

class Hotel:
    

    def __init__(self, name, location, rooms):
        """
        Initialize a Hotel object.

        Args:
            name (str): The name of the hotel.
            location (str): The location of the hotel.
            rooms (int): The number of rooms 
            available in the hotel.
        """
        self.name = name
        self.location = location
        self.rooms = rooms
        self.reservations = []

    """
    Add a reservation to the hotel.

    Args:
    reservation (Reservation): The reservation to be added.
    """
    def add_reservation(self, reservation):
        self.reservations.append(reservation)
        self.rooms -= reservation.num_rooms

    def remove_reservation(self, reservation):
        """
        Remove a reservation from the hotel.

        Args:
            reservation (Reservation): The
           reservation to be removed.
        """
        self.reservations.remove(reservation)
        self.rooms += reservation.num_rooms

    def display_info(self):
        """Display information about the hotel."""
        return f"Name: {self.name}, Location: {self.location}, \
        Rooms: {self.rooms}"

    def update_info(self, name=None, location=None, rooms=None):
        """Update hotel information."""
        if name:
            self.name = name
        if location:
            self.location = location
        if rooms:
            self.rooms = rooms

    def save_to_json(self, filename):
        """Serialize the hotel object to JSON and 
        write to a file."""
        with open(filename, 'a') as f:
            f.write(json.dumps(self.__dict__) + '\n')

    @classmethod
    def load_from_json(cls, filename):
        """Load a hotel object from JSON data in a file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                return cls(data['name'], data['location'], data['rooms'])
        except FileNotFoundError:
            return None

#customer.py
#import json

class Customer:
    def __init__(self, name, email):
        """Initialize a Customer object."""
        self.name = name
        self.email = email

    def to_dict(self):
        """Convert customer object to a dictionary."""
        return {"name": self.name, "email": self.email}

    @classmethod
    def save_to_json(cls, customers, filename):
        """Serialize the list of customer objects to \
        JSON and write to a file."""
        customer_data = [customer.to_dict() for customer in customers]

        try:
            with open(filename, 'r+') as f:
                data = json.load(f)
                data.extend(customer_data)
                f.seek(0)
                json.dump(data, f, indent=4)
        except FileNotFoundError:
            with open(filename, 'w') as f:
                json.dump(customer_data, f, indent=4)


    @classmethod
    def load_from_json(cls, filename):
        """Load a list of customer objects from JSON data in a file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                customers = [cls(customer['name'], customer['email']) \
                             for customer in data]
                return customers
        except FileNotFoundError:
            return []

    @staticmethod
    def display_customer_info(customers):
        """Display information about customers."""
        if customers:
            print("Customer Information:")
            for i, customer in enumerate(customers, start=1):
                print(f"{i}. Name: {customer.name}, \
                Email: {customer.email}")
        else:
            print("No customers found.")

    @staticmethod
    def find_customer(customers, name):
        """Find a customer by name."""
        for customer in customers:
            if customer.name == name:
                return customer
        return None

    @staticmethod
    def delete_customer(customers, name):
        """Delete a customer by name."""
        for i, customer in enumerate(customers):
            if customer.name == name:
                del customers[i]
                return True
        return False

    @staticmethod
    def modify_customer_info(customer, new_name=None, new_email=None):
        """Modify customer information."""
        if new_name:
            customer.name = new_name
        if new_email:
            customer.email = new_email

# reservation.py

#import json
#from datetime import datetime

class Reservation:
    def __init__(self, customer, hotel, num_rooms):
        """Initialize a Reservation object."""
        self.customer = customer
        self.hotel = hotel
        self.num_rooms = num_rooms
        self.reservation_date = datetime.now().strftime\
         ('%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        """Convert reservation object to a dictionary."""
        return {
            "customer": self.customer.to_dict(),
            "hotel": {"name": self.hotel.name, "location": \
                      self.hotel.location},
            "num_rooms": self.num_rooms,
            "reservation_date": self.reservation_date
        }

    def save_to_json(self, filename):
        """Serialize the reservation object to JSON and write \
        to a file."""
        with open(filename, 'a') as f:
            json.dump(self.to_dict(), f)
            f.write('\n')

    @classmethod
    def load_from_json(cls, filename):
        """Load a reservation object from JSON data in a file."""
        reservations = []
        try:
            with open(filename, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    customer = Customer.load_from_json\
                     (data['customer']['name'])
                    hotel = Hotel.load_from_json(data['hotel']['name'])
                    reservation = cls(customer, hotel, data['num_rooms'])
                    reservations.append(reservation)
        except FileNotFoundError:
            pass
        return reservations

#hotelManager.py
#import json
#from datetime import datetime

class HotelManager:
    """Class to manage hotel information including creation, 
    deletion, modification, and reservation."""

    def __init__(self, hotels_file, customers_file, \
                 reservations_file):
        """
    Initialize HotelManager with file paths for hotels, customers,
   and reservations.

    Args:
    hotels_file (str): File path for storing hotel information.
    customers_file (str): File path for storing customer information.
    reservations_file (str): File path for storing reservation information.
    """
        self.hotels_file = hotels_file
        self.customers_file = customers_file
        self.reservations_file = reservations_file

    def get_hotels(self):
        """
        Retrieve hotel information from the file.

        Returns:
            list: List of dictionaries representing hotel information.
        """
        hotels = []
        try:
            with open(self.hotels_file, 'r') as f:
                hotels = json.load(f)
        except FileNotFoundError:
            pass
        return hotels

    def display_available_hotels(self):
        """
        Display available hotels with their information.
        """
        hotels = self.get_hotels()
        if hotels:
            print("Available Hotels:")
            for i, hotel in enumerate(hotels, start=1):
                print(f"{i}. {hotel['name']} - \
                {hotel['location']} ({hotel['rooms']} rooms)")
        else:
            print("No hotels available.")

    def manage_hotels(self):
        """Options to choose from"""
        while True:
            print("\nManage Hotels")
            print("a. Create Hotel")
            print("b. Delete Hotel")
            print("c. Display Hotel Information")
            print("d. Modify Hotel Information")
            print("e. Reserve a Room")
            print("f. Cancel a Reservation")
            print("g. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == 'a':
                self.create_hotel()
            elif choice == 'b':
                self.delete_hotel()
            elif choice == 'c':
                self.display_hotel_info()
            elif choice == 'd':
                self.modify_hotel_info()
            elif choice == 'e':
                self.reserve_room()
            elif choice == 'f':
                self.cancel_reservation()
            elif choice == 'g':
                break
            else:
                print("Invalid choice. Please try again.")

    def create_hotel(self):
        """create new hotel"""
        self.display_available_hotels()
        name = input("Enter hotel name: ")
        location = input("Enter hotel location: ")

        # Check if the hotel with the same name and
        #location already exists
        hotels = self.get_hotels()
        for hotel in hotels:
            if hotel['name'] == name and hotel['location'] == location:
                print("This hotel is already on the list. \
                If you wish to modify, go to the Manage Hotel menu.")
                return

        rooms = int(input("Enter number of rooms: "))
        new_hotel = {"name": name, "location": location, "rooms": rooms}
        hotels.append(new_hotel)
        self.save_data(hotels, self.hotels_file)
        print("Hotel created successfully.")

    def delete_hotel(self):
        """delete existing hotel from list"""
        hotels = self.get_hotels()
        if not hotels:
            print("No hotels available.")
            return

        print("Select a hotel to delete:")
        self.display_available_hotels()
        choice = input("Enter the number of the hotel to delete: ")

        if not choice.isdigit() or int(choice) \
        not in range(1, len(hotels) + 1):
            print("Invalid choice. Please try again.")
            return

        del hotels[int(choice) - 1]
        print("Hotel deleted successfully.")
        self.save_data(hotels, self.hotels_file)

    def display_hotel_info(self):
        """Show hotels on database"""
        hotels = self.get_hotels()
        if hotels:
            print("Hotel Information:")
            for hotel in hotels:
                print(f"Name: {hotel['name']}, Location: \
                {hotel['location']}, Rooms: {hotel['rooms']}")
        else:
            print("No hotels found.")

    def modify_hotel_info(self):
        """Modify the info from a hotel"""
        hotels = self.get_hotels()
        if not hotels:
            print("No hotels available.")
            return

        print("Select a hotel to modify:")
        self.display_available_hotels()
        choice = input("Enter the number of the hotel to modify: ")

        if not choice.isdigit() or int(choice) not in \
        range(1, len(hotels) + 1):
            print("Invalid choice. Please try again.")
            return

        hotel_to_modify = hotels[int(choice) - 1]
        print("1. Modify name")
        print("2. Modify location")
        print("3. Modify number of rooms")
        option = input("Enter your choice: ")

        if option == '1':
            new_name = input("Enter new name: ")
            hotel_to_modify['name'] = new_name
            print("Hotel name modified successfully.")
        elif option == '2':
            new_location = input("Enter new location: ")
            hotel_to_modify['location'] = new_location
            print("Hotel location modified successfully.")
        elif option == '3':
            new_rooms = int(input("Enter new number of rooms: "))
            hotel_to_modify['rooms'] = new_rooms
            print("Number of rooms modified successfully.")
        else:
            print("Invalid choice. Please try again.")

        self.save_data(hotels, self.hotels_file)

    def reserve_room(self):
        """Book a reservation"""
        hotels = self.get_hotels()
        if not hotels:
            print("No hotels available.")
            return

        self.display_available_hotels()

        while True:
            try:
                hotel_choice = int(input\
                 ("Enter the number of the hotel to book: "))
                if hotel_choice < 1 or hotel_choice > len(hotels):
                    raise ValueError
                break
            except ValueError:
                print("Invalid choice. Please enter a valid number.")

        selected_hotel = hotels[hotel_choice - 1]

        max_rooms = selected_hotel.get('rooms', 0)
        if max_rooms <= 0:
            print("No rooms available in this hotel.")
            return

        print(f"Selected Hotel: {selected_hotel['name']} - \
        {selected_hotel['location']} ({max_rooms} rooms)")

        while True:
            try:
                num_rooms =int(input(f"Enter the number of rooms to book \
                (max {max_rooms} rooms available): "))
                if num_rooms < 1 or num_rooms > max_rooms:
                    raise ValueError
                break
            except ValueError:
                print(f"Invalid number of rooms. \
                Please enter a number between 1 and {max_rooms}.")

        customer_name = input("Enter customer name: ")
        customer_email = input("Enter customer email: ")

        customers = self.get_customers()
        if not any(customer['name'] == customer_name \
                   for customer in customers):
            customers.append({"name": customer_name, \
                              "email": customer_email})
            self.save_data(customers, self.customers_file)
            print("Customer added successfully.")

        reservation = {
            "customer": customer_name,
            "email": customer_email,
            "hotel": selected_hotel['name'],
            "location": selected_hotel['location'],
            "rooms": num_rooms,
            "reservation_date": datetime.now().strftime\
             ('%Y-%m-%d %H:%M:%S')
        }

        selected_hotel['rooms'] -= num_rooms
        self.save_data(hotels, self.hotels_file)

        reservations = self.get_reservations()
        reservations.append(reservation)
        self.save_data(reservations, self.reservations_file)

        print("Reservation created successfully.")

    def cancel_reservation(self):
        """cancel an existing reservation"""
        reservations = self.get_reservations()
        if not reservations:
            print("No reservations available.")
            return

        print("Select a reservation to cancel:")
        self.display_reservation_info()
        while True:
            try:
                reservation_choice = \
                int(input("Enter the number of the \
                reservation to cancel: "))
                if reservation_choice < 1 \
                or reservation_choice > len(reservations):
                    raise ValueError
                break
            except ValueError:
                print("Invalid choice. Please enter a valid number.")

        canceled_reservation = reservations.pop(reservation_choice - 1)
        hotel_name = canceled_reservation['hotel']
        canceled_rooms = canceled_reservation['rooms']

        hotels = self.get_hotels()
        for hotel in hotels:
            if hotel['name'] == hotel_name:
                hotel['rooms'] += canceled_rooms
                break

        self.save_data(reservations, self.reservations_file)
        self.save_data(hotels, self.hotels_file)

        print("Reservation canceled successfully.")

    def display_reservation_info(self):
        """display reservations"""
        reservations = self.get_reservations()
        if reservations:
            print("Reservation Information:")
            for i, reservation in enumerate(reservations, start=1):
                print(f"{i}. Customer: {reservation['customer']}, \
                Hotel: {reservation['hotel']}, \
                Rooms: {reservation['rooms']}")
        else:
            print("No reservations found.")

    def get_customers(self):
        """Check if customer is on the database"""
        try:
            with open(self.customers_file, 'r') as f:
                customers = json.load(f)
                return customers
        except FileNotFoundError:
            return []

    def get_reservations(self):
        """Check reservations"""
        try:
            with open(self.reservations_file, 'r') as f:
                reservations = json.load(f)
                return reservations
        except FileNotFoundError:
            return []

    def save_data(self, data, filename):
        """update information"""
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_data(self, filename):
        """load information"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return []

# customerManager.py
#import json
#from customer import Customer

"""
Customer Manager

This class manages customer information including creating, deleting,
modifying, and displaying customer data.

Attributes:
    customers_file (str): The file path to the JSON file storing 
    customer data.
    customers (list): A list containing Customer objects representing 
    customer data.

Methods:
    __init__: Initializes the CustomerManager with the 
    customers_file path and loads customer data.
    manage_customers: Displays a menu to manage customer data.
    create_customer: Allows the user to create a new customer and
   adds it to the customer list.
    delete_customer: Allows the user to delete a customer from 
    the customer list.
    display_customer_info: Displays information about all 
    customers in the customer list.
    modify_customer_info: Allows the user to modify information 
    of an existing customer.
    save_data: Saves the customer data to the customers_file.
    load_data: Loads customer data from the customers_file.

"""
class CustomerManager:
    def __init__(self, customers_file):
        """
    Initializes the CustomerManager.
    Args:
    customers_file (str): The file path to the JSON file
   storing customer data.
    """
        self.customers_file = customers_file
        self.customers = self.load_data()

    def manage_customers(self):
        """
        Displays a menu to manage customer data.
        """
        while True:
            print("\nManage Customers")
            print("a. Create Customer")
            print("b. Delete Customer")
            print("c. Display Customer Information")
            print("d. Modify Customer Information")
            print("e. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == 'a':
                self.create_customer()
            elif choice == 'b':
                self.delete_customer()
            elif choice == 'c':
                self.display_customer_info()
            elif choice == 'd':
                self.modify_customer_info()
            elif choice == 'e':
                break
            else:
                print("Invalid choice. Please try again.")

    def create_customer(self):
        """
    Allows the user to create a new customer and adds
   it to the customer list.
    """
        name = input("Enter customer name: ")
        email = input("Enter customer email: ")
        new_customer = Customer(name, email)
        self.customers.append(new_customer)
        print("Customer created successfully.")
        self.save_data()

    def delete_customer(self):
        """
    Allows the user to delete a customer from the customer list.
    """
        self.display_customer_info()
        if self.customers:
            name_to_delete = input("Enter customer name to delete: ")
            for customer in self.customers:
                if customer.name.lower() == name_to_delete.lower():
                    self.customers.remove(customer)
                    print("Customer deleted successfully.")
                    break
            else:
                print("Customer not found.")
        else:
            print("No customers available.")
        self.save_data()

    def display_customer_info(self):
        """
    Displays information about all customers in the customer list.
    """
        if self.customers:
            sorted_customers = sorted(self.customers, \
                                      key=lambda x: x.name.lower())
            print("Customer Information:")
            for customer in sorted_customers:
                print(f"Name: {customer.name}, Email: {customer.email}")
        else:
            print("No customers found.")

    def modify_customer_info(self):
        """
        Allows the user to modify information of an existing customer.
        """
        self.display_customer_info()
        if self.customers:
            name_to_modify = input("Enter customer name to modify: ")
            for customer in self.customers:
                if customer.name.lower() == name_to_modify.lower():
                    new_name = input("Enter new name \
                    (leave empty to keep current): ")
                    new_email = input("Enter new email \
                    (leave empty to keep current): ")
                    customer.name = new_name \
                    if new_name \
                    else customer.name
                    customer.email = new_email \
                    if new_email \
                    else customer.email
                    print("Customer information modified successfully.")
                    break
            else:
                print("Customer not found.")
        else:
            print("No customers available.")
        self.save_data()

    def save_data(self):
        """
        Saves the customer data to the customers_file.
        """
        with open(self.customers_file, 'w') as f:
            json.dump([customer.__dict__ \
                       for customer in self.customers], f, indent=4)

    def load_data(self):
        """
        Loads customer data from the customers_file.
        """
        try:
            with open(self.customers_file, 'r') as f:
                data = json.load(f)
                return [Customer(**customer) for customer in data]
        except FileNotFoundError:
            return []

#import json
#import os
#from datetime import datetime
"""
ReservationManager Class

This class manages reservations for hotels. It allows users 
to create, cancel, and display reservations.

Attributes:
    hotels_file (str): The file path to the JSON file containing
   hotel information.
    customers_file (str): The file path to the JSON file containing 
    customer information.
    reservations_file (str): The file path to the JSON file containing 
    reservation information.

Methods:
    __init__(self, hotels_file, customers_file, reservations_file): 
    Initializes the ReservationManager object.
    manage_reservations(self): Manages reservation operations such as 
    creating, canceling, and displaying reservations.
    create_reservation(self): Creates a new reservation.
    cancel_reservation(self): Cancels an existing reservation.
    display_reservation_info(self): Displays information about 
    existing reservations.
    display_available_hotels(self): Displays a list of available 
    hotels.
    load_hotels(self): Loads hotel data from the JSON file.
    save_hotels(self, hotels): Saves hotel data to the JSON file.
    load_customers(self): Loads customer data from the JSON file.
    save_customers(self, customers): Saves customer data to the 
    JSON file.
    load_reservations(self): Loads reservation data from the JSON
   file.
    save_reservations(self, reservations): Saves reservation data 
    to the JSON file.

Usage:
    Initialize a ReservationManager object with file paths to hotel,
   customer, and reservation JSON files.
    Call manage_reservations() to start managing reservations, where 
    users can create, cancel, and display reservations.
"""
#pylint: disable=W0311
# pylint: disable==W1514
# pylint: disable==C0116
#disable=missing-function-docstring,
#        missing-module-docstring,
#        

class ReservationManager:
    def __init__(self, hotels_file, customers_file, reservations_file):
        self.hotels_file = hotels_file
        self.customers_file = customers_file
        self.reservations_file = reservations_file

        # Create reservations file if it doesn't exist
        if not os.path.exists(reservations_file):
            with open(reservations_file, 'w') as f:
                json.dump([], f)

    def manage_reservations(self):
        while True:
            print("\nManage Reservations")
            print("a. Create a Reservation")
            print("b. Cancel a Reservation")
            print("c. Display Reservation Information")
            print("d. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == 'a':
                self.create_reservation()
            elif choice == 'b':
                self.cancel_reservation()
            elif choice == 'c':
                self.display_reservation_info()
            elif choice == 'd':
                break
            else:
                print("Invalid choice. Please try again.")

    def create_reservation(self):
          hotels = self.load_hotels()
          if not hotels:
              print("No hotels available.")
              return

          customers = self.load_customers()
          if not customers:
              print("No customers available. Please add a \
              customer first.")
              return

          self.display_available_hotels()

          while True:
              try:
                  hotel_choice = int(input("Enter the number of \
                  the hotel to book: "))
                  if hotel_choice < 1 or hotel_choice > len(hotels):
                      raise ValueError
                  break
              except ValueError:
                  print("Invalid choice. Please enter a valid number.")

          selected_hotel = hotels[hotel_choice - 1]

          while True:
              try:
                  num_rooms = int(input(f"Enter the number of rooms to \
                  book (max {selected_hotel['rooms']} \
                  rooms available): "))
                  if num_rooms < 1 or num_rooms > selected_hotel['rooms']:
                      raise ValueError
                  break
              except ValueError:
                  print(f"Invalid number of rooms. Please enter a \
                  number between 1 and {selected_hotel['rooms']}.")

          customer_name = input("Enter customer name: ")
          customer_email = input("Enter customer email: ")

          # Check if the customer already exists
          customer_exists = False
          for customer in customers:
              if customer['name'] == customer_name:
                  customer_exists = True
                  break

          # If customer does not exist, add them to the customers list
          if not customer_exists:
              customers.append({"name": customer_name, \
                                "email": customer_email})
              self.save_customers(customers)
              print("Customer added successfully.")

          # Create a reservation
          reservation = {
              "customer": customer_name,
              "hotel": selected_hotel['name'],
              "rooms": num_rooms
          }

          # Update available rooms in the hotel
          selected_hotel['rooms'] -= num_rooms
          self.save_hotels(hotels)

          # Save reservation
          reservations = self.load_reservations()
          reservations.append(reservation)
          self.save_reservations(reservations)

          print("Reservation created successfully.")


    def cancel_reservation(self):
        reservations = self.load_reservations()
        if not reservations:
            print("No reservations available.")
            return

        print("Select a reservation to cancel:")
        self.display_reservation_info()
        while True:
            try:
                reservation_choice = int(input\
                 ("Enter the number of the reservation to cancel: "))
                if reservation_choice < 1 or reservation_choice > \
                len(reservations):
                    raise ValueError
                break
            except ValueError:
                print("Invalid choice. Please enter a valid number.")

        canceled_reservation = reservations.pop(reservation_choice - 1)
        hotel_name = canceled_reservation['hotel']
        canceled_rooms = canceled_reservation['rooms']

        hotels = self.load_hotels()
        for hotel in hotels:
            if hotel['name'] == hotel_name:
                hotel['rooms'] += canceled_rooms
                break

        self.save_reservations(reservations)
        self.save_hotels(hotels)

        print("Reservation canceled successfully.")

    def display_reservation_info(self):
        reservations = self.load_reservations()
        if reservations:
            print("Reservation Information:")
            for i, reservation in enumerate(reservations, start=1):
                print(f"{i}. Customer: {reservation['customer']}, \
                Hotel: {reservation['hotel']}, \
                Rooms: {reservation['rooms']}")
        else:
            print("No reservations found.")

    def display_available_hotels(self):
        hotels = self.load_hotels()
        print("Available Hotels:")
        for i, hotel in enumerate(hotels, start=1):
            print(f"{i}. {hotel['name']} - {hotel['location']} \
            ({hotel['rooms']} rooms available)")

    def load_hotels(self):
        try:
            with open(self.hotels_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_hotels(self, hotels):
        with open(self.hotels_file, 'w') as f:
            json.dump(hotels, f, indent=4)

    def load_customers(self):
        try:
            with open(self.customers_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_customers(self, customers):
        with open(self.customers_file, 'w') as f:
            json.dump(customers, f, indent=4)

    def load_reservations(self):
        try:
            with open(self.reservations_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_reservations(self, reservations):
        with open(self.reservations_file, 'w') as f:
            json.dump(reservations, f, indent=4)

#import json
#from datetime import datetime
#from hotel_manager import HotelManager
#from customer_manager import CustomerManager

def main():
    hotels_file = 'hotels.json'
    customers_file = 'customers.json'
    reservations_file = 'reservations.json'
    choice = None
    while choice != '4':
        print("\nHotel Management System")
        print("1. Manage Hotels")
        print("2. Manage Customers")
        print("3. Manage Reservations")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            hotel_manager = HotelManager\
             (hotels_file, customers_file, reservations_file)
            hotel_manager.manage_hotels()
        elif choice == '2':
            customer_manager = CustomerManager(customers_file)
            customer_manager.manage_customers()
        elif choice == '3':
            reservation_manager = ReservationManager\
             (hotels_file, customers_file, reservations_file)
            reservation_manager.manage_reservations()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()


