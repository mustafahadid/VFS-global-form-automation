
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from unittest import result
import sqlite3
import pandas as pd
import time
from requests import options
from selenium.webdriver.common.by import By
import undetected_chromedriver.v2 as uc
import threading
import multiprocessing
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# database connection
conn = sqlite3.connect("db.db")
# create cursor
cur = conn.cursor()


def clean_input():
    ent_id.delete(0, END)
    ent_email.delete(0, END)
    ent_pass.delete(0, END)
    ent_visa_type.delete(0, END)
    ent_visa_center.delete(0, END)
    ent_visa_cath.delete(0, END)
    ent_first_name.delete(0, END)
    ent_last_name.delete(0, END)
    ent_birth_date.delete(0, END)
    ent_passport_no.delete(0, END)
    ent_passport_exp.delete(0, END)
    ent_sex.delete(0, END)
    ent_country.delete(0, END)
    ent_country_code.delete(0, END)
    ent_new_email.delete(0, END)
    ent_phone_no.delete(0, END)


def update(rows):
    trv.delete(*trv.get_children())
    for i in rows:
        trv.insert('', 'end', values=i)


def search():
    q = txt_search.get()
    query = "SELECT * FROM customers WHERE first_name LIKE'%"+q + \
        "%' OR last_name LIKE '%"+q+"%' OR passport_no LIKE '%"+q+"%'"
    cur.execute(query)
    conn.commit()
    rows = cur.fetchall()
    update(rows)


def clear():
    ent_search.delete(0, END)
    query = "SELECT * FROM customers"
    cur.execute(query)
    conn.commit()
    rows = cur.fetchall()
    update(rows)


def switch():
    if btn_ato["state"] == DISABLED:
        btn_ato["state"] = NORMAL
    else:
        btn_ato["state"] = DISABLED


def getrow(event):
    rowid = trv.identify_row(event.y)
    item = trv.item(trv.focus())
    cid.set(item['values'][0])
    email_vfs.set(item['values'][1])
    password.set(item['values'][2])
    visa_center.set(item['values'][3])
    visa_type.set(item['values'][4])
    visa_cath.set(item['values'][5])
    first_name.set(item['values'][6])
    last_name.set(item['values'][7])
    sex.set(item['values'][8])

    birth_date.set(str(item['values'][9]).zfill(8))
    nationality.set(item['values'][10])
    passport_no.set(item['values'][11])
    passport_exp.set(str(item['values'][12]).zfill(8))

    country_code.set(item['values'][13])
    phone_no.set(str(item['values'][14]))

    new_email.set(item['values'][15])
    # append to dict
    switch()
    dict_data = {'Email': [item['values'][1]], 'Pass': [item['values'][2]], 'Visa_center': [item['values'][3]], 'Visa_type': [item['values'][4]], 'Visa_cathegory': [item['values'][5]], 'First_name': [item['values'][6]], 'Last_name': [item['values'][7]], 'Sex': [
        item['values'][8]], 'Birth_date': [str(item['values'][9]).zfill(8)], 'Nationality': [item['values'][10]], 'Passport_no': [item['values'][11]], 'Passport_expire': [str(item['values'][12]).zfill(8)], 'Country_code': [item['values'][13]], 'Phone_no': [item['values'][14]], 'New_email': [item['values'][15]]}
    global result
    result = pd.DataFrame.from_dict(dict_data)
    pd.set_option('display.max_colwidth', None)


def add_new():
    e_mail = email_vfs.get()
    p_ssword = password.get()
    v_center = visa_center.get()
    v_type = visa_type.get()
    v_cath = visa_cath.get()
    f_name = first_name.get()
    l_name = last_name.get()
    p_no = passport_no.get()

    p_exp = str(passport_exp.get())
    p_phone = str(phone_no.get())
    c_code = country_code.get()
    b_date = str(birth_date.get())
    gender = sex.get()
    nation = nationality.get()
    n_email = new_email.get()

    query = "INSERT INTO customers(email, pass, visa_center, visa_type, visa_cathegory, first_name, last_name, sex, birth_data, nationality, passport_no, passport_expire, country_code, phone_no, new_email)VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cur.execute(query, (e_mail, p_ssword, v_center, v_type, v_cath, f_name,
                l_name, gender, b_date, nation, p_no, p_exp, c_code, p_phone, n_email))
    conn.commit()
    clear()
    clean_input()


def update_customer():
    c_id = cid.get()
    e_mail = email_vfs.get()
    p_ssword = password.get()
    v_center = visa_center.get()
    v_type = visa_type.get()
    v_cath = visa_cath.get()
    f_name = first_name.get()
    l_name = last_name.get()
    p_no = passport_no.get()

    p_exp = str(passport_exp.get())
    p_phone = str(phone_no.get())
    c_code = country_code.get()
    b_date = str(birth_date.get())
    gender = sex.get()
    nation = nationality.get()
    n_email = new_email.get()
    if messagebox.askyesno("Confirm Please", "Are you sure want to update this record"):
        query = "UPDATE customers SET email = ?, pass= ?, visa_center= ?, visa_type= ?, visa_cathegory= ?, first_name= ?, last_name= ?, sex= ?, birth_data= ?, nationality= ?, passport_no= ?, passport_expire= ?, country_code= ?, phone_no= ?, new_email= ? WHERE cid= ?"
        cur.execute(query, (e_mail, p_ssword, v_center, v_type, v_cath, f_name,
                            l_name, gender, b_date, nation, p_no, p_exp, c_code, p_phone, n_email, c_id))
        conn.commit()
        clear()
        clean_input()
    else:
        return True


def delete_customer():

    id = cid.get()
    if messagebox.askyesno("Confirm Delete", "Are your sure want to delete record?"):

        query = "DELETE FROM customers WHERE cid="+id
        cur.execute(query)
        conn.commit()
        clear()
        clean_input()
    else:
        return True

############################## AUTOMATE SECTION #######################################


def automate():
    print('starting.....')
    switch()

    try:
        browser = uc.Chrome()
        browser.get('https://visa.vfsglobal.com/tur/tr/pol/login')
        browser.maximize_window()
        # vfs login
        time.sleep(7)

        email = browser.find_element(By.XPATH, '//*[@id="mat-input-0"]')
        email.send_keys(str(result['Email'].to_string(index=False)))

        password = browser.find_element(By.XPATH, '//*[@id="mat-input-1"]')
        password.send_keys(str(result['Pass'].to_string(index=False)))

        login = browser.find_element(
            By.XPATH, "//span[contains(text(),'Oturum Aç')]")
        browser.execute_script(
            "arguments[0].scrollIntoView();", login)
        browser.execute_script("arguments[0].click();", login)

        # dashboard page
        time.sleep(7)
        # selecting accept all cookies button
        btn_hundler = browser.find_element(
            By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
        browser.execute_script(
            "arguments[0].scrollIntoView();", btn_hundler)
        browser.execute_script(
            "arguments[0].click();", btn_hundler)

        reserve_button = browser.find_element(
            By.XPATH, "/html/body/app-root/div/app-dashboard/section/div/div[2]/button/span[1]")
        browser.execute_script(
            "arguments[0].scrollIntoView();", reserve_button)
        browser.execute_script("arguments[0].click();", reserve_button)

        # basvuru details page
        # selecting center
        time.sleep(7)
        center = browser.find_element(By.XPATH, "//*[@id='mat-select-0']")
        browser.execute_script(
            "arguments[0].scrollIntoView();", center)
        browser.execute_script("arguments[0].click();", center)

        center_select = browser.find_element(
            By.XPATH, "//mat-option/span[contains(text(),'%s')]" % str(result['Visa_center'].to_string(index=False)))
        browser.execute_script(
            "arguments[0].scrollIntoView();", center_select)
        browser.execute_script("arguments[0].click();", center_select)

        # selecting visa type start 6-7
        time.sleep(7)
        visa_type = browser.find_element(By.XPATH, "//*[@id='mat-select-2']")
        browser.execute_script(
            "arguments[0].scrollIntoView();", visa_type)
        browser.execute_script("arguments[0].click();", visa_type)

        visa_type_select = browser.find_element(
            By.XPATH, "//*[text()[contains(.,'%s')]]" % str(result['Visa_type'].to_string(index=False)))
        browser.execute_script(
            "arguments[0].scrollIntoView();", visa_type_select)
        browser.execute_script(
            "arguments[0].click();", visa_type_select)

        # visa_type_select.click()
        time.sleep(7)
        visa_cathegory = browser.find_element(
            By.XPATH, "//*[@id='mat-select-4']")
        browser.execute_script(
            "arguments[0].scrollIntoView();", visa_cathegory)
        browser.execute_script("arguments[0].click();", visa_cathegory)

        visa_cath_select = browser.find_element(
            By.XPATH, "// *[text()[contains(., '%s')]]" % str(result['Visa_cathegory'].to_string(index=False)))
        browser.execute_script(
            "arguments[0].scrollIntoView();", visa_cath_select)
        browser.execute_script(
            "arguments[0].click();", visa_cath_select)

        # continue button
        time.sleep(10)
        continue_btn = browser.find_element(
            By.XPATH, '/html/body/app-root/div/app-eligibility-criteria/section/form/mat-card[2]/button')
        if continue_btn.is_enabled():
            browser.execute_script(
                "arguments[0].scrollIntoView();", continue_btn)
            browser.execute_script(
                "arguments[0].click();", continue_btn)

            # personal details information

            # Name field
            time.sleep(5)
            Name = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="mat-input-2"]')))
            Name.send_keys(
                str(result['First_name'].to_string(index=False)))

            # last Name field
            time.sleep(2)
            Last_name = browser.find_element(
                By.XPATH, '//*[@id="mat-input-3"]')
            Last_name.send_keys(
                str(result['Last_name'].to_string(index=False)))

            # sex field 11 femail , 12 male, 13 others
            time.sleep(2)
            click_sex = browser.find_element(
                By.XPATH, '//*[@id="mat-select-6"]')
            browser.execute_script(
                "arguments[0].scrollIntoView();", click_sex)
            browser.execute_script("arguments[0].click();", click_sex)

            sex = browser.find_element(
                By.XPATH, "//mat-option/span[contains(text(),'%s')]" % result['Sex'].to_string(index=False))
            browser.execute_script(
                "arguments[0].scrollIntoView();", sex)
            browser.execute_script("arguments[0].click();", sex)

            # date of birth field
            time.sleep(2)
            birth = browser.find_element(By.XPATH, '//*[@id="dateOfBirth"]')
            birth.send_keys(
                result['Birth_date'].to_string(index=False))

            # Nationality field
            time.sleep(4)
            nationality = browser.find_element(
                By.XPATH, '//*[@id="mat-select-8"]')
            browser.execute_script(
                "arguments[0].scrollIntoView();", nationality)
            browser.execute_script(
                "arguments[0].click();", nationality)

            select_nation = browser.find_element(
                By.XPATH, "//mat-option/span[contains(text(),'%s')]" % result['Nationality'].to_string(index=False))
            browser.execute_script(
                "arguments[0].scrollIntoView();", select_nation)
            browser.execute_script(
                "arguments[0].click();", select_nation)

            # passport Number field

            passport = browser.find_element(By.XPATH, '//*[@id="mat-input-4"]')
            passport.send_keys(
                str(result['Passport_no'].to_string(index=False)))

            # passport expire date field

            expire_date = browser.find_element(
                By.XPATH, '//*[@id="passportExpirtyDate"]')
            expire_date.send_keys(str(
                result['Passport_expire'].to_string(index=False)))

            # country code field

            code = browser.find_element(By.XPATH, '//*[@id="mat-input-5"]')
            code.send_keys(
                str(result['Country_code'].to_string(index=False)))

            # phone nu field

            phone = browser.find_element(By.XPATH, '//*[@id="mat-input-6"]')
            phone.send_keys(
                str(result['Phone_no'].to_string(index=False)))

            # email field

            email_address = browser.find_element(
                By.XPATH, '//*[@id="mat-input-7"]')
            email_address.send_keys(
                str(result['New_email'].to_string(index=False)))

            # register button
            time.sleep(2)
            registry = browser.find_element(
                By.XPATH, '/html/body/app-root/div/app-applicant-details/section/mat-card[2]/app-dynamic-form/div/div/app-dynamic-control/div/div/div[2]/button')
            browser.execute_script(
                "arguments[0].scrollIntoView();", registry)
            browser.execute_script("arguments[0].click();", registry)

            # continue button
            time.sleep(15)
            continue_btn_details = browser.find_element(
                By.XPATH, '/html/body/app-root/div/app-applicant-details/section/mat-card[2]/div[2]/div[2]/button')
            browser.execute_script(
                "arguments[0].scrollIntoView();", continue_btn_details)
            browser.execute_script(
                "arguments[0].click();", continue_btn_details)

            # selecting available date
            time.sleep(5)
            availabe_date = browser.find_elements(
                By.XPATH, '//td[contains(concat(" ",normalize-space(@class)," "),"date-availiable")]/div[@class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"]/div[@class="fc-daygrid-day-top"]/a[@class = "fc-daygrid-day-number"]')
            for date in availabe_date:
                browser.execute_script(
                    "arguments[0].scrollIntoView();", date)
                date.click()
                break

            time.sleep(3)
            times = browser.find_elements(
                By.XPATH, '//*[@name="SlotRadio"]')
            for time_element in times:
                browser.execute_script(
                    "arguments[0].scrollIntoView();", time_element)
                time_element.click()
                break
            # continue to next page button
            time.sleep(3)
            continue_btn_next = browser.find_element(
                By.XPATH, '/html/body/app-root/div/app-book-appointment/section/mat-card[2]/div/div[2]/button')
            if continue_btn_next.is_enabled():
                # ActionChains(browser).click(continue_btn_next).perform()
                browser.execute_script(
                    "arguments[0].scrollIntoView();", continue_btn_next)
                browser.execute_script(
                    "arguments[0].click();", continue_btn_next)

                # condition checkbox
                time.sleep(7)
                checkbox1 = browser.find_element(
                    By.XPATH, '//*[@id="mat-checkbox-1-input"]')
                browser.execute_script(
                    "arguments[0].scrollIntoView();", checkbox1)
                browser.execute_script(
                    "arguments[0].click();", checkbox1)

                checkbox2 = browser.find_element(
                    By.XPATH, '//*[@id="mat-checkbox-2-input"]')
                browser.execute_script(
                    "arguments[0].scrollIntoView();", checkbox2)
                browser.execute_script(
                    "arguments[0].click();", checkbox2)

                # button click to go payment
                time.sleep(3)
                online_btn = browser.find_element(
                    By.XPATH, '/html/body/app-root/div/app-review-and-payment/section/form/mat-card[2]/div/div[2]/button')
                browser.execute_script(
                    'arguments[0].scrollIntoView', online_btn)
                browser.execute_script(
                    'arguments[0].click()', online_btn)

                time.sleep(7)

            else:
                messagebox.showerror(
                    "Information", 'Operation failed, Try Again')
                browser.quit()
        else:
            messagebox.showerror(
                "Error", 'appointement date is not available')
            browser.quit()
    except:
        messagebox.showerror(
            'Information', 'Porgram will exit')
        print('No appointment available')
        browser.quit()


def threadautomate():
    t1 = threading.Thread(target=automate)
    t1.start()

############################## AUTOMATE SECTION #######################################


if __name__ == "__main__":
    multiprocessing.freeze_support()
    root = Tk()
    txt_search = StringVar()
    email_vfs = StringVar()
    password = StringVar()
    visa_center = StringVar()
    visa_type = StringVar()
    visa_cath = StringVar()
    first_name = StringVar()
    last_name = StringVar()
    passport_no = StringVar()

    passport_exp = StringVar()
    phone_no = StringVar()
    country_code = StringVar()
    birth_date = StringVar()
    sex = StringVar()
    nationality = StringVar()
    new_email = StringVar()
    cid = StringVar()
    # display section
    wrapper1 = LabelFrame(root, text="Client Recods History Details")
    wrapper2 = LabelFrame(root, text="Search")
    wrapper3 = LabelFrame(root, text="Client data")

    wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
    wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
    wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

    trv = ttk.Treeview(wrapper1, columns=(0, 1, 2, 3, 4, 5, 6, 7, 8,
                                          9, 10, 11, 12, 13, 14, 15), show="headings", height="6")
    trv.pack()
    trv.heading(0, text="ID")
    trv.heading(1, text="Email")
    trv.heading(2, text="Password")
    trv.heading(3, text="Visa Center")
    trv.heading(4, text="Visa Type")
    trv.heading(5, text="Visa Cathegory")
    trv.heading(6, text="First Name")
    trv.heading(7, text="Last Name")
    trv.heading(8, text="Sex")
    trv.heading(9, text="Birth data")
    trv.heading(11, text="Passport Number")
    trv.heading(12, text="Passport Exp date")
    trv.heading(10, text="Nationality")
    trv.heading(13, text="Country Code")
    trv.heading(14, text="Phone Number")
    trv.heading(15, text="Email Address")

    # event listener
    trv.bind('<Double 1>', getrow)
    query = "SELECT * FROM customers"
    cur.execute(query)
    rows = cur.fetchall()
    update(rows)

    # search section
    lbl_search = Label(wrapper2, text="Search by Name or passport no")
    lbl_search.pack(side=tk.LEFT, padx=10)
    ent_search = Entry(wrapper2, textvariable=txt_search)
    ent_search.pack(side=tk.LEFT, padx=6)
    btn_search = Button(
        wrapper2, text="Search", command=search)
    btn_search.pack(side=tk.LEFT, padx=6)
    btn_clear = Button(wrapper2, text="Clear", command=clear)
    btn_clear.pack(side=tk.LEFT, padx=10)

    btn_ato = Button(wrapper2, text="Get Appointment",
                     command=threadautomate, state=DISABLED)
    btn_ato.pack(side=tk.RIGHT, padx=10)

    # user data section
    lbl1 = Label(wrapper3, text="Email:")
    lbl1.grid(row=0, column=0, padx=5, pady=3, sticky='W')
    ent_email = Entry(wrapper3, width=25, textvariable=email_vfs)
    ent_email.grid(row=0, column=1, padx=5, pady=3, sticky='W')

    lbl2 = Label(wrapper3, text="Password:")
    lbl2.grid(row=1, column=0, padx=5, pady=3, sticky='W')
    ent_pass = Entry(wrapper3, width=25, textvariable=password)
    ent_pass.grid(row=1, column=1, padx=5, pady=3, sticky='W')

    ent_id = Entry(wrapper3, width=25, textvariable=cid)
    ent_id.grid_remove()

    lbl3 = Label(wrapper3, text="Visa Center:")
    lbl3.grid(row=0, column=2, padx=5, pady=3, sticky='W')
    ent_visa_center = ttk.Combobox(
        wrapper3, width=40, textvariable=visa_center)
    ent_visa_center['values'] = ('Poland Visa Application Center Ankara', 'Poland Visa Application Center Antalya', 'Poland Visa Application Center Beyoglu', 'Poland Visa Application Center Gaziantep', 'Poland Visa Application Center Izmir'
                                 )
    ent_visa_center.grid(row=0, column=3, padx=5, pady=3, sticky='W')

    lbl4 = Label(wrapper3, text="Visa Type:")
    lbl4.grid(row=1, column=2, padx=5, pady=3, sticky='W')
    ent_visa_type = ttk.Combobox(wrapper3, width=40, textvariable=visa_type)
    ent_visa_type['values'] = ('National Visa (Type D) / Uzun Donem  / Wiza typu D',
                               'Schengen Visa  (Type C) / Kisa Donem / Wiza typu C')
    ent_visa_type.grid(row=1, column=3, padx=5, pady=3, sticky='W')

    lbl5 = Label(wrapper3, text="Visa Cathegory:")
    lbl5.grid(row=2, column=2, padx=5, pady=3, sticky='W')
    ent_visa_cath = ttk.Combobox(wrapper3, width=40, textvariable=visa_cath)
    ent_visa_cath['values'] = ('Select one of three blow choice if National vias is selected', '1- Higher Education / Yuksek Ogrenim / studia wyzsze', '2- Work permit / Calisma Izni / w celu wykonywania pracy', '3- Long-Stay others / Diger Uzun Donem / wiza typu D w celu innym niz wymienione', 'Select one of three blow choice if Shengen vias is selected',
                               '1- Business / Is Seyahati / w celu biznesowym', '2- Tourist / Turistik / w celu turystycznym', '3- Truck-drivers / Tir Soforu / kierowcy zawodowi', '4- Short-Stay others / Diger Kisa Donem / wiza typu C w celu innym niz wymienione')
    ent_visa_cath.grid(row=2, column=3, padx=5, pady=3, sticky='W')

    lbl6 = Label(wrapper3, text="First Name:")
    lbl6.grid(row=3, column=0, padx=5, pady=3, sticky='W')
    ent_first_name = Entry(wrapper3, width=25, textvariable=first_name)
    ent_first_name.grid(row=3, column=1, padx=5, pady=3, sticky='W')

    lbl7 = Label(wrapper3, text="Last Name:")
    lbl7.grid(row=4, column=0, padx=5, pady=3, sticky='W')
    ent_last_name = Entry(wrapper3, width=25, textvariable=last_name)
    ent_last_name.grid(row=4, column=1, padx=5, pady=3, sticky='W')

    lbl8 = Label(wrapper3, text="Passport no:")
    lbl8.grid(row=5, column=0, padx=5, pady=3, sticky='W')
    ent_passport_no = Entry(wrapper3, width=25, textvariable=passport_no)
    ent_passport_no.grid(row=5, column=1, padx=5, pady=3, sticky='W')

    lbl9 = Label(wrapper3, text="Passport expire date:")
    lbl9.grid(row=6, column=0, padx=5, pady=3, sticky='W')
    ent_passport_exp = Entry(wrapper3, width=25, textvariable=passport_exp)
    ent_passport_exp.grid(row=6, column=1, padx=5, pady=3, sticky='W')

    lbl10 = Label(wrapper3, text="Date of Birth:")
    lbl10.grid(row=7, column=0, padx=5, pady=3, sticky='W')
    ent_birth_date = Entry(wrapper3, width=25, textvariable=birth_date)
    ent_birth_date.grid(row=7, column=1, padx=5, pady=3, sticky='W')

    lbl11 = Label(wrapper3, text="Country code:")
    lbl11.grid(row=6, column=2, padx=5, pady=3, sticky='W')
    ent_country_code = Entry(wrapper3, width=25, textvariable=country_code)
    ent_country_code.grid(row=6, column=3, padx=5, pady=3, sticky='W')

    lbl12 = Label(wrapper3, text="Phone Number:")
    lbl12.grid(row=7, column=2, padx=5, pady=3, sticky='W')
    ent_phone_no = Entry(wrapper3, width=25, textvariable=phone_no)
    ent_phone_no.grid(row=7, column=3, padx=5, pady=3, sticky='W')

    lbl13 = Label(wrapper3, text="Gender:")
    lbl13.grid(row=3, column=2, padx=5, pady=3, sticky='W')
    ent_sex = ttk.Combobox(wrapper3, width=15, textvariable=sex)
    ent_sex['values'] = ('Male', 'Female', 'Others')
    ent_sex.grid(row=3, column=3, padx=5, pady=3, sticky='W')

    lbl14 = Label(wrapper3, text="Nationality:")
    lbl14.grid(row=4, column=2, padx=5, pady=3, sticky='W')
    ent_country = ttk.Combobox(wrapper3, width=20, textvariable=nationality)
    ent_country['values'] = ("AFGHANISTAN",
                             "ALBANIA",
                             "ALGERIA",
                             "ANDORRA",
                             "ANGOLA",
                             "ANTIGUA AND BARBUDA",
                             "ARGENTINA",
                             "ARMENIA",
                             "AUSTRALIA",
                             "AUSTRIA",
                             "AUSTRIAN EMPIRE",
                             "AZERBAIJAN",
                             "BADEN",
                             "BAHAMAS, THE",
                             "BAHRAIN",
                             "BANGLADESH",
                             "BARBADOS",
                             "BAVARIA",
                             "BELARUS",
                             "BELGIUM",
                             "BELIZE",
                             "BENIN (DAHOMEY)",
                             "BOLIVIA",
                             "BOSNIA AND HERZEGOVINA",
                             "BOTSWANA",
                             "BRAZIL",
                             "BRUNEI",
                             "BRUNSWICK AND LÜNEBURG",
                             "BULGARIA",
                             "BURKINA FASO (UPPER VOLTA)",
                             "BURMA",
                             "BURUNDI",
                             "CABO VERDE",
                             "CAMBODIA",
                             "CAMEROON",
                             "CANADA",
                             "CAYMAN ISLANDS, THE",
                             "CENTRAL AFRICAN REPUBLIC",
                             "CENTRAL AMERICAN FEDERATION",
                             "CHAD",
                             "CHILE",
                             "CHINA",
                             "COLOMBIA",
                             "COMOROS",
                             "CONGO FREE STATE, THE",
                             "COSTA RICA",
                             "COTE DIVOIRE (IVORY COAST)",
                             "CROATIA",
                             "CUBA",
                             "CYPRUS",
                             "CZECHIA",
                             "CZECHOSLOVAKIA",
                             "DEMOCRATIC REPUBLIC OF THE CONGO",
                             "DENMARK",
                             "DJIBOUTI",
                             "DOMINICA",
                             "DOMINICAN REPUBLIC",
                             "DUCHY OF PARMA, THE",
                             "EAST GERMANY (GERMAN DEMOCRATIC REPUBLIC)",
                             "ECUADOR",
                             "EGYPT",
                             "EL SALVADOR",
                             "EQUATORIAL GUINEA",
                             "ERITREA",
                             "ESTONIA",
                             "ESWATINI",
                             "ETHIOPIA",
                             "FEDERAL GOVERNMENT OF GERMANY (1848-49)",
                             "FIJI",
                             "FINLAND",
                             "FRANCE",
                             "GABON",
                             "GAMBIA, THE",
                             "GEORGIA",
                             "GERMANY",
                             "GHANA",
                             "GRAND DUCHY OF TUSCANY, THE",
                             "GREECE",
                             "GRENADA",
                             "GUATEMALA",
                             "GUINEA",
                             "GUINEA-BISSAU",
                             "GUYANA",
                             "HAITI",
                             "HANOVER",
                             "HANSEATIC REPUBLICS",
                             "HAWAII",
                             "HESSE",
                             "HOLY SEE",
                             "HONDURAS",
                             "HUNGARY",
                             "I",
                             "ICELAND",
                             "INDIA",
                             "INDONESIA",
                             "IRAN",
                             "IRAQ",
                             "IRELAND",
                             "ISRAEL",
                             "ITALY",
                             "JAMAICA",
                             "JAPAN",
                             "JORDAN",
                             "KAZAKHSTAN",
                             "KENYA",
                             "KINGDOM OF SERBIA/YUGOSLAVIA",
                             "KIRIBATI",
                             "KOREA",
                             "KOSOVO",
                             "KUWAIT",
                             "KYRGYZSTAN",
                             "LAOS",
                             "LATVIA",
                             "LEBANON",
                             "LESOTHO",
                             "LEW CHEW (LOOCHOO)",
                             "LIBERIA",
                             "LIBYA",
                             "LIECHTENSTEIN",
                             "LITHUANIA",
                             "LUXEMBOURG",
                             "MADAGASCAR",
                             "MALAWI",
                             "MALAYSIA",
                             "MALDIVES",
                             "MALI",
                             "MALTA",
                             "MARSHALL ISLANDS",
                             "MAURITANIA",
                             "MAURITIUS",
                             "MECKLENBURG-SCHWERIN",
                             "MECKLENBURG-STRELITZ",
                             "MEXICO",
                             "MICRONESIA",
                             "MOLDOVA",
                             "MONACO",
                             "MONGOLIA",
                             "MONTENEGRO",
                             "MOROCCO",
                             "MOZAMBIQUE",
                             "NAMIBIA",
                             "NASSAU",
                             "NAURU",
                             "NEPAL",
                             "NETHERLANDS, THE",
                             "NEW ZEALAND",
                             "NICARAGUA",
                             "NIGER",
                             "NIGERIA",
                             "NORTH GERMAN CONFEDERATION",
                             "NORTH GERMAN UNION",
                             "NORTH MACEDONIA",
                             "NORWAY",
                             "OLDENBURG",
                             "OMAN",
                             "ORANGE FREE STATE",
                             "PAKISTAN",
                             "PALAU",
                             "PANAMA",
                             "PAPAL STATES",
                             "PAPUA NEW GUINEA",
                             "PARAGUAY",
                             "PERU",
                             "PHILIPPINES",
                             "PIEDMONT-SARDINIA",
                             "POLAND",
                             "PORTUGAL",
                             "QATAR",
                             "REPUBLIC OF GENOA",
                             "REPUBLIC OF KOREA (SOUTH KOREA)",
                             "REPUBLIC OF THE CONGO",
                             "ROMANIA",
                             "RUSSIA",
                             "RWANDA",
                             "SAINT KITTS AND NEVIS",
                             "SAINT LUCIA",
                             "SAINT VINCENT AND THE GRENADINES",
                             "SAMOA",
                             "SAN MARINO",
                             "SAO TOME AND PRINCIPE",
                             "SAUDI ARABIA",
                             "SCHAUMBURG-LIPPE",
                             "SENEGAL",
                             "SERBIA",
                             "SEYCHELLES",
                             "SIERRA LEONE",
                             "SINGAPORE",
                             "SLOVAKIA",
                             "SLOVENIA",
                             "SOLOMON ISLANDS, THE",
                             "SOMALIA",
                             "SOUTH AFRICA",
                             "SOUTH SUDAN",
                             "SPAIN",
                             "SRI LANKA",
                             "SUDAN",
                             "SURINAME",
                             "SWEDEN",
                             "SWITZERLAND",
                             "SYRIA",
                             "TAJIKISTAN",
                             "TANZANIA",
                             "TEXAS",
                             "THAILAND",
                             "TIMOR-LESTE",
                             "TOGO",
                             "TONGA",
                             "TRINIDAD AND TOBAGO",
                             "TUNISIA",
                             "TURKEY",
                             "TURKMENISTAN",
                             "TUVALU",
                             "TWO SICILIES",
                             "UGANDA",
                             "UKRAINE",
                             "UNION OF SOVIET SOCIALIST REPUBLICS",
                             "UNITED ARAB EMIRATES, THE",
                             "UNITED KINGDOM, THE",
                             "URUGUAY",
                             "UZBEKISTAN",
                             "VANUATU",
                             "VENEZUELA",
                             "VIETNAM",
                             "WÜRTTEMBERG",
                             "YEMEN",
                             "ZAMBIA",
                             "ZIMBABWE")
    ent_country.grid(row=4, column=3, padx=5, pady=3, sticky='W')

    lbl15 = Label(wrapper3, text="Email Address:")
    lbl15.grid(row=5, column=2, padx=5, pady=3, sticky='W')
    ent_new_email = Entry(wrapper3, width=25, textvariable=new_email)
    ent_new_email.grid(row=5, column=3, padx=5, pady=3, sticky='W')

    add_btn = Button(wrapper3, text="Add New", command=add_new)
    update_btn = Button(wrapper3, text="Update", command=update_customer)
    delete_btn = Button(wrapper3, text="Delete", command=delete_customer)
    clean_btn = Button(wrapper3, text="Clear", command=clean_input)

    add_btn.grid(row=10, column=0,  padx=5, pady=10)
    update_btn.grid(row=10, column=1,  padx=5, pady=10)
    delete_btn.grid(row=10, column=2,  padx=5, pady=10)
    clean_btn.grid(row=10, column=3,  padx=5, pady=10)

    root.title("Form")
    root.geometry("700x600")

    root.mainloop()
