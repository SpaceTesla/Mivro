import firebase_admin
from firebase_admin import credentials, firestore

credential = credentials.Certificate('firebase-key.json')
firebase_admin.initialize_app(credential)
db = firestore.client()

def api_history(barcode, product_data):
    api_history_ref = db.collection('api_history')
    barcode_doc = api_history_ref.document(barcode)

    if barcode_doc.get().exists:
        print(f'[Database] API history for "{barcode}" already exists.')
        return

    barcode_doc.set(product_data)
    print(f'[Database] API history for "{barcode}" stored successfully.')
