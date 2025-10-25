from app import create_app

flask_app = create_app()

# Run the Flask app
if __name__ == '__main__':
    flask_app.run(debug=True)