import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# 000 no movement
# 001 unknown
# 010 unknown
# 011 unknown
# 100 unknown
# 101 uknown
# 110 unkown
# 111 wasn't ever observed

CHAIR_MOVEMENT_TO_LINES = dict(
    top_up=('line0',),              # 001
    mid_up=('line1',),              # 010
    bot_down=('line0', 'line1'),    # 011
    bot_up=('line2',),              # 100
    top_down=('line0', 'line2'),    # 101
    mid_down=('line1', 'line2'),    # 110
    debug=('line0', 'line1', 'line2') # 111
)


@app.route('/chair_movement', methods=['PATCH'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

app.run()