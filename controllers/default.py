
import urllib.parse
from gluon.tools import fetch


def index(): 
    session.clear()
    return dict()



def check_user():
    cid = str(request.vars.cid).strip().upper()
    uid = str(request.vars.uid).strip().upper()
    password = str(request.vars.password).strip()

    if (cid == '' or uid == '' or password == ''):
        session.flash = 'User ID and Password required !'
        redirect(URL('index'))

       
    user_sql = f"""
        SELECT * FROM admin_user 
        WHERE cid = '{cid}' 
        AND user_id = '{uid}' 
        AND password = '{password}' 
        AND status = 'ACTIVE' 
        LIMIT 1
    """
    userRows = db.executesql(user_sql, as_dict=True)

    if not userRows:
        session.flash = 'Unauthorized User'
        redirect(URL('index'))
    else:
        cid = cid
        user_id = uid
        user_type = userRows[0]['user_type']
        user_name = userRows[0]['name']
        status = userRows[0]['status']

        

        session.cid = cid
        session.user_id = user_id
        session.user_type = user_type

        redirect(URL('home'))
    return dict()




def home():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    response.title="Appointment Portal"
    return dict()

def logout():
    session.clear()
    return redirect (URL('default','index'))