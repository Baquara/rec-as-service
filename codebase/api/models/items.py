import datetime
from app import db, ma

#Definição da classe / tabela usuário e seus campos

class Items(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    item_name = db.Column(db.String(20), unique=True, nullable=False)
    item_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    created_on = db.Column(db.DateTime, default = datetime.datetime.now())

    def __init__(self,item_name,item_type,description):
        self.item_name = item_name
        self.item_type = item_type
        self.description = description

#Definindo o Schema do Marshmallow para facilitar a utilização de JSON
class ItemSchema(ma.Schema):
    class Meta:
        fields = ('id','item_name','item_type','description','created_on')

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

db.create_all()
db.session.commit()