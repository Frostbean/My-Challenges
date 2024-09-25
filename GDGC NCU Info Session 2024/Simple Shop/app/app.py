from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

flag = "NCtfU{H0w_d1d_y0u_buy_7h3_flag_4w4y?}"

products = [
    {'id': 1, 'name': 'Laptop', 'price': 1000, 'buyable': True, 'image_url': 'logo.png'},
    {'id': 2, 'name': 'The not for Sale Flag', 'price': 1000000, 'buyable': False, 'image_url': 'flag.jpg'},
    {'id': 3, 'name': 'Headphones', 'price': 100, 'buyable': True, 'image_url': 'logo.png'},
    {'id': 4, 'name': 'Smartwatch', 'price': 200, 'buyable': True, 'image_url': 'logo.png'},
    {'id': 5, 'name': 'Camera', 'price': 700, 'buyable': True, 'image_url': 'logo.png'},
    {'id': 6, 'name': 'Tablet', 'price': 300, 'buyable': True, 'image_url': 'logo.png'}
]

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('index.html', products=products, balance=session.get('balance', 0))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        session['balance'] = 1000
        return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/buy/<int:product_id>')
def buy(product_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        balance = session.get('balance', 0)
        quantity = int(request.args.get('quantity', 1))
        total_price = product['price'] * quantity

        if balance >= total_price:
            session['balance'] = balance - total_price
            if product['name'] == "The not for Sale Flag":
                return render_template('purchase.html', product=product, quantity=quantity, total_price=total_price, balance=session['balance'], flag=True, flag_content=flag)
            return render_template('purchase.html', product=product, quantity=quantity, total_price=total_price, balance=session['balance'], flag=False)
        else:
            return render_template('index.html', products=products, balance=balance, error="Insufficient funds!")
    
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
