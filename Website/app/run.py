import sys
import os

# radius parameter on both search around tops and places around stops should be smaller

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from app import app

# app.run(debug=True, port=8000, host='localhost')
app.run(debug=True, port=8000, host='192.168.0.10')
# app.run(debug=True, port=8000, host='0.0.0.0')

