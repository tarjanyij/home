from flask import Blueprint, render_template, redirect,url_for, request, make_response
from flask_sqlalchemy import BaseQuery
from flask_login import login_required, current_user
from cpuinfo import get_cpu_info

from app.models import Temperature, User, SensorConfig
from app import db


main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    if current_user.is_authenticated:
        return render_template('index.html',name=current_user.name)
    else:
        return render_template('index.html')


@main.route('/sensortemp')
@login_required
def sensortemp():
    #rows = Temperature.query.filter(thermosensor_id="012033add00d").all()
    #rows = Temperature.query.filter(Temperature.date.like('2020-12-16%')).all()
    #rows = Temperature.query.filter_by(thermosensor_id="012033add00d").order_by(Temperature.date.desc()).first()
    #rows = []
    subquery = Temperature.query.filter().order_by(Temperature.date.desc()).first()
    #rows = Temperature.query.filter(Temperature.date == subquery.date)
    rows = Temperature.query\
            .outerjoin(SensorConfig, Temperature.thermosensor_id == SensorConfig.sensorid)\
            .filter(Temperature.date == subquery.date)\
            .order_by(SensorConfig.display_order)
    
    return render_template('sensortemp.html', name=current_user.name,rows = rows)
    
@main.route('/sensortempdata', methods=['POST'])
@login_required
def sensorTempData():
    sensorId = request.form.get('sensorid')
       
    rows =Temperature.query\
            .filter(Temperature.thermosensor_id == sensorId)\
            .order_by(Temperature.date)

    data="Date,Temperature\n"
    for items in rows:
        data= data+ str(items.date)+","+ str(items.temperature) +"\n"

    response = make_response(data, 200)
    response.mimetype = "text/plain"
    return response

@main.route('/environment')
@login_required
def environment():
    info = get_cpu_info()
    return render_template('environment.html',name=current_user.name, info = info)

@main.route('/sensorconfig')
@login_required
def sensor_config():
    #sensorids = db.session.query(Temperature.thermosensor_id).distinct()
    sensorConfigs = SensorConfig.query.all()
    return render_template('sensorconfig.html',name=current_user.name, sensorConfigs =sensorConfigs)

@main.route('/sensorconfig', methods=['POST'])
@login_required
def sensor_config_set():
    x = request.form
    y = int(len(x)/5+1)
    
    for i in range (1,y):
        #print(f"name érték : {x['name'+str(i)]}")
        update_row = SensorConfig.query.filter_by(sensorid = x['sensorid'+str(i)]).first()
        #print (update_row)
        update_row.sensorname = x['name'+str(i)]
        update_row.display_order = x['display_order'+str(i)]
        update_row.tick = x['tick'+str(i)]
        update_row.highervalue = x['highervalue'+str(i)]
        db.session.commit()
        
    return redirect(url_for('main.sensortemp'))

