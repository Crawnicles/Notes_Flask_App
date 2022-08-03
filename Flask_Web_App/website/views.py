from unicodedata import category
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from website.models import Transaction
from . import db
import json


views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        transaction = request.form.get('transaction')

        if len(transaction) < 1:
            flash('Transaction is too short!', category='error')
        else:
            new_transaction = Transaction(data=transaction, user_id=current_user.id)
            db.session.add(new_transaction)
            db.session.commit()
            flash('Transaction added!', category='success')
            
    return render_template("home.html", user=current_user)

@views.route('/delete-transaction', methods=['POST'])
def delete_transaction():
    transaction = json.loads(request.data)
    transactionId = transaction['tranactionId']
    transaction = Transaction.query.get(transactionId)
    if transaction:
        if transaction.user_id == current_user.id:
            db.session.delete(new_transaction)
            db.session.commit()
    
    return jsonify({})