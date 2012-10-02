/*!
 * Ziga JavaScript Library v0.42
 * https://github.com/trenta3dev/ziga
 *
 * Released under the ??? licence.
 */

function Channel(baseURL, channelName, token) {
  this.baseURL = baseURL;
  this.channelName = channelName;
  this.token = token;

  this._handleMessage = function (e) {
    console.log('GOT', $.parseJSON(e.data));
    $('#test').append($('<p>').text(e.data));
  };
  this._handleOpen = function (e) {
    alert("open");
  };
  this._handleError = function (e) {
    alert("close");
  };
}

Channel.prototype._getURL = function () {
  return this.baseURL + this.channelName + "/";
};

Channel.prototype.connect = function () {
  var url = this._getURL();

  this.source = new EventSource(url);

  this.source.addEventListener('message', this._handleMessage, false);
  this.source.addEventListener('open', this._handleOpen, false);
  this.source.addEventListener('error', this._handleError, false);

  return this;
};

function Ziga(applicationKey, options) {
  this.applicationKey = applicationKey;
  this.options = options;
}

Ziga.prototype.subscribe = function (channelName) {
  var channel
    , token;

  if ("private:".indexOf(channelName) >= 0) {
    token = "token";  // request it
    return;  // private channel
  }

  channel = new Channel(this._getURL(), channelName, token);
  channel.connect();
  return channel;
};

Ziga.prototype.unsubscribe = function (channelName) {
  return console.log('slogged', channelName);
};

Ziga.prototype._getURL = function () {
  return "http://localhost:9442/" + this.applicationKey + "/";
};
