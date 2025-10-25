from flask import request, redirect, url_for, render_template, jsonify
from models import Transactions
from datetime import datetime

def register_routes(app, db):
    # Read operation
    @app.route('/')
    def get_transactions():
        transactions = Transactions.query.all()
        return render_template('transactions.html', transactions=transactions)

    # Create operation
    @app.route('/add_transaction', methods=['GET', 'POST'])
    def add_transaction():  
        if request.method == 'POST':
            date = datetime.strptime(request.form['date'], "%Y-%m-%d").date()
            amount = float(request.form['amount'])

            new_transaction = Transactions(date=date, amount=amount)
            db.session.add(new_transaction)
            db.session.commit()

            return redirect(url_for('get_transactions'))
        
        return render_template('form.html')

    # Update operation
    @app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
    def edit_transaction(transaction_id):
        transaction = Transactions.query.get_or_404(transaction_id)
        if request.method == 'POST':
            transaction.date = datetime.strptime(request.form['date'], "%Y-%m-%d").date()
            transaction.amount = float(request.form['amount'])
            db.session.commit()
            return redirect(url_for('get_transactions'))                
            
        return render_template('edit.html', transaction=transaction)

    # Delete operation
    @app.route('/delete_transaction/<int:transaction_id>')
    def delete_transaction(transaction_id):

        transaction = Transactions.query.get_or_404(transaction_id)
        db.session.delete(transaction)
        db.session.commit()

        return redirect(url_for('get_transactions'))

    # Search operation
    @app.route('/search', methods=['GET', 'POST'])
    def search_transaction():
        if request.method == 'POST':
            min_amount = float(request.form['min_amount'])
            max_amount = float(request.form['max_amount'])

            transactions = Transactions.query.filter(
                Transactions.amount.between(min_amount, max_amount)
            ).all()
            return render_template('search.html', transactions=transactions)

        return render_template('search.html')

    # Total balance
    @app.route('/balance')
    def total_balance():
        total = db.session.query(db.func.sum(Transactions.amount)).scalar()
        return jsonify({'Total Balance': total})