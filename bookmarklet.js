// You can use this to create a bookmarklet in your browser.
// You will first need to change api_key and burl_domain.
// Then create a new bookmark, and set its destination to
// javascript: (function() { ...

(function() {
  var api_key = 'YOUR_API_KEY';
  var burl_domain = 'http://localhost:8000';
  var post_url = burl_domain + '/api/v2/burls/';

  xhr = new XMLHttpRequest();
  xhr.open("POST", encodeURI(post_url));
  xhr.setRequestHeader('Authorization', 'Token ' + api_key);
  xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  xhr.overrideMimeType('application/json');
  xhr.send(JSON.stringify({'url': document.location.href, 'description': document.title}));

  xhr.onload = function() {
    if (xhr.status === 201) {
      var responseJson = JSON.parse(xhr.responseText);
      var alertText = burl_domain + '/' + responseJson.burl + '/';
      alert(alertText);
    }
  };
}());
