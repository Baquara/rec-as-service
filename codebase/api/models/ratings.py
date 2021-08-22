import datetime
from app import db, ma


class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    id_user = db.Column(db.Integer, nullable = False)
    id_item = db.Column(db.Integer, nullable = False)
    created_on = db.Column(db.DateTime, default = datetime.datetime.now())

    def __init__(self,id_user,id_item):
        self.id_user = id_user
        self.id_item = id_item

class RatingsSchema(ma.Schema):
    class Meta:
        fields = ('id','id_user','id_item','created_on')

rating_schema = RatingsSchema()
ratings_schema = RatingsSchema(many=True)

db.create_all()
db.session.commit()