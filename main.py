from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///storage.db"
db = SQLAlchemy(app)
#######
class Produto(db.Model):
  __tablename__ = 'produto'
  id = db.Column(db.Integer,primary_key=True)
  codigo = db.Column(db.String,unique=True,nullable=False)
  nome = db.Column(db.String,unique=True,nullable=False)
  quantidade = db.Column(db.Float,nullable = False, default=0.0)
  descricao = db.Column(db.Text,default='Sem Descrição')
  def __init__(self,codigo:str,nome:str,quantidade:float,descricao:str):
    self.codigo = codigo
    self.nome = nome
    self.quantidade = quantidade
    self.descricao = descricao
    
  @property
  def get(self):
    return {
      'id':self.id,
      'codigo':self.codigo,
      'nome':self.nome,
      'quantidade':self.quantidade,
      'descricao':self.descricao
      }
  
  def update(self,dados:dict):
    ...
##############

@app.route('/',methods=['GET','POST'])
def route_index():
    if request.method == 'GET':
      return render_template('index.html',resp={})
    elif request.method == 'POST':
      data = dict(request.form)
      requeriments = ['codigo','nome','quantidade','descricao']
      types = [str,str,float,str]
      for index,key in enumerate(requeriments):
        if key not in data:
          return render_template('index.html',resp={'message':'Está faltando um valor!'})
        if types[index] == float:
        
          try:
            data[key] = float(data[key])
          except:
            print('error')
            return render_template('index.html',resp={'message':'O valor passado não é um flaot'})
      
      try:
        db.session.add(Produto(data['codigo'],data['nome'],data['quantidade'],data['descricao']))
        db.session.commit()
        render_template('index.html',resp={'message':'Registrado Com Sucesso!'})
        return render_template('index.html',resp={'message':'Registrado Com Sucesso!'})

      except:
        return render_template('index.html',resp={'message':'O Nome ou o Codigo ja está registrado!'})
@app.route('/view',methods=['GET','POST'])
def route_view():
  print(request.method)
  if request.method == 'GET':
    data = [produto.get for produto in Produto.query.all()]
    return render_template('view.html',data=data)
  elif request.method == 'POST':
    print('aqui')
    form = dict(request.form)
    if 'id' in form:
      try:
        
        id = int(form['id'])
        db.session.delete(Produto.query.get(id))
        db.session.commit()
      except:
        ...
    data = [produto.get for produto in Produto.query.all()]
    return render_template('view.html',data=data)
    
    
if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8080)
    
