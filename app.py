from flask import Flask, render_template, request, jsonify
from controllers.vmcontroller import SearchVms

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    form = request.form
    _search = SearchVms().get(dict(form))
    return render_template('index.html', vmList = _search)



@app.errorhandler(404)
def pageNotFound(e):
    return render_template('errors/404.html'), 404

if __name__ == '__main__':
   app.run()