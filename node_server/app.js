/**
 * Created by skycheung on 2016/11/22.
 */
var http = require('http');
var url = require('url');
var hex = require('./md5');
var des = require('./des');
var thisPwd;
var enResult;

http.createServer(function (request, response) {
    thisPwd = url.parse(request.url, true).query.password;
    enResult = des.strEnc(hex.hex_md5(thisPwd + "neu_dcp").substring(5, 27), "ec07204c8f2948d8b3927e769d63ca31!!", "92112a9c1d234e07b1499ebd9b01da00!@", "402ec3db0a524dc09dc99239b1c82fe2!#");
    response.writeHead(200, {'Content-Type': 'text/plain'});
    response.end(enResult);
}).listen(3000);

console.log('Server running at http://127.0.0.1:3000/');

