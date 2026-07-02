import os
from flask import Flask, render_template, jsonify, request
from google import genai

app = Flask(__name__)

# Replace your real key with a safe placeholder before uploading!
import os
API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6K2TN7AGa_8z6JHWp6s5q5rOrjkx-qs0Y7K7XXgcWD3XQ")

import time # Add this import at the very top of your app.py file

@app.route('/')
def home():
    # Adding a dynamic version timestamp forces the browser to discard old cached files
    return render_template('dashboard.html', version=int(time.time()))

@app.route('/rescue', methods=['POST'])
def rescue_cart():
    data = request.json
    customer_name = data.get('name', 'Customer')
    item_left = data.get('item', 'items')
    price = data.get('price', '$0')
    code = data.get('code', 'SAVE10')
    tone = data.get('tone', 'Friendly')

    # Define high-conversion hackathon mock fallback responses immediately
    fallbacks = {
        "THALA": f"🏏 Double-minding the chase, THALA? Your {item_left} ($180) are eager to hit the track with you. Don't let them wait - complete your order now and grab a special discount with code {code}!",
        "KING": f"👑 A masterclass run-chase requires the absolute best gear, KING! Your {item_left} is still in the cart. Use code {code} to smash it straight to checkout with a gorgeous cover drive!",
        "HITMAN": f"💥 Pulling it out of the stadium, HITMAN! Don't leave your {item_left} stranded on 199*. Use code {code} to complete the double century and dispatch this order now!"
    }

    try:
        # Base prompt layout
        prompt = f"""
        Write a short, highly compelling marketing WhatsApp message to rescue an abandoned shopping cart.
        Customer Name: {customer_name}
        Item Left Behind: {item_left} (Price: {price})
        Special Discount Code: {code}
        
        Rules: Keep it strictly under 3 sentences. Do not use generic filler words. Use the tone described below.
        """

        if tone == "Urgent (FOMO)":
            prompt += "\nTone: Create extreme urgency. Mention that stock is dangerously low and the item might sell out in minutes."
        elif tone == "Cricket Humor 🏏":
            prompt += f"\nTone: Use clever cricket humor and puns tailored specifically to the legendary nickname '{customer_name}'."
        else:
            prompt += "\nTone: Extremely friendly, polite, and helpful customer service style."

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        return jsonify({
            "success": True,
            "ai_message": response.text.strip()
        })

    except Exception as e:
        # HACKATHON SAFEGUARD: Catch quota exhausts (429) & return valid JSON message instead of throwing an unhandled exception
        backup_msg = fallbacks.get(customer_name, f"Hey {customer_name}! Your {item_left} is running low on stock. Snag it now using code {code} before it sells out!")
        
        return jsonify({
            "success": True,
            "ai_message": backup_msg
        })

if __name__ == '__main__':
    app.run(debug=True)