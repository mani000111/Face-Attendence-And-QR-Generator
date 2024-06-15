import qrcode,time,os
from PIL import Image

#global var

#who not in the list
def who_not_in_db():
    users_in_dataset_folder = os.listdir("users_datasets")
    for user in users_in_dataset_folder:
        user = user.split(".")[0]
        if user not in database:
            print(user,"\n")

#space make
def space_maker(text,total_space):
    ct = text
    need_space = total_space - len(text)
    
    for i in range(need_space):
        text += "  "
    if ct=="DEPARTMENT" or ct=="LONGITUDE":
        text = text[:-2]

    return text

#get current date and time
def get_date_time():
    #current date
    current_date = time.ctime().split(" ")
    current_date = f"{current_date[2]} - {current_date[1]} - {current_date[4]} ({current_date[0]})"
    
    #current time
    current_time = time.ctime().split(" ")[3]

    return current_date,current_time

#make qr code func
def make_qr(user_name):
    try:
        qr_template = ""

        #fetch data from database
        for key,val in database[user_name].items():
                if not val=="":
                        qr_template += f"{space_maker(key,13)} : {val}\n"
        
        #date ,time ,lat and long °
        c_date,c_time = get_date_time()
        qr_template += f"{space_maker('DATE',14)} : {c_date}\n{space_maker('TIME',14)} : {c_time}"

        user_qr = qrcode.make(qr_template)
        user_qr.save(f"users_qrcode\\{user_name}.png")
        #resize image
        img = Image.open(f"users_qrcode\\{user_name}.png")
        img = img.resize((400,400)) #image size
        img.save(f"users_qrcode\\{user_name}.png")

        return 0
    
    except :
        return 1


#  DATABASE -----------------------------------------------------------------------------------------------------------------------------------------

database = {


        "musk":{
            "NAME"  :"ELON MUSK",
            "GENDER" : "MALE",
            "QUALIFICATION" : "",
            "DEPARTMENT" : "",
            "EXPERIENCE" : "",
            "COLLEGE" : "THE INDIAN COLLEGE",
            "LOCATION" : "",
            },



    
}

#total data
# print("Total data : ",len(database.keys()))
# print("Total data names : ",database.keys())


