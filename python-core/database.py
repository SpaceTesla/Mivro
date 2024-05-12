import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

credential = credentials.Certificate('firebase-key.json')
firebase_admin.initialize_app(credential)
db = firestore.client()

def database_history(product_barcode, product_data):
    try:
        api_history_ref = db.collection('api_history')
        barcode_doc = api_history_ref.document(product_barcode)

        if barcode_doc.get().exists:
            print(f'[Database] API history for "{product_barcode}" exists.')
            return

        barcode_doc.set(product_data)
        print(f'[Database] API history for "{product_barcode}" stored.')
    except Exception as exc:
        print(f'Firestore storage error:\n {exc}')

def search_database(search_keyword, search_keys):
    try:
        api_history_ref = db.collection('api_history')

        search_queries = [
            api_history_ref.where(filter=FieldFilter(key, '>=', search_keyword))
            .where(filter=FieldFilter(key, '<=', search_keyword + '\uf8ff'))
            for key in search_keys
        ]

        found_documents = [
            doc.to_dict()
            for query in search_queries
            for doc in query.stream()
        ]

        print(f'[Database] Found {len(found_documents)} document(s) for "{search_keyword}".')
        return found_documents
    except Exception as exc:
        print(f'Database search error:\n {exc}')
