# OFFCORSS PROJECT: WOW
##### DS4A TEAM 25
C.I HERMECO S.A is the market leader in clothing for the children's segment in Colombia. It is a company with 40 years of experience committed to offering authentic, reliable and fun products and experiences for irreverent children with a COOL lifestyle, exceeding the satisfaction of our consumers and guaranteeing the durability of the company.

The company has detected an opportunity in understanding its customers and what they think of its products and services. That is the reason why we implemented WOW. 

## General Review
WOW is a powerful tool that allows OFFCORSS  to understand how the customers feel towards the brand. The application takes in a lot of information that the company has collected from customer surveys, and also information of the behavior of the company and its competitors in social platforms (like Facebook and Instagram). It applies a sentiment analysis model that was trained with spec

All is visualized in a stunning and interactive dashboard application that allows the user to navigate through comments history over time, recognizing associated products and sentiments.

## Project Structure
In this repository you will find two folders:

* **App:** This folder contains all the front-end and back-end structure of the application. It contains 4 folders:
    * **Notebooks:** there are recopiled the notebooks that we have develoment for the exploratory analysis of the data, and the model training and validing.
    * **Powerbi:** this folder contains the front-end development of the application made in Power Bi.
    * **Scrapping:** this folder contains three developments to automate the extraction of social media data from both the company and its competitors. One of them is implemented in robo framework to extract the facebook post and reactions. The other two, was made to extract the posts and comments from instagram (one using a library to extract the historic of the data and the other to refresh the database with the lasts post).
    * **Database:** this folder contains the structure that we desingned for the database, with csv files of the most recient versions of the stored data.

* **Documents:** This folder contains some general reports and deliveries documents associated with the course.