from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import Transaction
from datetime import datetime

expense_routes = Blueprint('expense_routes', __name__)

# ✅ Add a transaction (income or expense)
@expense_routes.route('/transactions', methods=['POST'])
@jwt_required()
def add_transaction():
    data = request.get_json()
    user_id = get_jwt_identity()

    if not data.get("amount"):
        return jsonify({"error": "Amount is required"}), 400

    try:
        amount = float(data["amount"])
    except ValueError:
        return jsonify({"error": "Invalid amount"}), 400

    if data["type"] == "expense":
        transaction = Transaction(
            user_id=user_id,
            type="expense",
            category=data.get("category", "General"),
            subcategory=data.get("subcategory"),
            title=data.get("title"),
            amount=amount,
            description=data.get("description"),
        )
    elif data["type"] == "income":
        if not data.get("source"):
            return jsonify({"error": "Source is required for income"}), 400
        
        transaction = Transaction(
            user_id=user_id,
            type="income",
            source=data["source"],
            amount=amount,
            description=data.get("description"),
        )
    else:
        return jsonify({"error": "Invalid transaction type"}), 400

    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({"message": "Transaction added successfully"}), 201


# ✅ Get transactions with filtering (by user)
@expense_routes.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    query = Transaction.query.filter_by(user_id=user_id)

    # Filtering by Type (income or expense)
    transaction_type = request.args.get('type')
    if transaction_type in ['income', 'expense']:
        query = query.filter(Transaction.type == transaction_type)

    # Filtering by Category (only for expenses)
    category = request.args.get('category')
    if category:
        query = query.filter(Transaction.category == category)

    # Filtering by Date Range
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Transaction.timestamp >= start_date)
        except ValueError:
            return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400

    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Transaction.timestamp <= end_date)
        except ValueError:
            return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400

    # Execute query
    transactions = query.order_by(Transaction.timestamp.desc()).all()

    result = [
        {
            "id": t.id,
            "type": t.type,
            "source": t.source if t.type == "income" else None,
            "category": t.category if t.type == "expense" else None,
            "subcategory": t.subcategory if t.type == "expense" else None,
            "title": t.title if t.type == "expense" else None,
            "amount": t.amount,
            "description": t.description,
            "timestamp": t.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for t in transactions
    ]

    return jsonify(result), 200


# ✅ Get categories and subcategories (for the logged-in user only)
@expense_routes.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    user_id = get_jwt_identity()  # Get logged-in user's ID

    # Query only transactions belonging to the logged-in user
    transactions = Transaction.query.filter_by(user_id=user_id).all()

    category_data = {}
    for transaction in transactions:
        if transaction.category:  # Only consider transactions with categories
            if transaction.category not in category_data:
                category_data[transaction.category] = set()  # Use set to avoid duplicates
            if transaction.subcategory:
                category_data[transaction.category].add(transaction.subcategory)

    # Convert sets to lists for JSON response
    category_data = {cat: list(subs) for cat, subs in category_data.items()}
    
    return jsonify(category_data)


# ✅ Create a new category or subcategory (for the logged-in user only)
@expense_routes.route('/categories/new', methods=['POST'])
@jwt_required()
def create_category():
    user_id = get_jwt_identity()  # Get logged-in user ID
    data = request.json

    category_name = data.get('category')
    subcategory_name = data.get('subcategory')

    if not category_name:
        return jsonify({"error": "Category name is required"}), 400

    # Check if the category exists for this user
    existing_transaction = Transaction.query.filter_by(user_id=user_id, category=category_name).first()

    if not existing_transaction:
        # If category does not exist, create it
        new_transaction = Transaction(
            user_id=user_id, category=category_name, subcategory=subcategory_name or None
        )
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify({"message": "New category created!"})

    # If category exists but subcategory is new, add the new subcategory
    if subcategory_name:
        subcategory_exists = Transaction.query.filter_by(
            user_id=user_id, category=category_name, subcategory=subcategory_name
        ).first()

        if not subcategory_exists:
            new_transaction = Transaction(
                user_id=user_id, category=category_name, subcategory=subcategory_name
            )
            db.session.add(new_transaction)
            db.session.commit()
            return jsonify({"message": "New subcategory added!"})

    return jsonify({"message": "Category and subcategory already exist for this user!"})


@expense_routes.route('/transactions/<int:id>', methods=['PUT'])
@jwt_required()
def update_transaction(id):
    user_id = get_jwt_identity()
    transaction = Transaction.query.filter_by(id=id, user_id=user_id).first_or_404()

    data = request.json

    # Update amount if provided and valid
    if 'amount' in data:
        try:
            transaction.amount = float(data['amount'])
        except ValueError:
            return jsonify({"error": "Invalid amount"}), 400

    # Update category if provided
    if 'category' in data and data['category']:
        transaction.category = data['category']

    # Update subcategory if provided
    if 'subcategory' in data:
        transaction.subcategory = data['subcategory']

    # Update title if provided
    if 'title' in data and data['title']:
        transaction.title = data['title']

    db.session.commit()

    return jsonify({
        "message": "Transaction updated successfully",
        "updated_transaction": {
            "id": transaction.id,
            "type": transaction.type,
            "category": transaction.category,
            "subcategory": transaction.subcategory,
            "title": transaction.title,
            "amount": transaction.amount,
            "description": transaction.description,
            "timestamp": transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
    }), 200


# Delete Transaction
@expense_routes.route('/transactions/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(id):
    user_id = get_jwt_identity()
    transaction = Transaction.query.filter_by(id=id, user_id=user_id).first_or_404()

    db.session.delete(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction deleted successfully"}), 200



# Delete Transaction
@expense_routes.route('/test', methods=['GET'])

def test():


    return jsonify({"message": "Transaction deleted successfully"}), 200
