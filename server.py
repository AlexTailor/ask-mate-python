from flask import Flask, render_template, request, redirect, url_for

import connection

app = Flask(__name__)


@app.route('/list')
def list_questions():
    questions = connection.get_csv_data()
    return render_template('list.html', questions=questions)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
