from flask import Flask, redirect, url_for,jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/SEdb"
mongo = PyMongo(app)

#notes with a particular tag
@app.route('/notes/<tag>')
def get_notes(tag):
    notes = mongo.db.notes.find({'tag':tag})
    return dumps(notes)

#latest notes with a particular tag
@app.route('/notes/<tag>/latest')
def get_latest(tag):
    notes = mongo.db.notes.find({'tag':tag}).sort([('time',-1)])
    return dumps(notes)

#most popular notes based on tag
@app.route('/notes/<tag>/popular')
def get_popular(tag):
    notes = mongo.db.notes.find({'tag':tag}).sort([('upvotes',-1)])
    return dumps(notes)

#upvote notes
@app.route('/notes/<ID>/upvote/')
def upvote(ID):
	v=mongo.db.notes.find_one({"_id":ObjectId(ID)})['upvotes']
	mongo.db.notes.update({"_id":ObjectId(ID)},{"$set":{'upvotes':v+1}})
	return jsonify({'upvote':v+1})
	
#downvote notes
@app.route('/notes/<ID>/downvote/')
def upvote(ID):
	v=mongo.db.notes.find_one({"_id":ObjectId(ID)})['downvotes']
	mongo.db.notes.update({"_id":ObjectId(ID)},{"$set":{'downvotes':v-1}})
	return jsonify({'downvote':v-1})
    
if __name__ == '__main__':
   app.run(debug = True)
