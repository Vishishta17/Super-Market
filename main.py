from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import json

local_server= True
app = Flask(__name__)
app.secret_key='hmsprojects'


login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/ver6'
db=SQLAlchemy(app)


class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    usertype=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class Orders(db.Model):
    oid=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50))
    name=db.Column(db.String(50))
    item=db.Column(db.String(50))
    quantity=db.Column(db.Integer)
    method=db.Column(db.String(50))
    time=db.Column(db.String(50),nullable=False)
    date=db.Column(db.String(50),nullable=False)
    category=db.Column(db.String(50))
    number=db.Column(db.String(50))
    details = db.relationship('Details', backref='Orders', cascade='all, delete')

class Products(db.Model):
    pid=db.Column(db.Integer,primary_key=True)
    productname=db.Column(db.String(50))
    brand=db.Column(db.String(50))
    price=db.Column(db.Integer)

class Trigr(db.Model):
    tid=db.Column(db.Integer,primary_key=True)
    oid=db.Column(db.Integer)
    email=db.Column(db.String(50))
    name=db.Column(db.String(50))
    action=db.Column(db.String(50))
    timestamp=db.Column(db.String(50))

class Details(db.Model):
    detail_id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey('products.pid'), nullable=False)
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    oid = db.Column(db.Integer, db.ForeignKey('orders.oid', ondelete='CASCADE'))
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255))
    productname = db.Column(db.String(255))
    unitprice = db.Column(db.Integer)
    product = db.relationship('Products', backref='Details')
    user = db.relationship('User', backref='Details')
    order = db.relationship('Orders', backref='Details')
    


@app.route('/')
def index():
    return render_template('index.html')
   


@app.route('/product',methods=['POST','GET'])
def products():

    if request.method=="POST":

        productname=request.form.get('productname')
        brand=request.form.get('brand')
        price=request.form.get('price')
        query=Products(productname=productname,brand=brand,price=price)
        db.session.add(query)
        db.session.commit()
        flash(" Product Information is Added","primary")
    return render_template('product.html')



@app.route('/order',methods=['POST','GET'])
@login_required
def orders():
    products=Products.query.all()

    if request.method=="POST":
        email=request.form.get('email')
        name=request.form.get('name')
        item=request.form.get('item')
        quantity=request.form.get('quantity')
        method=request.form.get('method')
        time=request.form.get('time')
        date=request.form.get('date')
        category=request.form.get('category')
        number=request.form.get('number')
        if len(number)<10 or len(number)>10:
            flash("Please give 10 digit number")
            return render_template('order.html',products=products)
        query=Orders(email=email,name=name,item=item,quantity=quantity,method=method,time=time,date=date,category=category,number=number)
        db.session.add(query)
        db.session.commit()
        flash("Order Placed","info")
    return render_template('order.html',products=products)



@app.route('/detail', methods=['POST'])
@login_required
def update_details():
    pid = request.form.get('pid')
    id = request.form.get('id')
    oid = request.form.get('oid')
    quantity = request.form.get('quantity')
    order = Orders.query.filter_by(oid=oid).first()
    product = Products.query.filter_by(pid=pid).first()
    name = order.name
    productname = product.productname
    unitprice = product.price
    total_price = int(quantity) * unitprice
    existing_detail = Details.query.filter_by(pid=pid, oid=oid).first()
    if existing_detail:
        existing_detail.id = id
        existing_detail.quantity = quantity
        existing_detail.total_price = total_price
        existing_detail.name = name
        existing_detail.productname = productname
        existing_detail.unitprice = unitprice
    else:
        new_detail = Details(
            pid=pid,
            id=id,
            oid=oid,
            quantity=quantity,
            total_price=total_price,
            name=name,
            productname=productname,
            unitprice=unitprice
        )
        db.session.add(new_detail)
    db.session.commit()
    return new_detail



@app.route('/detail')
@login_required
def bookings(): 
    em = current_user.email
    if current_user.usertype == "Owner":
        orders = Orders.query.all()
    else:
        orders = Orders.query.filter_by(email=em).all()

    # Fetch unitprice and total_price from Details table for each order
    details_data = []
    for order in orders:
        details = Details.query.filter_by(oid=order.oid).first()
        if details:
            details_data.append({
                'oid': order.oid,
                'unitprice': details.unitprice,
                'total_price': details.total_price
            })
        else:
            details_data.append({
                'oid': order.oid,
                'unitprice': None,
                'total_price': None
            })
    return render_template('detail.html', orders=orders, details_data=details_data)



@app.route("/edit/<int:oid>", methods=['POST', 'GET'])
@login_required
def edit(oid):    
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        item = request.form.get('item')
        quantity = request.form.get('quantity')
        method = request.form.get('method')
        time = request.form.get('time')
        date = request.form.get('date')
        category = request.form.get('category')
        number = request.form.get('number')
        post = Orders.query.get(oid)  # Using get() instead of filter_by().first()
        details = Details.query.filter_by(oid=oid).first()
        post.email = email
        post.name = name
        post.item = item
        post.quantity = quantity
        post.method = method
        post.time = time
        post.date = date
        post.category = category
        post.number = number
        details.quantity = int(post.quantity)
        details.total_price = int(post.quantity) * int(details.unitprice)
        details.name = post.name
        details.productname=post.item
        db.session.commit()
        flash("Slot is Updated", "success")
        return redirect('/detail')
    post = Orders.query.get(oid)
    details=Details.query.filter_by(oid=oid).first()
    return render_template('edit.html', posts=post,details=details)



@app.route("/delete/<int:oid>",methods=['POST','GET'])
@login_required
def delete(oid):
    query=Orders.query.filter_by(oid=oid).first()
    db.session.delete(query)
    db.session.commit()
    flash("Slot Deleted Successful","danger")
    return redirect('/detail')



@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        usertype=request.form.get('usertype')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        myquery=User(username=username,usertype=usertype,email=email,password=password)
        db.session.add(myquery)
        db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

    return render_template('signup.html')



@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    
    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))



@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'



@app.route('/details')
@login_required
def details():
    posts=Trigr.query.all()
    return render_template('trigers.html',posts=posts)



@app.route('/search',methods=['POST','GET'])
@login_required
def search():
    if request.method=="POST":
        query=request.form.get('search')
        brand=Products.query.filter_by(brand=query).first()
        name=Products.query.filter_by(productname=query).first()
        if name:

            flash("Item is Available","info")
        else:

            flash("Item is Not Available","danger")
    return render_template('index.html')

app.run(debug=True)    

