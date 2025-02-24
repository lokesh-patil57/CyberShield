from app import app

if __name__ == "__main__":
    # Always serve on port 5000 with host 0.0.0.0 to make it accessible
    app.run(host='0.0.0.0', port=5000, debug=True)