from flask import Blueprint, flash, render_template, request, jsonify, send_file
from flask import current_app as app
from . import database as db
import os
import csv
import time

from .dashboard import update_ml
from escalation import scheduler, PERSISTENT_STORAGE, LEADERBOARDS


def create_leaderboard_csv():
    rows = [x.__dict__ for x in db.get_leaderboard()]
    fieldnames = ['dataset_name', 'githash', 'run_id', 'created', 'model_name', 'model_author', 'accuracy',
                  'balanced_accuracy', 'auc_score', 'average_precision', 'f1_score', 'precision', 'recall',
                  'samples_in_train', 'samples_in_test', 'model_description', 'column_predicted', 'num_features_used',
                  'data_and_split_description', 'normalized', 'num_features_normalized', 'feature_extraction',
                  'was_untested_data_predicted']
    csv_filename = os.path.join(app.config[PERSISTENT_STORAGE],
                           LEADERBOARDS,
                           "escalation.leaderboard.%s.csv" % time.strftime("%Y-%m-%d-%H%M%S", time.localtime()))
    with open(csv_filename, 'w') as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator='\n', extrasaction='ignore')
        writer.writeheader()
        for elem in rows:
            writer.writerow(elem)
    return csv_filename


bp = Blueprint('leaderboard', __name__)


@bp.route('/leaderboard', methods=('GET', 'POST'))
def leaderboard():
    if request.method == 'POST' and request.headers.get('User-Agent') == 'escalation':
        error = db.add_leaderboard(request.form)
        if error:
            app.logger.info(error)
            return jsonify({'error': error}), 400

        job3 = scheduler.add_job(func=update_ml, args=[], id='update_ml')
    elif request.method == 'POST' and request.form['submit'] == 'Download CSV':
        csv_filename = create_leaderboard_csv()
        return send_file(csv_filename, as_attachment=True)
    elif request.method == 'POST' and 'submit' in request.form and request.form['submit'] == 'Delete':
        if request.form['adminkey'] != app.config['ADMIN_KEY']:
            flash("Incorrect admin code")
        else:
            requested = [int(x) for x in request.form.getlist('delete')]
            for id in requested:
                db.remove_leaderboard(id)

            job3 = scheduler.add_job(func=update_ml, args=[], id='update_ml')

    return render_template('leaderboard.html', table=db.get_leaderboard())
