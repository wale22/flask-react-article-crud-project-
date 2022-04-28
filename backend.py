from datetime import datetime
from flask import Flask, jsonify,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://wale:walexi202@localhost/reactflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
ma=Marshmallow(app)


class Articles(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.Text)
    title=db.Column(db.String(100))
    time= db.Column(db.DateTime, default=datetime.utcnow)   

    def __init__(self,content,title) :
        self.content=content
        self.title=title 



class userScheme(ma.Schema):
    class meta:
        fields = ('id','content','title')


article_schema= userScheme()
articles_schema= userScheme(many = True)



app.route('/get', method = ['GET'])
def getall():
    articles=Articles.query.all()
    result= articles_schema.dump(articles)
    return jsonify(result)



app.route('/get/<id>', method = ['GET'])
def getspec(id):
    article=Articles.query.get(id)
    result=article_schema.jsonify(article)


@app.route('/add', method=['POST'])
def add():
    title=request.json[title]
    content=request.json[content]

    article=Articles(content,title)
    db.session.add(article)
    db.session.commit()
    return article_schema.jsonify(article)


app.route('/update/<id>', method = ['PUT'])
def update(id):
    article=Articles.query.get(id)
    content= request.json[content]
    title=request.json[title]

    article.title=title
    article.content=content

    db.session.commit()
    return article_schema.jsonify(article) 


app.route('/delete/<id>', method = ['DELETE'])
def delete(id):
    article=Articles.query.get(id)
    db.session.delete(article)
    db.session.commit
    return article_schema.jsonify(article)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


