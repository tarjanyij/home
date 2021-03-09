from app.api import bp
from flask import jsonify
from sqlalchemy import func
from app.api.auth import token_auth
from app.models import Temperature

@bp.route('/sensortemperature', methods=['GET'])
@token_auth.login_required
def get_sensortemperature():
    #row = Temperature.query.filter_by(thermosensor_id="012033add00d").order_by(Temperature.date.desc()).first()
    #row = Temperature.query.filter().order_by(Temperature.date.desc()).limit(10).all()
    
    subquery = Temperature.query.filter().order_by(Temperature.date.desc()).first()
    row = Temperature.query.filter(Temperature.date == subquery.date)
        
    return jsonify(Temperature.to_collection_dict(row))