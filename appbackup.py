from flask import Flask, render_template, request, jsonify
import requests
import datetime
import sys
import os
# from main import query_travel_agent  # Import the query function from main.py
app = Flask(__name__)

BASE_URL = "http://localhost:8000"  # Backend endpoint

@app.route('/')
def index():
    """Serve the main recruitment interface"""
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    """Handle recruitment queries from the frontend"""
    print("Received query request")
    try:
        user_input = request.json.get('question', '').strip()
        
        if not user_input:
            return jsonify({
                'error': 'Please provide a recruitment question',
                'success': False
            }), 400
        
        # Send request to your recruitment backend
        payload = {"question": user_input}
        print(f"Sending query to backend: {payload}")
        # response = query_travel_agent(payload)  # Call the function directly
        response = requests.post(f"{BASE_URL}/query", json=payload, timeout=30)
        print(f'Backend response: {response.status_code}', file=sys.stderr)
        
        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            
            # Format the response for the premium UI
            formatted_response = {
                'answer': answer,
                'generated_at': datetime.datetime.now().strftime('%Y-%m-%d at %H:%M'),
                'success': True,
                'query': user_input  # Include original query for context
            }
            
            return jsonify(formatted_response)
        else:
            return jsonify({
                'error': f'AI service temporarily unavailable: {response.text}',
                'success': False
            }), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Request timeout - the AI is taking longer than expected. Please try again.',
            'success': False
        }), 504
        
    except requests.exceptions.ConnectionError:
        return jsonify({
            'error': 'Cannot connect to AI service. Please ensure the backend is running on port 8000.',
            'success': False
        }), 503
        
    except Exception as e:
        print(f"Error in query endpoint: {str(e)}", file=sys.stderr)
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'success': False
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'backend_url': BASE_URL
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print("Created 'templates' directory")
    
    print("🚀 Starting Elite Recruitment Intelligence Platform...")
    print("📍 Access the application at: http://localhost:5000")
    print("🔧 Backend should be running at: http://localhost:8000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)