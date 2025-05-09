def schedule_appointment():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))

    response.title='Schedule Appointment'
    submit=request.vars.submit
    btn_filter_appointment=request.vars.btn_filter_appointment
    appointment_id_filter = request.vars.appointment_id_filter
    btn_filter_item=request.vars.btn_filter_item
    btn_all=request.vars.btn_all
    c_id=session.cid
    condition = ''
    reqPage = len(request.args)

    session.item_id_filter = ''
    session.condition = ''

    if submit:
      
            appointment_id = str(request.vars.appointment_id)
            reason = str(request.vars.reason)
            status_type = str(request.vars.status_type)
            # return appointment_id
                
            try:
                
                doctor_id = str(request.vars.doctor_id_filter1).split('|')[0]
                doctor_name = str(request.vars.doctor_id_filter1).split('|')[1]
                patient_id = str(request.vars.patient_id_filter1).split('|')[0]
                patient_name = str(request.vars.patient_id_filter1).split('|')[1]
                
            except:
                doctor_id = ''
                doctor_name = ''
                patient_id = ''
                patient_name = ''

                
            # return doctor_id
            # return doctor_id
            # return patient_id
            
            
            if appointment_id=='' or appointment_id==None or appointment_id=='None':
                response.flash = 'Required Appointment ID'
            else:
                
                check_sql = "SELECT * FROM sm_appointment WHERE cid='"+str(c_id)+"' AND appointment_id= '"+str(appointment_id)+"';"
                check_appointment = db.executesql(check_sql, as_dict=True)
                
                if len(check_appointment)> 0:
                    response.flash = 'Appointment already exists !'
            
                else:
                    insert_sql = "INSERT INTO sm_appointment (cid,appointment_id,doctor_id,doctor_name,patient_id,patient_name,reason,status_type) VALUES ('"+str(c_id)+"','"+str(appointment_id)+"','"+str(doctor_id)+"','"+str(doctor_name)+"','"+str(patient_id)+"','"+str(patient_name)+"','"+str(reason)+"','"+str(status_type)+"');"      
                    insertappointment = db.executesql(insert_sql)
                    response.flash= 'Successfully saved!'
                            
                                
            

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
    # --------end paging 
    
    
    if btn_filter_item == "Filter":
        appointment_id_filter1 = request.vars.appointment_id_filter1
        doctor_id_filter2 = request.vars.doctor_id_filter2
        patient_id_filter2 = request.vars.patient_id_filter2
        # patient_id_filter1 = request.vars.patient_id_filter1
        
        condition = ''

        if appointment_id_filter1 !='':
            session.appointment_id_filter1 = appointment_id_filter1
            try:
                appointment_id_filter1 = str(appointment_id_filter1).split('|')[0]
            except:
                session.appointment_id_filter1 = ''
            condition = condition + " and appointment_id = '"+str(appointment_id_filter1)+"'"

        if doctor_id_filter2 !='':
            session.doctor_id_filter2 = doctor_id_filter2
            try:
                doctor_id_filter2 = str(doctor_id_filter2).split('|')[0]
            except:
                session.doctor_id_filter2 = ''
            condition = condition + " AND doctor_id = '" + str(doctor_id_filter2) + "'" 

        if patient_id_filter2 !='':
            session.patient_id_filter2 = patient_id_filter2
            try:
                patient_id_filter2 = str(patient_id_filter2).split('|')[0]
            except:
                session.patient_id_filter2 = ''
            condition = condition + " AND patient_id = '" + str(patient_id_filter2) + "'"

           
        reqPage=0
        session.condition = condition

    if btn_all == "All":
        condition = ''
        session.appointment_id_filter1 = ''
        session.doctor_id_filter2 = ''
        # session.patient_id_filter2 = ''
        session.patient_id_filter2 = ''
        session.condition = condition
        reqPage=0
    
    
    condition=session.condition
    if condition==None or condition=='None':
        condition=''
    appointmentRows_sql = "select * from sm_appointment where cid = '"+str(c_id)+"'  "+condition+" ORDER BY id DESC limit %d, %d;" % limitby
    # return appointmentRows_sql
    appointmentRows = db.executesql(appointmentRows_sql, as_dict=True)
    session.condition = condition
    # return 22

    total_record_sql = f"SELECT COUNT(id) AS total FROM sm_appointment WHERE cid='APPOINTMENT' {condition} ORDER BY id ASC;"
    total_record = db.executesql(total_record_sql, as_dict = True)
    total_rec = total_record[0]['total']

    return dict(appointmentRows=appointmentRows,page=page,items_per_page=items_per_page,total_rec=total_rec)

# *******************************************************************************************

def get_doctor_id_list():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid
    reqStr = ''

    itemlistRows_sql = "select doctor_id,doctor_name from sm_doctor where cid = '"+c_id+"';"
    itemlistRows = db.executesql(itemlistRows_sql, as_dict=True)

    for i in range(len(itemlistRows)):
        item_list_dict=itemlistRows[i]   
        doctor_id=str(item_list_dict["doctor_id"])
        doctor_name=str(item_list_dict["doctor_name"])   
        if reqStr == '':
            reqStr = doctor_id+'|'+doctor_name
        else:
            reqStr += ',' + doctor_id+'|'+doctor_name
    
    return reqStr

def get_patient_id_list():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid
    retStr = ''

    itemlistRows_sql1 = "select patient_id,patient_name from sm_patient where cid = '"+c_id+"';"
    itemlistRows1 = db.executesql(itemlistRows_sql1, as_dict=True)

    for i in range(len(itemlistRows1)):
        item_list_dict1=itemlistRows1[i]   
        patient_id=str(item_list_dict1["patient_id"])
        patient_name=str(item_list_dict1["patient_name"])   
        if retStr == '':
            retStr = patient_id+'|'+patient_name
        else:
            retStr += ',' + patient_id+'|'+patient_name
    
    return retStr


def get_appointment_id_list():
    if session.cid == '' or session.cid is None:
        redirect(URL('default', 'index'))

    c_id = session.cid
    regStr = ''

    itemlistRows_sql3 = "select appointment_id from sm_appointment where cid = '" + c_id + "';"
    itemlistRows3 = db.executesql(itemlistRows_sql3, as_dict=True)

    for item in itemlistRows3:
        appointment_id = str(item["appointment_id"])
        regStr += ',' + appointment_id if regStr else appointment_id

    response.headers['Content-Type'] = 'text/plain'
    return regStr


# ***************************************************************************************************************


def appointment_Download():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid
    condition = ''
    condition = session.condition
    if condition==None or condition=='None':
        condition=''

    download_sql = "select * from sm_appointment where cid = '"+c_id+"' "+condition+";"
    download_records = db.executesql(download_sql, as_dict=True)
    
    myString = 'Schedule Appointment Download \n\n'
    myString += 'appointment_id,doctor_id,doctor_name,patient_id,patient_name,reason,status_type\n'
    total=0 
    attTime = ''
    totalCount = 0
    for i in range(len( download_records)):
        recordsStr =  download_records[i]
        appointment_id=str(recordsStr["appointment_id"])
        doctor_id=str(recordsStr["doctor_id"])
        doctor_name=str(recordsStr["doctor_name"])
        patient_id=str(recordsStr["patient_id"])
        patient_name=str(recordsStr["patient_name"])
        reason=str(recordsStr["reason"])
        status_type=str(recordsStr["status_type"])
        

        myString += str(appointment_id) + ',' + str(doctor_id) + ',' + str(doctor_name) + ',' + str(patient_id) + ',' + str(patient_name) + ','+ str(reason) + ',' + str(status_type) + '\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_Appointment.csv'
    return str(myString)    

# *************************************************************************

def appointment_edit():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id=session.cid
    appointment_id =request.args(0)
    
    update_btn = request.vars.update_btn
    delete_btn = request.vars.delete_btn

    select_item_record_sql = f"SELECT * FROM sm_appointment WHERE cid = '"+str(c_id)+"' AND appointment_id ='"+str(appointment_id)+"' GROUP BY appointment_id LIMIT 1;"
    # return select_item_record_sql
    selected_item_record = db.executesql(select_item_record_sql, as_dict = True)
    # return 11

    # if len(selected_ret_record) != 0 :
    for i in range(len(selected_item_record)):
        item = selected_item_record[i]
        rowId = str(item["id"])
        appointment_id = str(item["appointment_id"])
        doctor_id = str(item["doctor_id"])
        doctor_name = str(item["doctor_name"])
        patient_id = str(item["patient_id"])
        patient_name = str(item["patient_name"])
        reason = str(item["reason"])
        status_type = str(item["status_type"])
        
        
        # return status
    
    if update_btn:
        
        reason_up = str(request.vars.reason)
        status_type_up = str(request.vars.status_type)
        try:

            doctor_id_up = str(request.vars.doctor_id_filter3).split('|')[0]
            doctor_name_up = str(request.vars.doctor_id_filter3).split('|')[1]
            patient_id_up = str(request.vars.patient_id_filter3).split('|')[0]
            patient_name_up = str(request.vars.patient_id_filter3).split('|')[1]

        except:
            doctor_id_up=''
            doctor_name_up=''
            patient_id_up=''
            patient_name_up=''    

        update_sql = f"UPDATE sm_appointment SET doctor_id = '"+str(doctor_id_up)+"', doctor_name = '"+str(doctor_name_up)+"',  patient_id = '"+str(patient_id_up)+"', patient_name = '"+str(patient_name_up)+"', reason = '"+str(reason_up)+"', status_type = '"+str(status_type_up)+"'  WHERE cid = '"+str(c_id)+"' AND appointment_id = '"+str(appointment_id)+"' LIMIT 1;"
        # return update_sql
        up_date = db.executesql(update_sql)
        session.flash = 'Updated Successfully!'

        redirect(URL('schedule_appointment','schedule_appointment'))

    if delete_btn:
        delete_sql = f"DELETE FROM sm_appointment WHERE cid = '"+str(c_id)+"' AND appointment_id='"+str(appointment_id)+"' LIMIT 1;"
        delete = db.executesql(delete_sql)
        session.flash = 'Deleted Successfully!'

        redirect(URL('schedule_appointment','schedule_appointment'))
            
    return dict(appointment_id=appointment_id,doctor_id=doctor_id,doctor_name=doctor_name,patient_id=patient_id,patient_name=patient_name, reason=reason,status_type=status_type)
    



