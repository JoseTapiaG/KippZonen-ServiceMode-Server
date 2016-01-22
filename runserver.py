from kippzonenserver import app

if __name__ == "__main__":
    app.config["SECRET_KEY"] = "ITSASECRET"
    app.run(port=5000, debug=True)