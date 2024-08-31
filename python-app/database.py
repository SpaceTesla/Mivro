# Core library imports: Firebase Admin SDK setup
import firebase_admin
from firebase_admin import credentials, firestore
from werkzeug.security import generate_password_hash, check_password_hash
from fuzzywuzzy import fuzz
from datetime import datetime

# Local project-specific imports: Models for Firestore documents
from models import AccountInfo, ScanHistory, SearchHistory

# Initialize the Firebase Admin SDK with the service account key
credential = credentials.Certificate('firebase-adminsdk.json')
firebase_admin.initialize_app(credential)
database = firestore.client() # Initialize the Firestore database client

# Create Firestore document references for the collections
user_reference = database.collection('users')
not_found_reference = database.collection('not_found')
error_reference = database.collection('errors')
flagged_reference = database.collection('flagged')

def database_history(email: str, product_barcode: str, product_data: dict) -> None:
    try:
        # Check if the user document and scan history for the product barcode exist in Firestore
        user_document = user_reference.document(email)
        if user_document.get().exists:
            user_data = user_document.get().to_dict()
            if 'scan_history' in user_data and product_barcode in user_data['scan_history']:
                print(f'[Database] Scan history for "{product_barcode}" exists.')
                return

        # Store the scan history for the product barcode in Firestore if it does not exist
        scan_history = ScanHistory(product_barcode=product_barcode, product_data=product_data)
        user_document.set({
            'scan_history': scan_history.to_dict()
        }, merge=True) # Merge the scan history with the existing user document (if any)

        print(f'[Database] Scan history for "{product_barcode}" stored.')
    except Exception as exc:
        runtime_error('database_history', str(exc), email=email, product_barcode=product_barcode)
        return {'error': 'Firestore storage error: ' + str(exc)}, 500

def database_search(email: str, product_keyword: str, search_keys: list) -> dict:
    try:
        # Retrieve the scan history of all user documents in Firestore
        user_stream = user_reference.stream()
        scan_results = []

        # Compare the product keyword with the search keys in the scan history for each user
        for user_document in user_stream:
            user_data = user_document.to_dict()
            scan_history = user_data.get('scan_history', {})

            # Compare the product keyword with the search keys in the scan history
            for scan_data in scan_history:
                for key in search_keys:
                    # Calculate the similarity score between the product keyword and the scan data by token set ratio method
                    field_value = str(scan_history[scan_data].get(key, '')).lower()
                    similarity_score = fuzz.token_set_ratio(product_keyword.lower(), field_value)
                    # Add the scan data to the results if the similarity score is above 70% (arbitrary threshold)
                    if similarity_score > 70:
                        scan_results.append({
                            'data': scan_history[scan_data],
                            'similarity': similarity_score
                        })

        # Sort the results by similarity (higher similarity = higher relevance)
        scan_results.sort(key=lambda x: x['similarity'], reverse=True)
        search_history = SearchHistory(user_searches=product_keyword) # Store the search history for the product keyword in Firestore
        user_reference.document(email).set({
            'search_history': firestore.ArrayUnion([search_history.to_dict()])
        }, merge=True) # Merge the search history with the existing user document (if any)

        print(f'[Database] Found {len(scan_results)} result(s) for "{product_keyword}".')
        return scan_results[0]['data'] if scan_results else None # Return the most relevant result (if any)
    except Exception as exc:
        runtime_error('database_search', str(exc), email=email, product_keyword=product_keyword)
        return {'error': 'Database search error: ' + str(exc)}, 500

def product_not_found(search_type: str, search_value: str) -> None:
    try:
        # Select the document name based on the search type
        document_name = 'barcodes' if search_type == 'barcode' else 'keywords'
        not_found_document = not_found_reference.document(document_name)

        # Add the search value to the not found list in Firestore
        not_found_document.set({
            'search_values': firestore.ArrayUnion([search_value])
        }, merge=True) # Merge the search value with the existing not found document (if any)

        print(f'[Database] "{search_value}" added to the "{document_name}" not found list.')
    except Exception as exc:
        runtime_error('product_not_found', str(exc), search_type=search_type, search_value=search_value)
        return {'error': 'Firestore storage error: ' + str(exc)}, 500

def runtime_error(function_name: str, error_message: str, **kwargs) -> None:
    try:
        # Select the document name based on the function name
        error_document = error_reference.document(function_name)
        # Store the error message and timestamp in Firestore for the function
        error_data = {
            'error_message': error_message,
            'timestamp': datetime.now().strftime('%d-%B-%Y %H:%M:%S')
        }
        # Check if additional keyword arguments are provided and add them to the error data
        if kwargs:
            error_data.update(kwargs)

        # Add the error data to the error reports in Firestore for the function
        error_document.set({
            'error_reports': firestore.ArrayUnion([error_data])
        }, merge=True) # Merge the error data with the existing error document (if any)

        print(f'[Database] Error logged for "{function_name}": {error_message}')
    except Exception as exc:
        runtime_error('runtime_error', str(exc), function_name=function_name, error_message=error_message, **kwargs)
        return {'error': 'Firestore storage error: ' + str(exc)}, 500

def register_user_profile(email: str, password: str) -> None:
    try:
        # Check if the user document already exists in Firestore
        user_document = user_reference.document(email)
        if user_document.get().exists:
            return {'error': 'User already exists.'}, 400

        # Create a new user document in Firestore with the account information
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        created_date = datetime.now().strftime('%d-%B-%Y')
        created_time = datetime.now().strftime('%I:%M %p')

        # Store the account information for the new user in Firestore
        account_info = AccountInfo(email=email, password=hashed_password, created_date=created_date, created_time=created_time)
        user_document.set({
            'account_info': account_info.to_dict()
        })

        # return {'message': 'Account created successfully.'}
    except Exception as exc:
        runtime_error('register_user_profile', str(exc), email=email)
        return {'error': 'Firestore registration error: ' + str(exc)}, 500

# This function does not have status codes because middleware.py handles the status codes
def validate_user_profile(email: str, password: str) -> dict:
    try:
        # Check if the user document exists in Firestore
        user_document = user_reference.document(email)
        if not user_document.get().exists:
            return {'error': 'User does not exist.'}

        # Check if the password matches the hashed password stored in Firestore
        user_data = user_document.get().to_dict()
        if not check_password_hash(user_data['account_info']['password'], password):
            return {'error': 'Incorrect password.'}

        return {'message': 'Login successful.'}
    except Exception as exc:
        runtime_error('validate_user_profile', str(exc), email=email)
        return {'error': 'Firestore validation error: ' + str(exc)}

def remove_user_profile(email: str) -> dict:
    try:
        # Check if the user document exists in Firestore
        user_document = user_reference.document(email)
        if user_document.get().exists:
            user_document.delete() # Delete the user document from Firestore
            return {'message': 'Account deleted successfully.'}
        else:
            return {'error': 'User document does not exist.'}, 404
    except Exception as exc:
        runtime_error('remove_user_profile', str(exc), email=email)
        return {'error': 'Firestore deletion error: ' + str(exc)}, 500

def save_health_profile(email: str, health_data: dict) -> dict:
    try:
        # Store the health profile data for the user in Firestore
        user_document = user_reference.document(email)
        user_document.set({
            'health_profile': health_data
        }, merge=True)  # Merge the health profile with the existing user document (if any)

        return {'message': 'Health profile saved successfully.'}
    except Exception as exc:
        runtime_error('save_health_profile', str(exc), email=email)
        return {'error': 'Firestore storage error: ' + str(exc)}, 500
