import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from werkzeug.security import generate_password_hash, check_password_hash

credential = credentials.Certificate('firebase-key.json')
firebase_admin.initialize_app(credential)
db = firestore.client()

user_ref = db.collection('users')
scan_history_ref = db.collection('scan_history')

def database_history(product_barcode, product_data):
    try:
        barcode_doc = scan_history_ref.document(product_barcode)
        if barcode_doc.get().exists:
            print(f'[Database] Product history for "{product_barcode}" exists.')
            return

        barcode_doc.set(product_data)
        print(f'[Database] Product history for "{product_barcode}" stored.')
    except Exception as exc:
        print(f'Firestore storage error:\n {exc}')

def database_search(product_keyword, search_keys):
    try:
        search_queries = [
            scan_history_ref.where(filter=FieldFilter(key, '>=', product_keyword))
            .where(filter=FieldFilter(key, '<=', product_keyword + '\uf8ff'))
            for key in search_keys
        ]

        found_documents = [
            doc.to_dict()
            for query in search_queries
            for doc in query.stream()
        ]

        print(f'[Database] Found {len(found_documents)} document(s) for "{product_keyword}".')
        return found_documents
    except Exception as exc:
        print(f'Database search error:\n {exc}')

def register_user(email, password):
    try:
        user_doc = user_ref.document(email)
        if user_doc.get().exists:
            return {'error': 'User already exists.'}

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        user_doc.set(
            {
                'email': email,
                'password': hashed_password
            }
        )
        return {'message': 'User registered successfully.'}
    except Exception as exc:
        return {'error': str(exc)}

def validate_user(email, password):
    try:
        user_doc = user_ref.document(email)
        if not user_doc.get().exists:
            return {'error': 'User does not exist.'}

        user_data = user_doc.get().to_dict()
        if not check_password_hash(user_data['password'], password):
            return {'error': 'Incorrect password.'}

        return {'message': 'Login successful.'}
    except Exception as exc:
        return {'error': str(exc)}
