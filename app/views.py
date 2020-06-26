from facebook import get_user_from_cookie, GraphAPI 
from flask import g, render_template, redirect, request, session, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import User, Disqualified, SurveyURL 
from app.forms import ConsentForm, Form2, Form3, InterestForm, AdminLogin, SurveyForm
from app.user_sorter import User_Sorter
from app.loc_worker import Location_Worker
import random
import urllib
import requests
import hashlib
from flask_babel import _
from flask_babel import lazy_gettext as _l
import flask_excel as excel
excel.init_excel(app)


# Facebook app details
FB_APP_ID = "427701117974000"
FB_APP_NAME = "DI Survey"
FB_APP_SECRET = "80d863179628eaaa7d3c46cf41a8d4ff"

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = ConsentForm()
    if form.validate_on_submit():
        if not 18 <= int(form.age.data) <= 35:
            return redirect(url_for('disqualified'))
        if request.args.get('utm_source'):
            session['utm_source'] = request.args.get('utm_source')
        else:
            session['utm_source'] = 'Not a facebook ad'
        session['age'] = form.age.data
        session['gender'] = form.gender.data
        return redirect(url_for('login'))
    return render_template('index.html', form=form)    

@app.route('/disqualified', methods=['GET', 'POST'])
def disqualified():
    form = InterestForm()
    if form.validate_on_submit():
        disqualified = Disqualified(
            name = form.name.data,
            email = form.email.data,
            phone = form.phone.data
        )
        db.session.add(disqualified)
        db.session.commit
        return redirect(url_for('index'))
    return render_template('disqualified.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        #First we're just going to see if people are already logged in to this system. If they are, redirect to their appropriate survey page based on group.
        return redirect(url_for('survey'+str(int(current_user.gender))))
    #Next we need to see whether they have a facebook login cookie.        
    result = get_user_from_cookie(cookies=request.cookies, app_id=FB_APP_ID, app_secret=FB_APP_SECRET)
    if result:
        g.result = result
    else:
    #If they don't have a facebook login cookie, redirect to the facebook login page, which will then redirect back to login_successful for further processing
        graph = GraphAPI(version='3.1')
        return redirect(graph.get_auth_url(FB_APP_ID, url_for('login_successful', _external=True),['email'])+'&response_type=code')

@app.route('/login_successful', methods=['GET', 'POST'])
def login_successful():
    #First we're just going to check again to see if people are already logged in to this system. If they are, redirect to their appropriate survey page based on group.
    if current_user.is_authenticated:
        session['uid'] = current_user.id
        return redirect(url_for('survey'+str(current_user.group)))
    else:
        #Check to see if we are coming from a facebook login page
        if request.args.get('code'):
            code = request.args.get('code')
            result = requests.get('https://graph.facebook.com/v3.1/oauth/access_token?client_id='+FB_APP_ID+'&redirect_uri='+url_for('login_successful', _external=True)+'&client_secret='+FB_APP_SECRET+'&code='+code+'&scope=email')
            g.result = result.json()
        # If we get a permissions error then we'll create a dummy result with uid that's generated internally so we can continue with the survey rather than lose the data
        elif request.args.get('error_code') == '200':
            lastunapproveduser = User.query.filter(User.id.like('777%')).order_by(User.id.desc()).first()
            if not lastunapproveduser:
                uid = int(77700000000)
            else:
                uid = int(lastunapproveduser.id)
            g.result = {
                'access_token': 'fizzlebip',
                'uid': str(uid+1)
            }
    if 'access_token' in g.result.keys():
        if g.result['access_token'] != 'fizzlebip':
            graph = GraphAPI(g.result['access_token'])
    if 'uid' not in g.result.keys():
        profile = graph.get_object("me",fields='email, id, first_name, last_name, short_name, name')
        user = User.query.filter(User.id == profile['id']).first()
    #If we got a no app permission error create a dummy profile using an id that starts in 777
    elif g.result['access_token'] == 'fizzlebip':
        profile = {
            'id': g.result['uid'],
            'name': 'no app permissions',
            'email': 'no app permissions',
            'short_name': 'no app permissions'
        }
        user = User.query.filter(User.id == g.result['uid']).first()
    else:
        user = User.query.filter(User.id == g.result['uid']).first()
    if not user:
        # Not an existing user so get info
        if 'email' not in profile.keys():
            if 'email' not in g.result.keys():
                profile['email'] = 'none available'
            else:
                profile['email'] = g.result['email']
        # Create the user and insert it into the database
        user = User(
            id=profile['id'],
            name=profile['name'],
            access_token=g.result['access_token'],
            gender=bool(int(session['gender'])),
            coastal=True,
            ed=True,
            reg=True,
            phone='3019611660',
            loc='Tunis',
            block=4,
            group=4,
            email=profile['email'],
            hashedid= hashlib.md5(str(profile['id'])).hexdigest(),
            age=session['age'],
            facebookname=profile['short_name'],
            utm_source = session['utm_source']
            )
        db.session.add(user)
    elif user.access_token != g.result["access_token"]:
        # If an existing user, update the access token
        user.access_token = g.result["access_token"]
    login_user(user)
    session['uid'] = hashlib.md5(str(user.id)).hexdigest()
    return redirect(url_for('survey' + str(int(user.gender))))

@app.route('/survey0', methods=['GET', 'POST'])
@login_required
#Treatment 1
def survey0():
    return redirect('https://www.surveymonkey.com/r/BTSXG9Y?uid='+str(session.get('uid', 'none')))
                
@app.route('/survey1', methods=['GET', 'POST'])
@login_required
#Treatment 2
def survey1():
    return redirect('https://www.surveymonkey.com/r/BRC9HHR?uid='+str(session.get('uid', 'none')))

@app.route('/admin')
def admin():
     
    user = ''
    users = User.query.all()
    m = list([True, False])
    res = [(i, j, k, l) for i in m for j in m for k in m for l in m]
    i = 0
    j = 0
    rows = range(16)
    totalcount0 = 0
    totalcount1 = 0
    totalcount2 = 0
    totalcount3 = 0
    totalcount4 = 0

    #First create the rows list based on the possible permutations of our four blocking elements (gender, ed, coastal, reg). Then include a count for each list element of the number of users sorted into each of the five random groups for each permutation, or block.
    for i in range(16):
        for j in range(4):
            if j == 0:
                gender = res[i][j]
            elif j == 1:
                ed = res[i][j]
            elif j == 2:
                coastal = res[i][j]
            elif j == 3:
                reg = res[i][j]
        rows[i] = {
            'number': i+1,
            'gender': gender,
            'ed': ed,
            'coastal': coastal,
            'reg': reg,
            'count0': User.query.filter_by(gender=gender, ed=ed, coastal=coastal, reg=reg, group=0).count(),
            'count1': User.query.filter_by(gender=gender, ed=ed, coastal=coastal, reg=reg, group=1).count(),
            'count2': User.query.filter_by(gender=gender, ed=ed, coastal=coastal, reg=reg, group=2).count(),
            'count3': User.query.filter_by(gender=gender, ed=ed, coastal=coastal, reg=reg, group=3).count(),
            'count4': User.query.filter_by(gender=gender, ed=ed, coastal=coastal, reg=reg, group=4).count()
        }

        #Then get a count of the number of users in each of the five groups, and the overall total number of users.
        totalcount0 = totalcount0 + rows[i]['count0']
        totalcount1 = totalcount1 + rows[i]['count1']
        totalcount2 = totalcount2 + rows[i]['count2']
        totalcount3 = totalcount3 + rows[i]['count3']
        totalcount4 = totalcount4 + rows[i]['count4']
        totalusercount = totalcount0 + totalcount1 + totalcount2 + totalcount3 + totalcount4
        gender = ''
        ed = ''
        coastal = ''
        reg =''

    #Next, check and see if there was a form submission, and if so, save the results.

    form = SurveyForm()
    if form.validate_on_submit():
        surveyurls = [ ]
        for entry in form.entries:
            print entry
            surveyurl = SurveyURL.query.filter(SurveyURL.id == entry.id.data).first()
            if not surveyurl:
                print 'foo'
                surveyurl = SurveyURL(
                    id = entry.id.data,
                    lang = entry.lang.data,
                    treatmento = entry.treatmentno.data,
                    url = entry.url.data,
                    updatedby = entry.updatedby.data
                )
                db.session.add(surveyurl)
                db.session.commit()
                surveyurls.append(surveyurl)
        form.populate_obj(surveyurl)
        return redirect(url_for('admin'), rows=rows, users=users, totalcount0=totalcount0, totalcount1=totalcount1, totalcount2=totalcount2, totalcount3=totalcount3, totalcount4=totalcount4, totalusercount=totalusercount, form=form)

    return render_template('admin.html', rows=rows, users=users, totalcount0=totalcount0, totalcount1=totalcount1, totalcount2=totalcount2, totalcount3=totalcount3, totalcount4=totalcount4, totalusercount=totalusercount, form=form)

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/seleniumtest')
def seleniumtest():
    return render_template('seleniumtest.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLogin()
    if form.validate_on_submit():
        if form.pw.data == 'E66%K7Dzp$hk':
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('index'))
    return render_template('admin_login.html', form=form)

@app.route('/export', methods=['GET'])
def doexport():
#    for user in User.query.all():
#        if user.hashedid is None:
#            user.hashedid = hashlib.md5(str(user.id)).hexdigest()
#    db.session.commit()
    return excel.make_response_from_tables(db.session, [User, Disqualified], 'xls')
