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

  socket.on('info_event', function (data) {
    //event gets called from server when info data is updated, so update the info tab
    //write data
    var tp = data['type'];
    if(tp == '0'){
        $('#ps')[0].innerHTML = data['data'];
    }
    if(tp == '1'){
        $('#syslog')[0].innerHTML = data['data'];
    }
    if(tp == '2'){
        $('#netstat')[0].innerHTML = data['data'];
    }
  });

  socket.on('log_event', function (data) {
    //event gets called from server when new log events are generated, and add them to the log tab
    //if clear is set, all log data is cleared before adding the new data
    //TODO if host is not known, add the host
    var ahref = $("#" + data['host'] + "_tab")[0];
    var key = $(ahref).attr('href');
    if(data['clear'] == '1') {
      $(key)[0].innerHTML = data['data'];  
    }
    else {
      $(key)[0].innerHTML += data['data'];
    }
    //$(key).id = "ggg";
    //href.attr('href').show()
  });

  socket.on('select_tab_event', function (data) {
    //event gets called from server when the tab-focus should be changed
    var tab = $('#hostlogtab.tabs');
    var ahref;
    if(data['host_index']){
      var integer = parseInt(data['host_index'], 10);
      ahref = $('#hostlogtab.tabs')[0].children[integer].children[0];
    }
    else if(data['host_name']){
      ahref = $("#" + data['host_name'] + "_tab")[0];
    }
    selectTabByHref(tab, ahref);
  });

  socket.on('add_hosts_event', function (data) {
    //event gets called from server when new hosts are discovered, and should be added to the vis.js diagram
    if(addNode(data['hosts'], data['apearance']) != 0) {
      return;//if we cannot ad the host, dont try to add the rest
    }

    if(data['edges'] && data['edges']['from'] && data['edges']['to']) {
      addEdge(data['hosts'], data['edges']['from'], data['edges']['to']);
    } 
    
    if (addNewStaticTab(data['hosts']) >= 0) {
      //choose the tab
      var tab = $('#hostlogtab.tabs');
      var ahref = $("#" + data['hosts'] + "_tab")[0];
      selectTabByHref(tab, ahref);
    }
  });

  socket.on('update_hosts_event', function (data) {
    //event gets called from server when the host apearance should be updated in the vis.js diagram
    if(data['edges'] && data['edges']['from'] && data['edges']['to']) {
      addEdge(data['hosts'], data['edges']['from'], data['edges']['to']);
    }
    if(data['apearance']){
      updateNode(data['hosts'], data['apearance']);
    }
  });

  socket.on('remove_hosts_event', function (data) {
    //event gets called from server when hosts should be removed from the vis.js diagram
    removeNode(data['hosts']);
  });

});

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

function get_logging_data() {
  socket.emit('get_logging_data', {data: ''});
  //call server to tell we want last (100) loglines from 'host'
}

function get_info_data() {
  socket.emit('get_info_data', {data: ''});
  //call server to tell we want updated info tab from 'host'
}

function set_focus() {
  socket.emit('set_focus', {data: ''});
  //call server to tell we want to change focus, to receive updated info from 'host'
}


/********************************************************/
/*                        UI calls                      */
/********************************************************/
function addNewStaticTab(host)
{
  var ret = 0;
  if($("#" + host + "_tab").length) {
    return 1;//tab exists
  }

  $.addDynaTab({
    tabID : 'hostlogtab',
    type : 'html',
    html : 'empty',
    tabTitle : host
  });

  //add hostname to button-id
  try {
    var len = $('#hostlogtab.tabs')[0].children.length;
    var ahref = $('#hostlogtab.tabs')[0].children[len-1].children[0];
    ahref.id = host + "_tab";
  }
  catch (err) {
    alert(err);
    ret = -1;
  }
  return ret;
}

function selectTabByHref(tab, ahref)
{
  var ret = 0;
  try {
    var event = $.Event("click");
    event.data = {ahref:"",tab:""};
    event.data.ahref = ahref;
    event.data.tab = tab;
    $("#hostlogtab").showTab(event);
  }
  catch (err) {
    alert(err);
    ret = -1;
  }
  return ret;
}


function addNode(host, appearance) {
  var img;
  var ret = 0;
  if(appearance == '1') {
      img = 'static/img/pc.png';
  }
  else{
      img = 'static/img/pc2.png';
  }
  try {
      nodes.add({ id: host + "_node", label: host, image: img, shape: 'image', font: '12px Arial white'});
  }
  catch (err) {
      alert(err);
      ret = -1;
  }
  return ret;
}

function updateNode(host, appearance) {
  var img;
  var ret = 0;
  if(appearance == '1') {
      img = 'static/img/pc.png';
  }
  else{
      img = 'static/img/pc2.png';
  }
  try {
      nodes.update({
          id: host + "_node",
          image: img
      });
  }
  catch (err) {
      alert(err);
      ret = -1;
  }
  return ret;
}

function addEdge(id, from, to) {
  var ret = 0;
  try {
      edges.add({ id: id + "_edge", from: from + "_node", to: to + "_node"});
  }
  catch (err) {
      alert(err);
      ret = -1;
  }
  return ret;
}

function removeNode(host) {
  var ret = 0;
  try {
      nodes.remove({id: host + "_node"});
  }
  catch (err) {
    alert(err);
    ret = -1;
  }
  return ret;
}

function removeEdge(id) {
  var ret = 0;
  try {
      edges.remove({id: id + "_edge"});
  }
  catch (err) {
    alert(err);
    ret = -1;
  }
  return ret;
}

function draw() {
  // create an array with nodes
  nodes = new vis.DataSet();
  //nodes.add({ id: 'localhost_node', label: 'localhost', image: 'static/img/pc.png', shape: 'image', font: '12px Arial white'});
  // create an array with edges
  edges = new vis.DataSet();

  // create a network
  var container = document.getElementById('network');
  var data = {
      nodes: nodes,
      edges: edges
  };
  var options = {};
  network = new vis.Network(container, data, options);

  /*network.on("click", function (params) {
      params.event = "[original event]";
      //alert('Click event:' + JSON.stringify(params, null, 4));
      //console.log('click event, getNodeAt returns: ' + this.getNodeAt(params.pointer.DOM));
  });*/
}


