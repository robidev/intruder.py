var nodes, edges, network, socket;

$(document).ready(function() {
	//add tabs
	$("#hostlogtab").dynatabs({
		tabBodyID : "hostlogbody",
		showCloseBtn : true,
	});

  namespace = '';
  socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

  /* register events from server */

  socket.on('info_event', function (type, data) {
    //event gets called from server when info data is updated, so update the info tab
    //type = {ps, syslog, netstat};
    //write data
    $('#ps')[0].innerHTML = "";
    $('#syslog')[0].innerHTML = "";
    $('#netstat')[0].innerHTML = "";
  });

  socket.on('log_event', function (host, data, clear) {
    //event gets called from server when new log events are generated, and add them to the log tab
    //if clear is set, all log data is cleared before adding the new data
    //if host is not known, add the host
  });

  socket.on('select_tab_event', function (host_index) {
    //event gets called from server when the tab-focus should be changed
    var tab = $('#hostlogtab.tabs');
    var len = $('#hostlogtab.tabs')[0].children.length;
    var href = $('#hostlogtab.tabs')[0].children[host_index].children[0];
    var event = $.Event("click");
    event.data = {ahref:"",tab:""};
    event.data.ahref = href;
    event.data.tab = tab;
    $("#hostlogtab").showTab(event);
  });

  socket.on('add_hosts_event', function (hosts, edges, apearance) {
    //event gets called from server when new hosts are discovered, and should be added to the vis.js diagram
    addNode();
    addEdge();
    addNewStaticTab();
  });

  socket.on('update_hosts_event', function (hosts, apearance) {
    //event gets called from server when the host apearance should be updated in the vis.js diagram
    updateNode();
  });

  socket.on('remove_hosts_event', function (hosts) {
    //event gets called from server when hosts should be removed from the vis.js diagram
  });

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
        nodes.add({ id: '4', label: 'PC4', image: 'static/img/pc.png', shape: 'image', font: '12px Arial white'});
    }
    catch (err) {
        alert(err);
    }
}

function updateNode() {
    try {
        nodes.update({
            id: '1',
            image: 'static/img/pc2.png'
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
        {id: '1', label: 'Node 1', image: 'static/img/pc.png', shape: 'image', font: '12px Arial white'},
        {id: '2', label: 'Node 2', image: 'static/img/pc.png', shape: 'image', font: '12px Arial white'},
        {id: '3', label: 'Node 3', image: 'static/img/pc.png', shape: 'image', font: '12px Arial white'},
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

}

/********************************************************/
/*             socket.io calls               */
/********************************************************/

/* emit from client to server */

function get_page_data() {
  socket.emit('get_page_data', {data: ''});
  //call server to tell we want all data, so we can fill the ui (normally done once on full page load/refresh)
}

function get_hosts() {
  socket.emit('get_hosts', {data: ''});
  //call server to tell we want current list of hosts
}

function get_logging_data(host) {
  socket.emit('get_logging_data', {data: ''});
  //call server to tell we want last (100) loglines from 'host'
}

function get_info_data(host) {
  socket.emit('get_info_data', {data: ''});
  //call server to tell we want updated info tab from 'host'
}

function set_focus(host) {
  socket.emit('set_focus', {data: ''});
  //call server to tell we want to change focus, to receive updated info from 'host'
}

