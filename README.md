# URHope

**Tasks completed**

1. Role based sign up and login for volunteers and NGOs
2. Role based profile updation for volunteers and NGOs
3. Task Creation, updation, deletion by NGO/Group
4. Task viewed by volunteers based on their pincode
5. Volunteers can apply to volunteer for maximum 2 tasks at a time. If a volunteer want to defy, then he/she can take back application
6. In any case when a volunteer applies for the task or take application back, respective NGO/group will be notified via an email
7. NGO can download the details of volunteers who has applied for any task, as an excel file
8. A notification is added on notification page of the NGO after succesful application for any task provided by NGO, by volunteers
9. NGO can monitor the tasks and has dynamic information about everything that is related to any task created by them
10. NGOs can communicate with volunteers via email or phone number and volunteers can communicate as well
11. Pin based search for NGO for needy people
12. Couldn't help section: Needy person can fill the form and nearby NGOs will receive the notifications on an email. If there are no nearby NGOs found then an email will be sent to URHope Team containing that person's information
13. Admin Panel: Admin can monitor the whole website. He can view,delete NGOs, Volunteers, Tasks and can see active status of any user present on the website. He can see the logs and can decide about the behaviour of website and monitor the website efficiently


**Tasks Remaining**
1. Integration of Jino's work
2. Releasing fully functional Version 1
3. Start working to integrate new Frontend Designs
4. Releasing fully functional Version 2
5. Working to include new additional features


# Running in Local

## SETUP
```python
git clone git@github.com:sk-sharique/urhope.git
cd urhope
python3 -m venv urhope.env
source urhope.env/bin/activate
pip3 install -r requirements.txt
```

## RUNNING APP ON LOCAL SERVER

```python
python app.py
```
Access the application on your local server.
