console.log('Hello World');

const express = require('express');
const app = express();

const MongoClient = require('mongodb').MongoClient
var db

MongoClient.connect('mongodb://root:password@10.0.0.134:27017', (err, database) => {
  if (err) return console.log(err)
  db = database
  app.listen(3000, () => {
    console.log('listening on 3000')
  })
  app.get('/', (req, res) => {
    // do something here
    res.sendFile(__dirname + '/index.html')
    // Note: __dirname is directory that contains the JavaScript source code. Try logging it and see what you get!
    // Mine was '/Users/zellwk/Projects/demo-repos/crud-express-mongo' for this app.
  })

  //DBMS
function logEvent(message) {
  var logEntry = JSON.parse(message)
  arrayOfObjects.push({
    msg: message
  })
  console.log(logEntry);
  db.collection('eventlog').save(logEntry, (err, result) => {
    if (err) return console.log(err)
    //console.log('logged')

  })
}

  //Get API data
  app.post('/api/get/', (req, res) => {
    res.send('API RESPONSE')
  })

  //Set API data
  app.post('/api/set/', (req, res) => {
    res.send('API RESPONSE')
  })


  //Add junk to db
  app.post('/stockdata', (req, res) => {
    db.collection('quotes').save(req.body, (err, result) => {
      if (err) return console.log(err)

      console.log('saved to database')
      res.redirect('/')
    })
  })
})
