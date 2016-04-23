var express = require('express');
var fs = require('fs');
var multer = require("multer");
var wav = require('wav');

var port = 3700;
var outFile = 'demo.wav';
var app = express();

var zerorpc = require("zerorpc");

var zerorpcclient = new zerorpc.Client();
zerorpcclient.connect("tcp://127.0.0.1:4242");

var storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, "/Users/pascal/Desktop/Sorch/server/tmp");
    },
    filename: function (req, file, cb) {
        cb(null, "test.wav");
    }
});

var uploading = multer({
   storage:  storage,
   limits: {fileSize: 10000000, files: 1}
});

app.set('views', __dirname + '/tpl');
app.set('view engine', 'jade');
app.engine('jade', require('jade').__express);
app.use(express.static(__dirname + '/public'))

app.get('/', function(req, res){
  res.render('index', {pageData: {songTitle: ""}});
});

app.post('/upload', uploading.single("wav"), function(req, res, next){
    zerorpcclient.invoke("startNNS", "World!", function(error, result, more) {
        console.log(error);
        console.log(result);
        res.render("index", {pageData: {songTitle: result}});
    });
});
app.listen(port);

console.log('server open on port ' + port);