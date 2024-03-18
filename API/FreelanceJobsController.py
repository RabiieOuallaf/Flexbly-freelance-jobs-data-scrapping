from flask import Flask, jsonify, request
from FreelanceJobsService import scrap_freelancer_jobs

app = Flask(__name__)


@app.route('/api/v1/freelance')
def scrap_freelance_jobs():
    filters = request.args.to_dict()
    jobs = scrap_freelancer_jobs(filters)
    return jsonify(jobs)


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


if __name__ == '__main__':
    app.run()
