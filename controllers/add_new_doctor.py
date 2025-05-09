def add_new_doctor():
    cid = session.cid
    # return cid
    submit = request.vars.submit
    btn_filter = request.vars.btn_filter
    btn_all = request.vars.btn_all
    condition = ''
    reqPage = len(request.args)
    
    if submit:
        doctor_id = request.vars.doctor_id
        doctor_name = request.vars.doctor_name
        mobile_no = request.vars.mobile_no
        password = request.vars.password
        address = request.vars.address
        email_address = request.vars.email_address
        status_type = request.vars.status_type
        

        if doctor_id =='' or doctor_id =='None':
            response.flash = ' Required id'
        elif doctor_name =='' or doctor_name =='None':
            response.flash = 'Requaired Name'
        elif mobile_no =='' or mobile_no =='None':
             response.flash = 'Required mobile no'
        elif password =='' or password =='None':
             
             response.flash = 'Required password'
   
        else:
            check_doctor_sql = f"SELECT * FROM sm_doctor where cid = '{cid}' and doctor_id = '{doctor_id}';"
            # return check_doctor_sql
            check_doctor = db.executesql(check_doctor_sql, as_dict=True)
            
            
            
            if len(check_doctor) > 0:
                response.flash = 'Already Exists!!'
            else:
                if len(mobile_no) == 11 or len(mobile_no) == 13:
                    response.flash = "Invalid Mobile Number "

                if not email_address or '@' not in email_address:
                    response.flash = "Invalid email "


                else:
                    check_doctor_sql = "INSERT INTO sm_doctor (cid,doctor_id,doctor_name,password,mobile_no,address,email_address,status_type) VALUES ('"+str(cid)+"','"+str(doctor_id)+"','"+str(doctor_name)+"','"+str(password)+"','"+str(mobile_no)+"','"+str(address)+"','"+str(email_address)+"','"+str(status_type)+"');"
                    db.executesql(check_doctor_sql)
                    response.flash= 'Successfully saved!'

    # items per page ----------------------------------------------------------           
    session.items_per_page = 20
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    if(page==0):
        limitby = (page * items_per_page, (page + 1) * items_per_page)
    else:
        limitby = ((page* items_per_page), items_per_page)
    # ---------------------------------------------------------------------------

    if btn_filter == 'Filter':
        doctor_id_filter = request.vars.doctor_id_filter
        # return doctor_id_filter
        if doctor_id_filter !='':
            session.doctor_id_filter = doctor_id_filter
            try:
                doctor_id_filter = str(doctor_id_filter).split('|')[0]
            except:
                session.doctor_id_filter = ''
            condition = condition + " and doctor_id = '"+str(doctor_id_filter)+"'"

        # return session.doctor_id_filter
        reqPage=0
        session.condition = condition

    if btn_all == "All":
        condition = ''
        session.doctor_id_filter = ''
        session.condition = condition
        reqPage=0

    condition=session.condition
    if condition==None or condition=='None':
        condition=''
    itemRows_sql = "select * from sm_doctor where cid = '"+str(cid)+"'  "+condition+" ORDER BY id DESC limit %d, %d;" % limitby
    # return itemRows_sql
    itemRows = db.executesql(itemRows_sql, as_dict=True)
    session.condition = condition

    total_record_sql = f"SELECT COUNT(id) AS total FROM sm_doctor WHERE cid='APPOINTMENT' {condition} ORDER BY id ASC;"
    total_record = db.executesql(total_record_sql, as_dict = True)
    total_rec = total_record[0]['total']

    return dict(itemRows=itemRows,page=page,items_per_page=items_per_page,total_rec=total_rec)

def get_doctor_id_list():
    response.view = 'generic.html'
    response.headers['Content-Type'] = 'text/plain'

    if not session.cid:
        redirect(URL('default', 'index'))
    
    cid = session.cid
    rows = db.executesql(
        "SELECT doctor_id, doctor_name FROM sm_doctor WHERE cid = '{}' GROUP BY doctor_id".format(cid),
        as_dict=True
    )
    
    return ','.join(['{}|{}'.format(r['doctor_id'], r['doctor_name']) for r in rows])

# ---------------------------------------------------------------------------------------------------------

def doctor_edit():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id=session.cid
    doctor_id =request.args(0)
    
    update_btn = request.vars.update_btn
    delete_btn = request.vars.delete_btn

    select_item_record_sql = f"SELECT * FROM sm_doctor WHERE cid = '"+str(c_id)+"' AND doctor_id ='"+str(doctor_id)+"' GROUP BY doctor_id LIMIT 1;"
    # return select_item_record_sql
    selected_item_record = db.executesql(select_item_record_sql, as_dict = True)
    # return 11

    # if len(selected_ret_record) != 0 :
    for i in range(len(selected_item_record)):
        item = selected_item_record[i]
        rowId = str(item["id"])
        doctor_id = str(item["doctor_id"])
        doctor_name = str(item["doctor_name"])
        mobile_no = str(item["mobile_no"])
        password = str(item["password"])
        address = str(item["address"])
        email_address = str(item["email_address"])
        status_type = str(item["status_type"])
       
        
        # return status
    
    if update_btn:
        doctor_name_up = str(request.vars.doctor_name)
        mobile_no_up = str(request.vars.mobile_no)
        password_up = str(request.vars.password)
        address_up = str(request.vars.address)
        email_address_up = str(request.vars.email_address)
        status_type_up = str(request.vars.status_type)
        # return  price_up 

        update_sql = f"UPDATE sm_doctor SET doctor_name = '"+str(doctor_name_up)+"',  mobile_no = '"+str(mobile_no_up)+"', password = '"+str(password_up)+"', address = '"+str(address_up)+"', email_address = '"+str(email_address_up)+"',status_type = '"+str(status_type_up)+"'  WHERE cid = '"+str(c_id)+"' AND doctor_id = '"+str(doctor_id)+"' LIMIT 1;"
        # return update_sql
        up_date = db.executesql(update_sql)

        session.flash = 'Update Successfully!'

        redirect(URL('add_new_doctor','add_new_doctor'))

    if delete_btn:
        delete_sql = f"DELETE FROM sm_doctor WHERE cid = '"+str(c_id)+"' AND doctor_id='"+str(doctor_id)+"' LIMIT 1;"
        delete = db.executesql(delete_sql)

        session.flash = 'Deleted Successfully!'

        redirect(URL('add_new_doctor','add_new_doctor'))
            
    return dict(doctor_id=doctor_id,doctor_name=doctor_name,mobile_no=mobile_no,password=password,address=address,email_address=email_address,status_type=status_type)
