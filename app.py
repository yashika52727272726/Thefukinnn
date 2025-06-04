from flask import Flask, jsonify, request
import time
import random

app = Flask(__name__)

API_KEY = "piroyashika"  # Required API key

# 100 Unique Decline Responses
DECLINE_RESPONSES = [
    {"code": "DEC-001", "message": "Insufficient funds"},
    {"code": "DEC-002", "message": "Card declined by issuer"},
    {"code": "DEC-003", "message": "Invalid CVV"},
    {"code": "DEC-004", "message": "Expired card"},
    {"code": "DEC-005", "message": "Transaction not permitted"},
    {"code": "DEC-006", "message": "Exceeds withdrawal limit"},
    {"code": "DEC-007", "message": "Restricted card"},
    {"code": "DEC-008", "message": "Suspected fraud"},
    {"code": "DEC-009", "message": "3D Secure failed"},
    {"code": "DEC-010", "message": "Invalid card number"},
    {"code": "DEC-011", "message": "Bank declined (Do Not Honor)"},
    {"code": "DEC-012", "message": "Lost/Stolen card"},
    {"code": "DEC-013", "message": "Pickup card"},
    {"code": "DEC-014", "message": "Invalid expiration date"},
    {"code": "DEC-015", "message": "Invalid transaction"},
    {"code": "DEC-016", "message": "Issuer unavailable"},
    {"code": "DEC-017", "message": "System malfunction"},
    {"code": "DEC-018", "message": "Duplicate transaction"},
    {"code": "DEC-019", "message": "Card not supported"},
    {"code": "DEC-020", "message": "Merchant blacklisted"},
    {"code": "DEC-021", "message": "Country restriction"},
    {"code": "DEC-022", "message": "Currency not supported"},
    {"code": "DEC-023", "message": "Invalid PIN"},
    {"code": "DEC-024", "message": "Card blocked"},
    {"code": "DEC-025", "message": "Account frozen"},
    {"code": "DEC-026", "message": "Bank processing error"},
    {"code": "DEC-027", "message": "Payment gateway timeout"},
    {"code": "DEC-028", "message": "AVS mismatch"},
    {"code": "DEC-029", "message": "Invalid billing details"},
    {"code": "DEC-030", "message": "Card bin not allowed"},
    {"code": "DEC-031", "message": "High-risk transaction"},
    {"code": "DEC-032", "message": "Excessive declines"},
    {"code": "DEC-033", "message": "Issuer not responding"},
    {"code": "DEC-034", "message": "Card type not accepted"},
    {"code": "DEC-035", "message": "Payment processor error"},
    {"code": "DEC-036", "message": "Invalid merchant ID"},
    {"code": "DEC-037", "message": "Inactive card"},
    {"code": "DEC-038", "message": "Chargeback flagged"},
    {"code": "DEC-039", "message": "Exceeds frequency limit"},
    {"code": "DEC-040", "message": "Invalid amount"},
    {"code": "DEC-041", "message": "Issuer declined (no reason)"},
    {"code": "DEC-042", "message": "Network error"},
    {"code": "DEC-043", "message": "Invalid MCC"},
    {"code": "DEC-044", "message": "Cardholder verification failed"},
    {"code": "DEC-045", "message": "Temporary hold"},
    {"code": "DEC-046", "message": "Refer to issuer"},
    {"code": "DEC-047", "message": "Payment method expired"},
    {"code": "DEC-048", "message": "Transaction canceled"},
    {"code": "DEC-049", "message": "Invalid token"},
    {"code": "DEC-050", "message": "Declined (generic)"},
    # Additional 50 decline responses (51-100)
    {"code": "DEC-051", "message": "Invalid account type"},
    {"code": "DEC-052", "message": "Bank declined (fraud)"},
    {"code": "DEC-053", "message": "Incorrect ZIP code"},
    {"code": "DEC-054", "message": "Invalid session"},
    {"code": "DEC-055", "message": "Card not activated"},
    {"code": "DEC-056", "message": "Bank declined (policy)"},
    {"code": "DEC-057", "message": "Invalid API key"},
    {"code": "DEC-058", "message": "Processor declined"},
    {"code": "DEC-059", "message": "Invalid IP address"},
    {"code": "DEC-060", "message": "Velocity limit exceeded"},
    {"code": "DEC-061", "message": "Invalid name on card"},
    {"code": "DEC-062", "message": "Bank declined (retry later)"},
    {"code": "DEC-063", "message": "Card not present"},
    {"code": "DEC-064", "message": "Invalid terminal ID"},
    {"code": "DEC-065", "message": "Invalid PIN block"},
    {"code": "DEC-066", "message": "Invalid track data"},
    {"code": "DEC-067", "message": "Invalid EMV data"},
    {"code": "DEC-068", "message": "Invalid cryptogram"},
    {"code": "DEC-069", "message": "Invalid AID"},
    {"code": "DEC-070", "message": "Invalid TVR"},
    {"code": "DEC-071", "message": "Invalid TSI"},
    {"code": "DEC-072", "message": "Invalid application label"},
    {"code": "DEC-073", "message": "Invalid CVM"},
    {"code": "DEC-074", "message": "Invalid ARQC"},
    {"code": "DEC-075", "message": "Invalid ARPC"},
    {"code": "DEC-076", "message": "Invalid IAD"},
    {"code": "DEC-077", "message": "Invalid AIP"},
    {"code": "DEC-078", "message": "Invalid ATC"},
    {"code": "DEC-079", "message": "Invalid UN"},
    {"code": "DEC-080", "message": "Invalid CID"},
    {"code": "DEC-081", "message": "Invalid KVV"},
    {"code": "DEC-082", "message": "Invalid service code"},
    {"code": "DEC-083", "message": "Invalid PAN sequence"},
    {"code": "DEC-084", "message": "Invalid PSNS"},
    {"code": "DEC-085", "message": "Invalid CSN"},
    {"code": "DEC-086", "message": "Invalid PAN"},
    {"code": "DEC-087", "message": "Invalid expiry date"},
    {"code": "DEC-088", "message": "Invalid cardholder name"},
    {"code": "DEC-089", "message": "Invalid currency"},
    {"code": "DEC-090", "message": "Invalid amount"},
    {"code": "DEC-091", "message": "Invalid country"},
    {"code": "DEC-092", "message": "Invalid MCC"},
    {"code": "DEC-093", "message": "Invalid merchant"},
    {"code": "DEC-094", "message": "Invalid terminal"},
    {"code": "DEC-095", "message": "Invalid acquirer"},
    {"code": "DEC-096", "message": "Invalid issuer"},
    {"code": "DEC-097", "message": "Invalid network"},
    {"code": "DEC-098", "message": "Invalid response code"},
    {"code": "DEC-099", "message": "Invalid auth code"},
    {"code": "DEC-100", "message": "Invalid reversal"},
]

@app.route('/process', methods=['POST'])
def process_payment():
    """Process payment with 25-second delay & random decline response"""
    if request.headers.get('API-Key') != API_KEY:
        return jsonify({"status": "error", "message": "Invalid API key"}), 401

    data = request.get_json()
    if not data or 'card_data' not in data:
        return jsonify({"status": "error", "message": "Missing card_data"}), 400

    card_data = data['card_data']
    if not isinstance(card_data, str) or card_data.count('|') != 3:
        return jsonify({"status": "error", "message": "Invalid format. Use CC|MM|YY|CVV"}), 400

    # Simulate 25-second processing delay
    time.sleep(25)

    # Select a random decline response
    decline = random.choice(DECLINE_RESPONSES)

    # Format response
    response = {
        "card_data": card_data,
        "response": decline,
        "status": "declined"
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
