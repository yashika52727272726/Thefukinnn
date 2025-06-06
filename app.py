from flask import Flask, jsonify, request
import time
import random

app = Flask(__name__)

API_KEY = "yashika"  # Required API key

# 200 Unique Decline Responses (original 100 + new 100)
DECLINE_RESPONSES = [
    # Original 100 responses (1-100)
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

    # Additional 100 decline responses (101-200)
    {"code": "DEC-101", "message": "Card activation required"},
    {"code": "DEC-102", "message": "Maximum PIN attempts exceeded"},
    {"code": "DEC-103", "message": "Issuer inoperative"},
    {"code": "DEC-104", "message": "Invalid transaction type"},
    {"code": "DEC-105", "message": "Exceeds issuer withdrawal limit"},
    {"code": "DEC-106", "message": "Invalid card verification value"},
    {"code": "DEC-107", "message": "No account found"},
    {"code": "DEC-108", "message": "No credit account"},
    {"code": "DEC-109", "message": "No debit account"},
    {"code": "DEC-110", "message": "Account closed"},
    {"code": "DEC-111", "message": "Account not found"},
    {"code": "DEC-112", "message": "Transaction not allowed for cardholder"},
    {"code": "DEC-113", "message": "Transaction not allowed for terminal"},
    {"code": "DEC-114", "message": "Exceeds issuer limit"},
    {"code": "DEC-115", "message": "Invalid security code"},
    {"code": "DEC-116", "message": "Restricted card - lost"},
    {"code": "DEC-117", "message": "Restricted card - stolen"},
    {"code": "DEC-118", "message": "Restricted card - fraud"},
    {"code": "DEC-119", "message": "Restricted card - counterfeit"},
    {"code": "DEC-120", "message": "Call issuer for further information"},
    {"code": "DEC-121", "message": "Card acceptor contact acquirer"},
    {"code": "DEC-122", "message": "Card expired"},
    {"code": "DEC-123", "message": "Possible fraud - withhold card"},
    {"code": "DEC-124", "message": "PIN required"},
    {"code": "DEC-125", "message": "PIN change required"},
    {"code": "DEC-126", "message": "Refer to card issuer"},
    {"code": "DEC-127", "message": "Refer to card issuer's special conditions"},
    {"code": "DEC-128", "message": "Invalid merchant category"},
    {"code": "DEC-129", "message": "Invalid transaction date"},
    {"code": "DEC-130", "message": "Invalid transaction time"},
    {"code": "DEC-131", "message": "Invalid transaction sequence"},
    {"code": "DEC-132", "message": "Invalid transaction reference"},
    {"code": "DEC-133", "message": "Invalid transaction amount"},
    {"code": "DEC-134", "message": "Invalid transaction currency"},
    {"code": "DEC-135", "message": "Invalid transaction destination"},
    {"code": "DEC-136", "message": "Invalid transaction source"},
    {"code": "DEC-137", "message": "Invalid transaction type"},
    {"code": "DEC-138", "message": "Invalid transaction method"},
    {"code": "DEC-139", "message": "Invalid transaction channel"},
    {"code": "DEC-140", "message": "Invalid transaction device"},
    {"code": "DEC-141", "message": "Invalid transaction location"},
    {"code": "DEC-142", "message": "Invalid transaction country"},
    {"code": "DEC-143", "message": "Invalid transaction IP"},
    {"code": "DEC-144", "message": "Invalid transaction MAC"},
    {"code": "DEC-145", "message": "Invalid transaction fingerprint"},
    {"code": "DEC-146", "message": "Invalid transaction browser"},
    {"code": "DEC-147", "message": "Invalid transaction OS"},
    {"code": "DEC-148", "message": "Invalid transaction device ID"},
    {"code": "DEC-149", "message": "Invalid transaction session"},
    {"code": "DEC-150", "message": "Invalid transaction token"},

    # Additional 50 decline responses (151-200)
    {"code": "DEC-151", "message": "Card temporarily restricted"},
    {"code": "DEC-152", "message": "Card permanently restricted"},
    {"code": "DEC-153", "message": "Card security violation"},
    {"code": "DEC-154", "message": "Card usage limit exceeded"},
    {"code": "DEC-155", "message": "Card not yet effective"},
    {"code": "DEC-156", "message": "Card expired prematurely"},
    {"code": "DEC-157", "message": "Card authentication failed"},
    {"code": "DEC-158", "message": "Card verification failed"},
    {"code": "DEC-159", "message": "Card validation failed"},
    {"code": "DEC-160", "message": "Card authorization failed"},
    {"code": "DEC-161", "message": "Card capture failed"},
    {"code": "DEC-162", "message": "Card settlement failed"},
    {"code": "DEC-163", "message": "Card chargeback failed"},
    {"code": "DEC-164", "message": "Card refund failed"},
    {"code": "DEC-165", "message": "Card reversal failed"},
    {"code": "DEC-166", "message": "Card void failed"},
    {"code": "DEC-167", "message": "Card adjustment failed"},
    {"code": "DEC-168", "message": "Card reconciliation failed"},
    {"code": "DEC-169", "message": "Card reporting failed"},
    {"code": "DEC-170", "message": "Card monitoring failed"},
    {"code": "DEC-171", "message": "Card fraud detection failed"},
    {"code": "DEC-172", "message": "Card risk assessment failed"},
    {"code": "DEC-173", "message": "Card compliance failed"},
    {"code": "DEC-174", "message": "Card regulation failed"},
    {"code": "DEC-175", "message": "Card policy failed"},
    {"code": "DEC-176", "message": "Card procedure failed"},
    {"code": "DEC-177", "message": "Card guideline failed"},
    {"code": "DEC-178", "message": "Card standard failed"},
    {"code": "DEC-179", "message": "Card protocol failed"},
    {"code": "DEC-180", "message": "Card specification failed"},
    {"code": "DEC-181", "message": "Card requirement failed"},
    {"code": "DEC-182", "message": "Card condition failed"},
    {"code": "DEC-183", "message": "Card constraint failed"},
    {"code": "DEC-184", "message": "Card limitation failed"},
    {"code": "DEC-185", "message": "Card restriction failed"},
    {"code": "DEC-186", "message": "Card prohibition failed"},
    {"code": "DEC-187", "message": "Card exclusion failed"},
    {"code": "DEC-188", "message": "Card rejection failed"},
    {"code": "DEC-189", "message": "Card denial failed"},
    {"code": "DEC-190", "message": "Card refusal failed"},
    {"code": "DEC-191", "message": "Card cancellation failed"},
    {"code": "DEC-192", "message": "Card termination failed"},
    {"code": "DEC-193", "message": "Card suspension failed"},
    {"code": "DEC-194", "message": "Card revocation failed"},
    {"code": "DEC-195", "message": "Card withdrawal failed"},
    {"code": "DEC-196", "message": "Card recall failed"},
    {"code": "DEC-197", "message": "Card retrieval failed"},
    {"code": "DEC-198", "message": "Card recovery failed"},
    {"code": "DEC-199", "message": "Card replacement failed"},
    {"code": "DEC-200", "message": "Card renewal failed"},

    # 50 Missing responses (MIS-001 to MIS-050)
    {"code": "MIS-001", "message": "Missing card number"},
    {"code": "MIS-002", "message": "Missing expiration date"},
    {"code": "MIS-003", "message": "Missing CVV"},
    {"code": "MIS-004", "message": "Missing cardholder name"},
    {"code": "MIS-005", "message": "Missing billing address"},
    {"code": "MIS-006", "message": "Missing ZIP code"},
    {"code": "MIS-007", "message": "Missing country"},
    {"code": "MIS-008", "message": "Missing currency"},
    {"code": "MIS-009", "message": "Missing amount"},
    {"code": "MIS-010", "message": "Missing transaction ID"},
    {"code": "MIS-011", "message": "Missing merchant ID"},
    {"code": "MIS-012", "message": "Missing terminal ID"},
    {"code": "MIS-013", "message": "Missing acquirer ID"},
    {"code": "MIS-014", "message": "Missing issuer ID"},
    {"code": "MIS-015", "message": "Missing network ID"},
    {"code": "MIS-016", "message": "Missing API key"},
    {"code": "MIS-017", "message": "Missing authentication token"},
    {"code": "MIS-018", "message": "Missing session ID"},
    {"code": "MIS-019", "message": "Missing device fingerprint"},
    {"code": "MIS-020", "message": "Missing IP address"},
    {"code": "MIS-021", "message": "Missing user agent"},
    {"code": "MIS-022", "message": "Missing browser info"},
    {"code": "MIS-023", "message": "Missing OS info"},
    {"code": "MIS-024", "message": "Missing device info"},
    {"code": "MIS-025", "message": "Missing location data"},
    {"code": "MIS-026", "message": "Missing timezone"},
    {"code": "MIS-027", "message": "Missing timestamp"},
    {"code": "MIS-028", "message": "Missing reference number"},
    {"code": "MIS-029", "message": "Missing order ID"},
    {"code": "MIS-030", "message": "Missing customer ID"},
    {"code": "MIS-031", "message": "Missing payment method"},
    {"code": "MIS-032", "message": "Missing payment type"},
    {"code": "MIS-033", "message": "Missing payment channel"},
    {"code": "MIS-034", "message": "Missing payment source"},
    {"code": "MIS-035", "message": "Missing payment destination"},
    {"code": "MIS-036", "message": "Missing payment details"},
    {"code": "MIS-037", "message": "Missing payment instructions"},
    {"code": "MIS-038", "message": "Missing payment confirmation"},
    {"code": "MIS-039", "message": "Missing payment receipt"},
    {"code": "MIS-040", "message": "Missing payment authorization"},
    {"code": "MIS-041", "message": "Missing payment capture"},
    {"code": "MIS-042", "message": "Missing payment settlement"},
    {"code": "MIS-043", "message": "Missing payment reconciliation"},
    {"code": "MIS-044", "message": "Missing payment reporting"},
    {"code": "MIS-045", "message": "Missing payment monitoring"},
    {"code": "MIS-046", "message": "Missing payment verification"},
    {"code": "MIS-047", "message": "Missing payment validation"},
    {"code": "MIS-048", "message": "Missing payment authentication"},
    {"code": "MIS-049", "message": "Missing payment security"},
    {"code": "MIS-050", "message": "Missing payment compliance"}
]

@app.route('/key=<key>/cc=<card_data>', methods=['GET'])
def process_payment(key, card_data):
    """Process payment with 25-second delay & random decline response"""
    if key != API_KEY:
        return jsonify({"status": "error", "message": "Invalid API key"}), 401

    if not card_data or card_data.count('|') != 3:
        return jsonify({"status": "error", "message": "Invalid format. Use CC|MM|YY|CVV"}), 400

    # Simulate 25-second processing delay
    time.sleep(25)

    # Select a random decline response from all 250 possibilities
    decline = random.choice(DECLINE_RESPONSES)

    # Format response
    response = {
        "card_data": card_data,
        "response": decline,
        "status": "declined" if decline["code"].startswith("DEC") else "missing_data"
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333)
