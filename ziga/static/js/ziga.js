/*!
 * Ziga JavaScript Library v0.42
 * https://github.com/trenta3dev/ziga
 *
 * Released under the ??? licence.
 */

var Channel = function (baseURL, channelName, token, functionError, functionOpen) {
  var self = this;

  this.baseURL = baseURL;
  this.channelName = channelName;
  this.token = token;

  this._handleMessage = function (e) {
    $(self).trigger("newMessage", $.parseJSON(e.data).data);
  };
  this._handleOpen = function (e) {
    if (functionOpen)
      functionOpen();
  };
  this._handleError = function (e) {
    if (functionError)
      functionError();
  };
};

Channel.prototype._getURL = function () {
  return this.baseURL + this.channelName + "/";
};

Channel.prototype.on = function(name, callback) {
  return $(this).on(name, callback);
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

Ziga.prototype.subscribe = function (channelName, functionError, functionOpen) {
  var channel
    , token;

  if ("private:".indexOf(channelName) >= 0) {
    token = "token";  // request it
    return;  // private channel
  }

  channel = new Channel(this._getURL(), channelName, token, functionError, functionOpen);
  channel.connect();

  return channel;
};

Ziga.prototype.unsubscribe = function (channelName) {
  return console.log('slogged', channelName);
};

Ziga.prototype._getURL = function () {
  return "http://localhost:4242/" + this.applicationKey + "/";
};