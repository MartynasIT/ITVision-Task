from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from init_db import base, Calls
from flask import jsonify
import time
import random
from helpers import Helpers
app = Flask("CallLogs")

# connecting to db
engine = create_engine('sqlite:///CallLog.db?check_same_thread=False')
base.metadata.bind = engine
# session
db_session = sessionmaker(bind=engine)
session = db_session()


# Routes for requests
# get all logs
@app.route('/getLogs')
def show_log():
    return get_calls()


# log incoming call
@app.route('/logCall', methods=['POST'])
def new_call():
    if request.method == 'POST':
        direction = None
        dialed_number = None

        try:
            dialed_number = request.json.get('DialedNumber', '')
            direction = request.json.get('Direction', '')
        except KeyError:
            pass
        # passed data is fetched
        uu_id = request.json.get('UUID', '')
        caller_id = request.json.get('CallerID', '')
        extension = request.json.get('Extension', '')
        # helper class instantiated to simulate call
        helpers = Helpers(None, None, 0, None)
        call_start_time = helpers.start_call_time()
        log_call(helpers, uu_id, call_start_time, caller_id,
                 extension, dialed_number, direction)
        return '', 204


# get single log from db
@app.route('/getLog/<string:uu_id>', methods=['GET'])
def request_call(uu_id):
    return get_call(uu_id)


def get_calls():
    calls = session.query(Calls).all()
    return jsonify(Calls=[call.serialize for call in calls])


def get_call(uu_id):
    call = session.query(Calls).filter_by(UUID=uu_id).one()
    return jsonify(Calls=call.serialize)


def log_call(helpers, uu_id, call_start_time, caller_id,
             extension, dialed_number, direction):
    helpers.start_call_time()
    result = Calls(UUID=uu_id, CallStartTime=call_start_time, CallerID=caller_id,
                   Extension=extension, DialedNumber=dialed_number, Direction=direction)
    session.add(result)
    session.commit()
    proceed_call(helpers, uu_id)


# deciding how to simulate call
def proceed_call(helpers, uu_id):
    action = helpers.pick_action()
    # user hung up
    if action == "Call failed":
        helpers.end_call_time()
        unsucc_call(helpers, uu_id)
    # call was forwarded to group but no one picked up
    if action == "Move to group with 300":
        # simulate waiting for pick up to avoid having call time being zero
        wait_time = random.randint(1, 7)
        time.sleep(wait_time)
        helpers.end_call_time()
        unsucc_call(helpers, uu_id, group=300)
    else:
        helpers.end_call_time()
        update_call(uu_id, call_end_time=helpers.get_call_end(), duration=helpers.total_call_time(),
                    bill_sec=helpers.get_chat_duration(), extension=200, answer_state=helpers.get_answer_state())


# to avoid same code when phone was not picked up
def unsucc_call(helpers, uu_id, group=None):
    helpers.end_call_time()
    update_call(uu_id, call_end_time=helpers.get_call_end(), duration=helpers.total_call_time(),
                bill_sec=helpers.get_chat_duration(), extension=group, answer_state=helpers.get_answer_state())


# update data in db after call ends
def update_call(uu_id, extension=None, answer_state=None, bill_sec=None,
                duration=None, call_end_time=None):
    update = session.query(Calls).filter_by(UUID=uu_id).one()
    if extension is not None:
        update.Extension = extension
    if answer_state is not None:
        update.AnswerState = answer_state
    if bill_sec is not None:
        update.Billsec = bill_sec
    if duration is not None:
        update.Duration = duration
    if call_end_time is not None:
        update.CallEndTime = call_end_time

    session.add(update)
    session.commit()


if __name__ == '__main__':
    app.run(host='localhost', port=900)
