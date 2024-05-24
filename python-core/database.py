import firebase_admin
from firebase_admin import credentials, firestore
from werkzeug.security import generate_password_hash, check_password_hash

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

        user_document.set({
            'scan_history': {
                product_barcode: product_data
            }
        }, merge=True)

        print(f'[Database] Scan history for "{product_barcode}" stored.')
    except Exception as exc:
        print(f'Firestore storage error:\n {exc}')

def database_search(product_keyword, search_keys):
    try:
        user_stream = user_reference.stream()
        scan_results = []

        for user_document in user_stream:
            user_data = user_document.to_dict()
            scan_history = user_data['scan_history']

            user_scans = [
                scan_data
                for scan_data in scan_history.values()
                if any(product_keyword.lower() in str(value).lower() for value in scan_data.values())
            ]

            scan_results.extend(user_scans)

        product_document = scan_results[0] if scan_results else None
        print(f'[Database] Found {len(scan_results)} document(s) for "{product_keyword}".')
        return product_document
    except Exception as exc:
        print(f'Database search error:\n {exc}')

def register_user(email, password):
    try:
        user_document = user_reference.document(email)
        if user_document.get().exists:
            return {'error': 'User already exists.'}

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        user_document.set({
            'account_info': {
                'email': email,
                'password': hashed_password
            }
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
