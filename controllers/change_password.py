def is_strong_password(password):
    return (
        len(password) >= 8 and
        any(char.isupper() for char in password) and
        any(char.islower() for char in password) and
        any(char.isdigit() for char in password) and
        any(char in '!@#$%^&*()-=_+[]{}|;:,.<>?/~`' for char in password)
    )

def change_password(): 

    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    response.title='Change Password'
    c_id = str(session.cid).upper()
    user_id = str(session.user_id).upper()
      
    btn_change_password=request.vars.btn_change_password

    
    if btn_change_password:
        c_id=str(request.vars.c_id.strip()).upper()
        user_id=str(request.vars.user_id.strip()).upper()
        old_password=str(request.vars.old_pass).strip()
        new_password=str(request.vars.new_pass).strip()
        confirm_password=str(request.vars.confirm_pass).strip()

        if (c_id==''or user_id==''or old_password==''or new_password==''or confirm_password==''):
            response.flash = 'All fields must be required!'
        else:
            check_user_sql = f"SELECT id, password FROM admin_user WHERE cid = '{c_id}'  AND user_id = '{user_id}'  AND status = 'ACTIVE'  LIMIT 1;"
            check_user = db.executesql(check_user_sql, as_dict = True)

            if not check_user:
                response.flash= 'Invalid user!'
            else:
                user_password=check_user[0]['password'] 
                if user_password!=old_password:
                    response.flash = 'Old password is not correct!'
                else:
                    if new_password!=confirm_password:
                        response.flash = 'Required New password and Confirm password needs to be same!'
                    else:
                        if not is_strong_password(new_password):
                            response.flash = 'Password is not strong(length must be 8 character)!'
                        else:
                            if confirm_password==old_password:
                                response.flash = 'Required Old password and Confirm password Not same!'
                            else:
                                
                                update_sql = f"UPDATE admin_user SET password = '{new_password}' WHERE cid = '{c_id}' AND user_id = '{user_id}';"
                                update = db.executesql(update_sql)

                                session.flash= 'Password Changed Successfully!'
                                redirect(URL('default','index'))                        
                            
    return dict()