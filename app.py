from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop_un.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'your-secret-key-hereertrtygeterwtert'


db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    price = db.Column(db.Float, nullable=True)
    product_count = db.Column(db.Integer, default=1)
    brend = db.Column(db.String(50))
    description = db.Column(db.Text())
    image = db.Column(db.Text())


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(250), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    message = db.Column(db.Text(), nullable=True)


@app.route('/')
def index():
    popular_products = Product.query.all() #[:3]
    return render_template('index.html', popular_products=popular_products)


@app.route('/products')
def product_list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)


@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    popular_products = Product.query.all()#[:3]
    return render_template('product_detail.html', product=product, popular_products=popular_products) 


@app.route('/product/add', methods=['GET', 'POST'])
def product_add():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        product_count = request.form.get('product_count')
        brend = request.form.get('brend')
        description = request.form.get('description')
        image = request.files.get('image')

        filename = None
        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        product = Product(
            name=name,
            price=price,
            product_count=product_count,
            brend=brend,
            description=description,
            image=filename
        )

        db.session.add(product)
        db.session.commit()

        return redirect(url_for('product_list'))
    return render_template('product_add.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        message = request.form.get('message')

        contact = Contact(
            fullname=fullname,
            email=email,
            message=message
        )

        db.session.add(contact)
        db.session.commit()

        return redirect(url_for('index'))
        
    return render_template('contact.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

