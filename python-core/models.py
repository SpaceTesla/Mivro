from config import DEFAULT_NAME, DEFAULT_PHOTO

class AccountInfo:
    def __init__(self, display_name=DEFAULT_NAME, photo_url=DEFAULT_PHOTO, email=None,
                 password=None, phone_number=None, email_verified=False,
                 created_date=None, created_time=None):
        self.display_name = display_name
        self.photo_url = photo_url
        self.email = email
        self.password = password
        self.phone_number = phone_number
        self.email_verified = email_verified
        self.created_date = created_date
        self.created_time = created_time

    def to_dict(self):
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

class HealthProfile:
    def __init__(self, age=None, gender=None, height=None, weight=None, body_mass_index=None,
                 dietary_preferences=None, medical_conditions=None, allergies=None):
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.body_mass_index = body_mass_index
        self.dietary_preferences = dietary_preferences
        self.medical_conditions = medical_conditions
        self.allergies = allergies

    def to_dict(self):
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

class ScanHistory:
    def __init__(self, product_barcode=None, product_data=None):
        self.product_barcode = product_barcode
        self.product_data = product_data

    def to_dict(self):
        return {
            self.product_barcode: self.product_data
        }

class ChatHistory:
    def __init__(self, user_message=None, bot_response=None):
        self.user_message = user_message
        self.bot_response = bot_response

    def to_dict(self):
        return {
            'user_message': self.user_message,
            'bot_response': self.bot_response
        }

class SearchHistory:
    def __init__(self, user_searches=None):
        self.user_searches = user_searches

    def to_dict(self):
        return {
            'user_searches': self.user_searches
        }

class PaymentHistory:
    def __init__(self, payment_gateway=None, product_barcode=None, product_data=None):
        self.payment_gateway = payment_gateway
        self.product_barcode = product_barcode
        self.product_data = product_data

    def to_dict(self):
        return {
            'payment_gateway': self.payment_gateway,
            self.product_barcode: self.product_data
        }
