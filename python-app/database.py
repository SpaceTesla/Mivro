import firebase_admin
from firebase_admin import credentials, firestore
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from models import AccountInfo, ScanHistory, SearchHistory

credential = credentials.Certificate('firebase-key.json')
firebase_admin.initialize_app(credential)
database = firestore.client()

user_reference = database.collection('users')

def database_history(email, product_barcode, product_data):
    try:
        user_document = user_reference.document(email)
        if user_document.get().exists:
            user_data = user_document.get().to_dict()
            if 'scan_history' in user_data and product_barcode in user_data['scan_history']:
                print(f'[Database] Scan history for "{product_barcode}" exists.')
                return

        scan_history = ScanHistory(product_barcode=product_barcode, product_data=product_data)
        user_document.set({
            'scan_history': scan_history.to_dict()
        }, merge=True)

        print(f'[Database] Scan history for "{product_barcode}" stored.')
    except Exception as exc:
        print(f'Firestore storage error:\n {exc}')

def database_search(email, product_keyword, search_keys):
    try:
        user_stream = user_reference.stream()
        scan_results = []
        # found_keys = []

        for user_document in user_stream:
            user_data = user_document.to_dict()
            scan_history = user_data.get('scan_history', {})

            for scan_data in scan_history:
                if any(product_keyword.lower() in str(scan_history[scan_data].get(key, '')).lower() for key in search_keys):
                    scan_results.append(scan_history[scan_data])
                    # found_keys.append(key)

        search_history = SearchHistory(user_searches=product_keyword)
        user_reference.document(email).set({
            'search_history': search_history.to_dict()
        }, merge=True)

        print(f'[Database] Found {len(scan_results)} document(s) for "{product_keyword}".')
        return scan_results[0] if scan_results else None
    except Exception as exc:
        print(f'Database search error:\n {exc}')

def register_user(email, password):
    try:
        user_document = user_reference.document(email)
        if user_document.get().exists:
            return {'error': 'User already exists.'}

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        created_date = datetime.now().strftime('%d-%B-%Y')
        created_time = datetime.now().strftime('%I:%M %p')

        account_info = AccountInfo(email=email, password=hashed_password, created_date=created_date, created_time=created_time)
        user_document.set({
            'account_info': account_info.to_dict()
        })
    except Exception as exc:
        return {'error': str(exc)}

def validate_user(email, password):
    try:
        user_document = user_reference.document(email)
        if not user_document.get().exists:
            return {'error': 'User does not exist.'}

        user_data = user_document.get().to_dict()
        if not check_password_hash(user_data['account_info']['password'], password):
            return {'error': 'Incorrect password.'}

        return {'message': 'Login successful.'}
    except Exception as exc:
        return {'error': str(exc)}

def remove_user(email):
    try:
        user_document = user_reference.document(email)
        if user_document.get().exists:
            user_document.delete()
        else:
            return {'error': 'User document does not exist.'}
    except Exception as exc:
        return {'error': str(exc)}
