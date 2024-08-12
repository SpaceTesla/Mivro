from datetime import datetime
from config import DEFAULT_NAME, DEFAULT_PHOTO

# Model for user account information
class AccountInfo:
    def __init__(self, display_name: str = DEFAULT_NAME, photo_url: str = DEFAULT_PHOTO, email: str = None,
                 password: str = None, phone_number: str = None, email_verified: bool = False,
                 created_date: str = None, created_time: str = None):
        self.display_name = display_name
        self.photo_url = photo_url
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.email_verified = email_verified
        self.created_date = created_date
        self.created_time = created_time

    def to_dict(self) -> dict:
        return {
            'display_name': self.display_name,
            'photo_url': self.photo_url,
            'email': self.email,
            'password': self.password,
            'phone_number': self.phone_number,
            'email_verified': self.email_verified,
            'created_date': self.created_date,
            'created_time': self.created_time
        }

# Model for user health profile
class HealthProfile:
    def __init__(self, age: int = None, gender: str = None, height: float = None, weight: float = None, body_mass_index: float = None,
                 allergies: list = None, dietary_preferences: list = None, medical_conditions: list = None):
        from utils import calculate_bmi # Importing here to avoid circular import error

        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.body_mass_index = body_mass_index or calculate_bmi(weight, height)
        self.allergies = allergies
        self.dietary_preferences = dietary_preferences
        self.medical_conditions = medical_conditions

    def to_dict(self) -> dict:
        return {
            'age': self.age,
            'gender': self.gender,
            'height': self.height,
            'weight': self.weight,
            'body_mass_index': self.body_mass_index,
            'dietary_preferences': self.dietary_preferences,
            'medical_conditions': self.medical_conditions,
            'allergies': self.allergies
        }

# Model for user scan history
class ScanHistory:
    def __init__(self, product_barcode: str = None, product_data: dict = None):
        self.product_barcode = product_barcode
        self.product_data = product_data

    def to_dict(self) -> dict:
        return {
            self.product_barcode: self.product_data
        }

# Model for user chat history
class ChatHistory:
    def __init__(self, user_message: str = None, bot_response: str = None, timestamp: str = None):
        self.user_message = user_message
        self.bot_response = bot_response
        self.timestamp = timestamp or datetime.now().strftime('%d-%B-%Y %I:%M %p')

    def to_dict(self) -> dict:
        return {
            'user_message': self.user_message,
            'bot_response': self.bot_response,
            'timestamp': self.timestamp
        }

# Model for user search history
class SearchHistory:
    def __init__(self, user_searches: list = None):
        self.user_searches = user_searches

    def to_dict(self) -> dict:
        return {
            'user_searches': self.user_searches
        }

# Model for user payment history
class PaymentHistory:
    def __init__(self, payment_gateway: str = None, product_barcode: str = None, product_data: dict = None, timestamp: str = None):
        self.payment_gateway = payment_gateway
        self.product_barcode = product_barcode
        self.product_data = product_data
        self.timestamp = timestamp or datetime.now().strftime('%d-%B-%Y %I:%M %p')

    def to_dict(self) -> dict:
        return {
            'payment_gateway': self.payment_gateway,
            'timestamp': self.timestamp,
            self.product_barcode: self.product_data
        }

# Model for user favorites
class Favorite:
    def __init__(self, product_name: str = None, product_barcode: str = None):
        self.product_name = product_name
        self.product_barcode = product_barcode

    def to_dict(self) -> dict:
        return {
            'product_name': self.product_name,
            'product_barcode': self.product_barcode
        }
