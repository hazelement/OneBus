import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from app import app


if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.realpath(__file__)) + "/"

    cert = current_folder + "ssl/yychub.csr"
    key = current_folder + "ssl/yychub.key"

    context = (cert, key)
    # app.run(host='0.0.0.0', port=8080, threaded=True, debug=True, ssl_context=context)  # for deployment
    
    # app.run(debug=True, port=8000, host='localhost')
    # app.run(debug=True, port=8000, host='192.168.0.10')
    # app.run(debug=True, port=8000, host='0.0.0.0')
    # app.run(host='localhost', port=8000, ssl_context=context, threaded=True, debug=True)
    # app.run(host='localhost', threaded=True, debug=True)
    # app.run(host='192.168.0.4', port=8080, threaded=True, debug=True, ssl_context='adhoc')
    app.run(host='192.168.0.10', port=443, threaded=True, debug=True, ssl_context=context)
    # app.run(host='0.0.0.0', port=7563, threaded=True, debug=True, ssl_context=context)
