from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Your Gmail address
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Your App Password
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

@app.route('/send-enquiry', methods=['POST'])
def send_enquiry():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        message = data.get('message')

        if not name or not email or not phone or not message:
            return jsonify({'message': 'All fields are required'}), 400

        # Send Email
        msg = Message(
            subject=f"Enquiry from {name}",
            recipients=[os.getenv('MAIL_USERNAME')],  # Your Gmail address
            body=f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
        )
        mail.send(msg)

        return jsonify({'message': 'Enquiry sent successfully!'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Failed to send enquiry'}), 500


if __name__ == '__main__':
    app.run(debug=True)
