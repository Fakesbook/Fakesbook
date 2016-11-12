Zoe"-Zach Project
=================

# Goal
To have a website that displays a graph of a social network to its users such that they gain access to one another's information based on friend connections
and boolean sharing controls they set.

The data handled by this webapp should be encrypted in transit and at rest as it will contain sensitive images and data about people.

# TODO

1. Draw 1st-round architecture diagram of the system
2. Implement front-end
  * Simple version of UI
  * Figure out what data UI needs from the server
3. Implement back-end
  * install virtualenv
  * install flask
  * serve index.html at /

# Plan

Frontend
========
* Graph
  * Nodes representing people
  * Images and other data available on click of a node
* Control panel
  * Inputs
    * image upload
    * name
    * todo: other data
  * Boolean toggles for privacy settings
    * who can see image? Fs, FoFs, P
* User interface for viewing and friending people
* User interface for accepting friend requests
* "Who can see my info?" button
  * image
  * name
  * todo: other data
* Account creation in JS, sends PW hash to server as PW
* Key agreements in JS

Backend
=======
* Webserver
  * Flask
  * DB
    * user data
  * Users w/ registration
  * User settings

Encryption
==========
The webserver will store uploaded images and data. The webserver should not be able to read the images and data, and simply store the encrypted files.
In order to implement this, we will need end-to-end encryption involving key agreements between the users of the site.

Key agreement will have to happen in javascript on the client side. Each user will need to enter a password, the hash of which the server stores,
which is used to initiate key agreements with other users. This way, the server will never be able to access the data available to a given e2e session.

To scale this solution to a group, we will need to implement n^2 key agreements, which we can borrow from the Signal Protocol RFC.

# Timeline
* Working instance by February
