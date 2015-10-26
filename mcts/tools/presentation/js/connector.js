var addConnection = function(connection) {
  connection.onstatechange = function () {
    // connection.state is either 'connected,' 'closed,' or 'terminated'
    console.log("presentation api server connection's state is now ", connection.state);
  };
  connection.onmessage = function (evt) {
      // echo back the data
      connection.send(evt.data);
  };
};

navigator.presentation.receiver.getConnection().then(addConnection);
navigator.presentation.receiver.onconnectionavailable = function(evt) {
  navigator.presentation.receiver.getConnections().then(function(connections) {
    addConnection(connections[connections.length-1]);
  });
};
