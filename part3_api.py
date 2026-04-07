from datetime import datetime, timedelta
from sqlalchemy import func

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def get_low_stock_alerts(company_id):
    days_lookback = 30
    cutoff_date = datetime.utcnow() - timedelta(days=days_lookback)

    # 1. Calculate sales velocity
    sales_velocity = db.session.query(
        InventoryChange.inventory_id,
        func.sum(InventoryChange.quantity_diff).label('total_sold')
    ).filter(
        InventoryChange.change_type == 'sale',
        InventoryChange.created_at >= cutoff_date
    ).group_by(InventoryChange.inventory_id).subquery()

    # 2. Join with Inventory to find low stock
    alerts = db.session.query(
        Product.name, Inventory.quantity, ProductType.low_stock_threshold
    ).join(Product).join(ProductType).join(sales_velocity).filter(
        Inventory.quantity < ProductType.low_stock_threshold
    ).all()

    return jsonify([{"name": a.name, "stock": a.quantity} for a in alerts])
