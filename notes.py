from flask import Flask, redirect, url_for,jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/SEdb"
mongo = PyMongo(app)

#sample JSONs
'''
{
	"_id" : ObjectId("5bc0de4d7495c3f50f6c5bd6"),
	"tag" : "ML",
	"course" : 1,
	"upvotes" : 10,
	"downvotes" : 2,
	"title" : "Neural networks",
	"summary" : "An overview of neural networks",
	"block" : 0,
	"islink" : 1,
	"link" : "http://neuralnetworksanddeeplearning.com/chap1.html",
	"time" : ISODate("2018-10-12T17:47:57.933Z")
}
{
	"_id" : ObjectId("5bc22037fdc52ba0ad988d64"),
	"tag" : "ML",
	"course" : 1,
	"upvotes" : 10,
	"downvotes" : 2,
	"title" : "Regression",
	"summary" : "A brief of linear and logistic regression",
	"block" : 0,
	"islink" : 1,
	"link" : "https://www.listendata.com/2014/11/difference-between-linear-regression.html",
	"time" : ISODate("2018-10-13T16:41:27.899Z")
}
{
	"_id" : ObjectId("5bc220e2fdc52ba0ad988d65"),
	"tag" : "OOMD",
	"course" : 1,
	"upvotes" : 11,
	"downvotes" : 2,
	"title" : "OOMD",
	"summary" : "Unit 2",
	"block" : 0,
	"islink" : 1,
	"link" : "https://drive.google.com/file/d/1QNVuZ1vuKdnwIfRcv1FygFaiNlh6fYLM/view?usp=sharing",
	"time" : ISODate("2018-10-13T16:44:18.340Z")
}
'''

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
