import streamlit as st
import pandas as pd
import hashlib
from PIL import Image
import pickle
import bz2
import numpy as np


def make_hashes(password):   
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()

# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,Email,password,Cpassword) VALUES (?,?,?,?,?,?)',(FirstName,LastName,Mobile,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data



def main():
    st.title("Welcome To Crop Recommendation System")
    menu = ["Home","Login","SignUp"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        original_title="<p style='text-align: center;'>Crop Recommendation system predicts the user, what crop type. would be the most suitable for the selected area by collecting. the environmental factors for plant growth and processing. them with the trained sub-models of the main of the system.</p>"
        image = Image.open('flow.png')
        st.image(image)
        st.markdown(original_title, unsafe_allow_html=True)
    elif choice == "Login":
        st.subheader("Login Section")
        Email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(Email,check_hashes(password,hashed_pswd))
            if result:
                st.success("Logged In as {}".format(Email))
                activities=['K-Nearest Neighbors','Liner SVM','Decision Tree','Random Forest','Navier Bayers','ExtraTreesClassifier']
                option=st.selectbox('Which model you use?',activities)
                N=float(st.slider('N Value', 0.0, 140.0))
                P=float(st.slider('N Value', 5.0, 145.0))
                K=float(st.slider('N Value', 5.0, 205.0))
                temp=float(st.slider('N Value', 8.0, 44.0))
                Hum=float(st.slider('N Value', 14.0, 100.0))
                Ph=float(st.slider('N Value', 3.5, 10.0))
                Rain=float(st.slider('N Value', 20.0, 299.0))
                sfile = bz2.BZ2File("All Model", 'r')
                model=pickle.load(sfile)
                if st.button("Predict"):
                    if option=="K-Nearest Neighbors":
                        test_prediction = model[0].predict([[N,P,K,temp,Hum,Ph,Rain]])
                        le=pickle.load(open('le.pkl', 'rb'))
                        label=le.inverse_transform(test_prediction)
                        st.success("The Crop Recommandded is "+label[0])
                        st.success("The Score is "+str(np.amax(model[0].predict_proba([[N,P,K,temp,Hum,Ph,Rain]]))))
                    if option=="Liner SVM":
                        test_prediction = model[1].predict([[N,P,K,temp,Hum,Ph,Rain]])
                        le=pickle.load(open('le.pkl', 'rb'))
                        label=le.inverse_transform(test_prediction)
                        st.success("The Crop Recommandded is "+label[0])
                        #st.success("The Score is "+str(np.amax(model[1].predict_proba([[N,P,K,temp,Hum,Ph,Rain]]))))
                    if option=="Decision Tree":
                        test_prediction = model[2].predict([[N,P,K,temp,Hum,Ph,Rain]])
                        le=pickle.load(open('le.pkl', 'rb'))
                        label=le.inverse_transform(test_prediction)
                        st.success("The Crop Recommandded is "+label[0])
                        st.success("The Score is "+str(np.amax(model[2].predict_proba([[N,P,K,temp,Hum,Ph,Rain]]))))
                    if option=="Random Forest":
                        test_prediction = model[3].predict([[N,P,K,temp,Hum,Ph,Rain]])
                        le=pickle.load(open('le.pkl', 'rb'))
                        label=le.inverse_transform(test_prediction)
                        st.success("The Crop Recommandded is "+label[0])
                        st.success("The Score is "+str(np.amax(model[3].predict_proba([[N,P,K,temp,Hum,Ph,Rain]]))))
                    if option=="Navier Bayers":
                        test_prediction = model[4].predict([[N,P,K,temp,Hum,Ph,Rain]])
                        le=pickle.load(open('le.pkl', 'rb'))
                        label=le.inverse_transform(test_prediction)
                        st.success("The Crop Recommandded is "+label[0])
                        st.success("The Score is "+str(np.amax(model[4].predict_proba([[N,P,K,temp,Hum,Ph,Rain]]))))
                    if option=="ExtraTreesClassifier":
                        test_prediction = model[5].predict([[N,P,K,temp,Hum,Ph,Rain]])
                        le=pickle.load(open('le.pkl', 'rb'))
                        label=le.inverse_transform(test_prediction)
                        st.success("The Crop Recommandded is "+label[0])
                        st.success("The Score is "+str(np.amax(model[5].predict_proba([[N,P,K,temp,Hum,Ph,Rain]]))))
                        
            else:
                st.warning("Incorrect Email/Password")
                
    elif choice == "SignUp":
        FirstName = st.text_input("Firstname")
        LastName = st.text_input("Lastname")
        Mobile = st.text_input("Mobile")
        Email = st.text_input("Email")
        new_password = st.text_input("Password",type='password')
        Cpassword = st.text_input("Confirm Password",type='password')
        if st.button("Signup"):
            create_usertable()
            add_userdata(FirstName,LastName,Mobile,Email,make_hashes(new_password),make_hashes(Cpassword))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
           
if __name__ == '__main__':
    main()