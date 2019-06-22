var nodes, edges, network;

$(document).ready(function() {
	//add tabs
	$("#hostlogtab").dynatabs({
		tabBodyID : "hostlogbody",
		showCloseBtn : true,
	});

  /*$('#stopStreamButtonID').click(function(event) {        
    socket.emit('stopStreamButtonID', {data: ''});
  });

  namespace = '';

  var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
  socket.on('connect', function() {
      socket.emit('my event', {data: 'Connected to server'});
  });

  socket.on('serverUpdate', function(msg) {
    //console.log(msg);
    setStatus(msg);				
  });
  socket.on('lastTrialDiv', function(msg) {
    console.log('lastTrialDiv received')
    plotSpinner(0);
    $('#lastTrialPlotID').html(msg.plotDiv);				
  });
  socket.on('refreshvideostream', function(msg) {
    console.log('refreshvideostream received')
    setStatus(msg);				
    window.location.reload()
  });*/
});

function addNewStaticTab()
	{
		$.addDynaTab({
			tabID : 'hostlogtab',
			type : 'html',
			html : '<p>This HTML content is loaded statically</p>',
			params : {},
			tabTitle : 'google.com'
		});
	}

// convenience method to stringify a JSON object
function toJSON(obj) {
    return JSON.stringify(obj, null, 4);
}

function addNode() {
    try {
        nodes.add({ id: '4', label: 'PC4', image: 'img/pc.png', shape: 'image', font: '12px Arial white'});
    }
    catch (err) {
        alert(err);
    }
}

function updateNode() {
    try {
        nodes.update({
            id: '1',
            image: 'img/pc2.png'
        });
    }
    catch (err) {
        alert(err);
    }
}

function addEdge() {
    try {
        edges.add({ id: '3', from: '2', to: '4'});
    }
    catch (err) {
        alert(err);
    }
}

function draw() {
    // create an array with nodes
    nodes = new vis.DataSet();
    nodes.add([
        {id: '1', label: 'Node 1', image: 'img/pc.png', shape: 'image', font: '12px Arial white'},
        {id: '2', label: 'Node 2', image: 'img/pc.png', shape: 'image', font: '12px Arial white'},
        {id: '3', label: 'Node 3', image: 'img/pc.png', shape: 'image', font: '12px Arial white'},
    ]);

    // create an array with edges
    edges = new vis.DataSet();
    edges.add([
        {id: '1', from: '1', to: '2'},
        {id: '2', from: '1', to: '3'},
    ]);

    // create a network
    var container = document.getElementById('network');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {};
    network = new vis.Network(container, data, options);

    network.on("click", function (params) {
        params.event = "[original event]";
        //alert('Click event:' + JSON.stringify(params, null, 4));
        console.log('click event, getNodeAt returns: ' + this.getNodeAt(params.pointer.DOM));
    });
}

function add_host() {

  addNewStaticTab();
  var tab = $('#hostlogtab.tabs');

  var len = $('#hostlogtab.tabs')[0].children.length;
  var href = $('#hostlogtab.tabs')[0].children[len-1].children[0];
  var event = $.Event("click");
  event.data = {ahref:"",tab:""};
  event.data.ahref = href;
  event.data.tab = tab;
  $("#hostlogtab").showTab(event);

  $('#ps')[0].innerHTML = "";
  $('#syslog')[0].innerHTML = "";
  $('#netstat')[0].innerHTML = "";

  addNode();
  addEdge();
  updateNode();
}
