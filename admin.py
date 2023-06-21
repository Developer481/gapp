from flask import Flask
import prat  # Import your Flask app

app = prat.app  # Access the Flask app object from the prat module

# Run your Flask app
if __name__ == "__main__":
    app.run()
