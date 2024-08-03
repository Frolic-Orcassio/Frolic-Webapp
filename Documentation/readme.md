# Frolic 2024 User-Roles and Features:

---

The purpose of this webapp is to manage events and information of tech-fest Frolic 2024 hosted by Darshan University.

This webapp is divided into two parts: 1.) main website 2.) admin panel. 

- The purpose of main website is to present information about Frolic, its events, stalls, about us and Darshan University. This is where guest users can authenticate and register their teams and surf the overall site. The event coordinators can also manage their events through this portal after authentication.
- The admin panel is for super users who can manage data for every events and their coordinators plus all other information. They basically have rights to access any piece of information.

There will be 5 types of users roles, the below roles follow hierarchy:

- **Guest** : site visitors
- **Participant** : Authenticated guests
- **Event Coordinator** : A Special participant who can create a certian amount of events
- **Stall admin** : A Special participant who can create/update/delete his/her stall and upload images, description, menu etc... 
- **Admin** : Has access to admin panel and can access profiles of every authenticated users, events, stalls and Frolic information templates. 

The features will be based on hierarchy of users, for example an event coordinator will have all rights that participant has. This hierarchical structure makes it easy to understand features easily.

### Guest:

- Can surf the site, view all information as events, stalls, registration forms and other pages.
- Can authenticate via google sign in

### Participant:

- Register with his team in multiple events upto certain limit or cancle a registered event
- Gets email for registering
- Can view profile information and see event participation status

### Event Coordinator:

- Gets access to event creation dashboard where an event can be customized (can create only one event)
- Can see participated teams registered on his/her event and mark them as ready before event starts
- Can update team status during event
- Email is sent to all team leaders before 15 minutes when event starts

### Stall admin:

-  Gets access to stall creation dashboard where a stall can be customized (can create only one stall)

### Admin:

- Can access all events, stalls and participants data
- An admin can upgrade or downgrade the role of a participant

