# flask-saml2-okta
Flask app use SAML2.0 integrated with OKTA for SSO

### .env example

```aidl
export FLASK_APP=/home/ram/Desktop/flask-saml2-okta/application.py
export FLASK_DEBUG=1
export APP_SECRET=YOUR_PROJ_SECRET_FOR_ENV
```

### Development

```bash
pip install -r requirements/dev.txt

source .env
flask run --with-threads

curl http://localhost:5000/api/user
```

