from flask import Flask, request, abort
import mirador


app = Flask(__name__)
mc = mirador.MiradorClient('apitest')


@app.route('/moderate', methods=('POST',))
def moderate():
    image = request.files.get('image', None)

    if not image or not image.stream:
        return abort(400)

    res = mc.classify_file(image)
    safe_str = 'Safe' if res.safe else 'Unsafe'

    return """
    <!doctype html>
    <h4>The Image is {} - {}</h4>
    """.format(safe_str, res.value)


@app.route('/')
def index():

    return """
    <!doctype html>
    <h1>Moderate Image</h1>
    <form action="/moderate" method=post enctype=multipart/form-data>
        <input type=file accept='image/jpg,image/jpeg,image/png' name=image>
        <input type=submit value=Moderate>
    </form>
    """


if __name__ == '__main__':
    app.run()
