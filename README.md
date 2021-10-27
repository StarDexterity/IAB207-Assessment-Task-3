# IAB207-Assessment-Task-3
**My Sports**  
Angus Phelan - n11032111  
Joshua Bryans - n10996931    
Zachary Torr - n11099381
    
    
**TODO**   
- The owner of the event should be able to update the details of the event (including the status). They can also delete their own events. Create a page where the owner can see all their events, from this page, have an option to delete and update each event. An additional update page will be required. It will look very similiar to the create event page.
    
- To buy tickets, the user should be logged in. The user should provide details such as the quantity of the tickets to be booked. An order is generated by the application, and the order detail (order id) is provided to the user for reference.   
        a. If the user buys tickets equal to the tickets available, the event should be labeled ‘Booked out’ 
        b. If the user enters a number of tickets that exceeds the tickets available, the application should inform the user that the order cannot be placed. 
    

- Your landing page must allow users to browse the events by category (you are free to support this functionality using a drop-down menu or some other intuitive way). In addition, you might include a text-based search functionality. However, this is an advanced feature and is optional to those who would like to include it (it is not specified in the CRA but the more intuitive your search is the better).  
    **Features:**   
    - Search bar (optional)   
    - Filters (optional)   
    - Browse by category   
     
       
- Error Handling:   
    a. You must gracefully handle instances of “page is not found” and “internal server errors” by providing a useful message and allowing users to easily navigate back to the landing/home page.   
    b. A user should be authenticated (via login) to perform tasks on this site.   
    c. User input validation – empty strings, incorrect input for specific fields, etc. should be correctly managed. The more validators the better, aka email and password validators (make sure it makes sense for the context)   
    d. Use the post-redirect-get pattern when posting forms.


