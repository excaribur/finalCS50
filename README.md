# NoteInvest
#### Video Demo: https://youtu.be/Rbyc7n3IDDs

#### Description:
Hi everyone. I would like to show my a final project of CS50 course. My project is like a notebook or diary to note your interested stocks.Also, you can save technical price such as resistance price or support price.

You can note stock in SET only (stocks in Thailand only) 

This project has many features or functionality as below
1. Log in and register ( hash password)
2. Search quote (price) by symbol (PTT, BA, MEGA,..)
3. Add stocks in your table to track it
4. Choose stock that you want to follow up
5. Take a note , Technical price(support or resistance) by go to look the chart and description as the link that website provide to you
6. Filter stocks by percent of nearby resistance or support price
7. Unfollow or delete any stocks that you don’t want

#### Data provide by:
This project retrieved data from yahoo finance (www.yahoofinance.com) and scalping Thai name of stock from www.settrade.com

#### Database:
Use sqlite because CS50. It’s easy to use for practice and light weight on IDE of cs50

#### file:App.py
Components in this file are route of request GET and POST from client in web browser 

/ is a homepage. User can get and post

/login is login page 

/register is register page you must provide username and password(at least one of those: number, character, and special characters )

/add to add stock after click qoute 

/info to go to page infomation of stock

/follow to go page that stock was fellow up 

/unfollow if you don't want to follow stock

/save this post to update technical price and note in a information stock page

/cal this post to calculate shares to how much money you must to have if ypu wanto buy stock

/delete to delete stock from database

/scan to filter technical price in percent at the homepage

/logout to log out


#### file: Service.py 
This is helper function to working in function in app.py file

Important functions are

login 
to check login session and make annotation on  top of each route function that need a login to working 

retrieved data from yahoofinance by library and use pandas to read and clean those data

Read ,Update ,Delete in database 

Check for registration password 
Password must be included with at least one of number , alphabetical, and special characters 

#### file: htm,css
Use bootstrap to make up and decorate