import pyttsx3
import paypalrestsdk
import requests

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed percent (can go over 100)
engine.setProperty('volume', 0.2)  # Volume 0-1

# Initialize PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "AUFV0w8TNE3EanqrSYHNB6CtP2MrzUbjJIM2OzYccqB-_WDHwlQ1u-v1QKgxtES4u8Y27u01eqPf7bbp",
    "client_secret": "EE7920dV58xG2DRo5_yRCxotPCHq5W5dEWzJcOjWf-3_mlnoeCWoXtHrhg0isteSGD7GFKqhH28jpeHA"})

# Function to speak text
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Function to convert INR to USD
def convert_inr_to_usd(amount_inr):
    # Note: This is a simplified example. For real applications, use a reliable currency conversion API.
    conversion_rate = 0.013  # Approximate conversion rate (1 INR ≈ 0.013 USD)
    amount_usd = amount_inr * conversion_rate
    return round(amount_usd, 2)

# Function to execute PayPal payment
def execute_payment(recipient, amount_inr, secret_pin):
    amount_usd = convert_inr_to_usd(amount_inr)
    if secret_pin != "1234":  # Replace with your logic to check the secret pin
        speak_text("Incorrect secret pin. Transaction halted.")
        print("Incorrect secret pin. Transaction halted.")
        return

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "transactions": [{
            "amount": {
                "total": f"{amount_usd}",
                "currency": "USD"},  # Changed to USD
            "description": f"Payment to {recipient} (₹{amount_inr})"}],
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/payment/cancel"}})

    if payment.create():
        speak_text(f"Payment of ₹{amount_inr} (${amount_usd}) to {recipient} created successfully.")
        print(f"Payment of ₹{amount_inr} (${amount_usd}) to {recipient} created successfully.")
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = link.href
                speak_text(f"Please visit this URL to approve the payment: {approval_url}")
                print(f"Approval URL: {approval_url}")
                break
    else:
        speak_text(f"Payment failed. {payment.error}")
        print(f"Payment failed. {payment.error}")

# Main Function
def main():
    recipient = input("Who do you want to pay? ")

    while True:
        amount = input("How much would you like to send? ")
        try:
            amount_inr = float(amount)  # Convert the input amount to a number
            break
        except ValueError:
            print("I didn't catch that. Could you please enter the number again?")
            continue

    confirmation = input(f"You are sending ₹{amount_inr} to {recipient}. Type 'yes' to confirm: ")
    if confirmation.lower() != "yes":
        speak_text("Transaction cancelled.")
        print("Transaction cancelled.")
        return

    secret_pin = input("Please provide your secret pin: ")

    execute_payment(recipient, amount_inr, secret_pin)

if __name__ == "__main__":
    main()
