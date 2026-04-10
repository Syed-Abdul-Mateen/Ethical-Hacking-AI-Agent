import os
from src.web_ui.app import create_app

if __name__ == "__main__":
    # Use the renamed 'configs' directory
    app = create_app('configs/agent_config.yaml')
    
    print("Starting Ethical Hacking AI Agent Web Interface...")
    print("Listening on http://127.0.0.1:5000")
    # Run the Flask development server
    app.run(host='0.0.0.0', port=5000, debug=True)
