# A-level Computer Science Python Project - Cashier System
## Jack Domleo - The Redhill Academy Sixth Form - 2017/18

This was my coursework project for my A-level Computer Science course. I decided to program a cashier shop for a pretend client, 'Jenny', that uses a local database.

There are many things wrong with this project, however due to my knowledge and experience at the time of doing the project, I was not able to identify them. I.e.
- Uses a local database which is bad if the system goes down
- The file and naming conventions are terrible and inconsistent
- The system uses procedural programming and leaves lots of unfinished functions open and running, using up CPU power and memory
- The GUI uses tkinter and looks awful
- No user guide
- Not 100% tested
- Logo isn't transparent or optimised
- Lots of repeated code that could be put into functions
- No version control (Git) since I was not aware of version control until many months after this project was finished and submitted

While these are good points to identify, due to lack of knowledge, were not identifiable at the time. I am planning on redoing this project in Electron JS in the near future, a link will be provided once complete. In the new version, since I have had work experience since this project, I will work towards resolving the issues stated above.

### Setup and start

1. Clone this repo
2. Run the script `MAIN PROGRAM - Cashiersystem.py`
3. Log in initially using `1001` as the username and `1234` as the password
3. Once you make a transaction, a .txt file will be added to the Receipts directory
4. A database, shop.db, will be created. You can drag and drop the database [here](http://inloop.github.io/sqlite-viewer/) to view it.

As mentioned earlier, this is not a great program, however I was only a sixth form student and am looking forward to create a new version in Electron JS.
