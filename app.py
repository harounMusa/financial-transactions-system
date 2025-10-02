# Import libraries
from flask import Flask, request, redirect, url_for, render_template, jsonify

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route('/')
def get_transactions():
    return render_template('transactions.html', transactions=transactions)

# Create operation
@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
        
    if request.method == 'POST':
        date = request.form['date']
        amount = request.form['amount']

        if date and amount:
            if len(transactions) > 0:
                new_id = transactions[-1]['id'] + 1
            else:
                new_id = 1
            new_transaction = {'id': new_id,
                                'date': date,
                                'amount': amount}
            
            transactions.append(new_transaction)

        return redirect(url_for('get_transactions'))
    
    return render_template('form.html')

# Update operation
@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        date = request.form['date']
        amount = request.form['amount']
        for transaction in transactions:
            if transaction_id == transaction['id']:
                transaction['date'] = date
                transaction['amount'] = amount
                break
                
        return redirect(url_for('get_transactions'))
    
    for transaction in transactions:
        if transaction_id == transaction['id']:
            return render_template('edit.html', transaction=transaction)
        
    return {'message': 'id not found '}, 404
# Delete operation
@app.route('/delete_transaction/<int:transaction_id>')
def delete_transaction(transaction_id):
    for t in transactions:
        if t['id'] == transaction_id:
            transactions.remove(t)
            break

    return redirect(url_for('get_transactions'))

# Search operation
@app.route('/search', methods=['GET', 'POST'])
def search_transaction():
    if request.method == 'POST':
        min_amount = request.form['min_amount']
        max_amount = request.form['max_amount']
        
        new_list = []
        for t in transactions:
            if float(min_amount) <= float(t['amount']) <= float(max_amount):
                new_list.append(t)
        return render_template('transactions.html', transactions=new_list)

    return render_template('search.html')

# Total balance
@app.route('/balance')
def total_balance():
    result = 0
    for t in transactions:
        result += float(t['amount'])
    return jsonify({'Total Balance': result})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
   