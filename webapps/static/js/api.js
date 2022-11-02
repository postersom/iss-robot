var countTest = 0;
var countFail = 0;
var countFailing = 0;
var countAborted = 0;
var countPass = 0;
var currentStation = "";
var milliseconds = 5000;
var myInterval;

var versionIP;

function isInteraction(slot,ip,serialnumber){
	//strobe.gif
	
	var ip_local = $('#ip_local').val();
	$.ajax({
	  url: "http://"+ip_local+":8008/getInteraction?ip="+ip+"&sn="+serialnumber
	  //url: "http://10.196.11.137:8008/getInteraction?ip="+ip+"&sn="+sn
      //url: "http://localhost/ISS-Mockup/jsonData",  
	  //async: false
	}).done(function(json) {
		var countJson = JSON.stringify(json);

			if(countJson != "\"{}\""){
				console.log("5555");

				//$("#"+interAc).html("<img src=\"Images/strobe.gif\" width=\"16\" height=\"16\" alt=alert />");
				$("#"+serialnumber).html("<img style=\"float:right;margin-top:10px;margin-right:10px;\" src=\"Images/strobe.gif\" width=\"27\" height=\"27\"/>");

			}
	});
}

/* parameter
/* 	- station 
*/
function getUUT(){

	console.log("getUUT");
	var ip_local = $('#ip_local').val();
    
    var UserType = $("#userType").val();
	console.log("UserType"+UserType);
	$.ajax({
	  url: "http://"+ip_local+":8008/getUUT?station="+sessionStorage.getItem("station_ses")
		//url: "http://10.196.11.137:8008/getUUT?station="+sessionStorage.getItem("station_ses")
      //url: "http://localhost:8080/iss/jsonData",  
	  //async: false
	}).done(function(json) {
	//var json = "\"{"1": {"slot": "A02", "status": "New", "nccode": "", "logIP": "10.196.11.218", "serialnumber": "-", "batchid": "4", "reason": "", "station": "REGRESSION", "location": "", "server_ip": "10.196.11.142", "time": "-", "part": "", "test_id": "362", "operation": "REGRESSION", "unit": "-"}, "0": {"slot": "A01", "status": "Aborted", "nccode": "Unknown", "logIP": "10.196.11.218", "serialnumber": "TEST3", "batchid": "4", "reason": "null", "station": "REGRESSION", "location": "A01-D [1]", "server_ip": "10.196.11.142", "time": "0:06:13", "part": "", "test_id": "361", "operation": "REGRESSION", "unit": "TEST3-D"}, "3": {"slot": "A04", "status": "Aborted", "nccode": "-", "logIP": "10.196.11.218", "serialnumber": "TEST4", "batchid": "4", "reason": "Aborted by user.", "station": "REGRESSION", "location": "A04-D [1]", "server_ip": "10.196.11.142", "time": "0:02:25", "part": "", "test_id": "364", "operation": "REGRESSION", "unit": "TEST4-D"}, "2": {"slot": "A03", "status": "Aborted", "nccode": "Unknown", "logIP": "10.196.11.218", "serialnumber": "TEST2", "batchid": "4", "reason": "Unit execution engine instance requested to abort", "station": "REGRESSION", "location": "A03-D [1]", "server_ip": "10.196.11.142", "time": "0:00:25", "part": "", "test_id": "363", "operation": "REGRESSION", "unit": "TEST2-D"}}\";
		var data = JSON.parse(json);
		var uutData = "";
		$.each(data, function (key, value) {
			var status = value.status;
			var slot = value.slot;
			var serialnumber = value.serialnumber;
			var station = value.station;
			var time = value.time;
			var part = value.part;
			var test_id = value.test_id;
            var slotCom = value.slot;
            //Use in view node $ delivery list
            var diskIp = value.server_ip;
            
            //Use in scan-in
            var logIp = value.logIP;
            var operation = value.operation;
            var batchId = value.batchid;
            var operator_id = "";
            var test_id = value.test_id
            var lock = value.lock
            var commentTxt = value.comment;
            var comment_lock = value.comment_lock;
            var comment_re = value.comment_re;
            var release = value.release;
            var test_ip = value.server_ip;
            
            if(status == "Testing"){
                var color_h = "#EFC700";
                var color_b = "#EFC700";
            }else if(status == "Passes"){
                var color_h = "#007727";
                var color_b = "#009933";
            }else if(status == "Failed"){
                var color_h = "#C40101";
                var color_b = "#FF0000";
            }else if(status == "Aborted"){
                var color_h = "#D88200";
                var color_b = "#FF9900";
            }else if(status == "Failing"){
                var color_h = "#660020";
                var color_b = "#990033";
            }else if(status == "New"){
                var color_h = "#CCCCCC";
                var color_b = "#EFEFEF";
            }else if(status == "-"){
                var color_h = "#CCCCCC";
                var color_b = "#EFEFEF";
            }else if(status == "Scanning"){
                var color_h = "#B2C24E";
                var color_b = "#B2C24E";
            }else if(status == "Deleting" || status == "Checking out"){
                var color_h = "#3DA8CC";
                var color_b = "#3DA8CC";
            }else if(status == "Aborting"){
                var color_h = "#CC803D";
                var color_b = "#CC803D";
            }else if(status == "Used"){
                var color_h = "#CCCCCC";
                var color_b = "#CCCCCC";
            }
            if(station =="burn-in"){
				
				
				if(status == "-"){	
					uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#444">'+
					'<div class="panel" style="width:100%;margin-bottom:0;">'+
						'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
							'<div class="row">'+
								'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
								'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
									'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
								'</div>'+
							'</div>'+
						'</div>'+
						' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_h+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
							'<div style="text-align:left;">'+
								'<span style="font-size:16px;margin:5px;color:'+color_h+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
							'</div>'+
							'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
						'</div>'+
						'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_h+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
							'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
							'<div class="row">'+
								'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
									'<a class="comment" style="display:block; color:#444; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
								'</div>'+ 
							'</div>'+
						'</div>'+
						'</div>'+
					'</div>'+
				'</div>';
				}else if(status == "New"){	
					uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#444">'+
					'<div class="panel" style="width:100%;margin-bottom:0;">'+
						'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
							'<div class="row">'+
								'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
								'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
									'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
								'</div>'+
							'</div>'+
						'</div>'+
						' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_h+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
							'<div style="text-align:left;">'+
								'<span style="font-size:16px;margin:5px;color:'+color_h+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
							'</div>'+
							'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
						'</div>'+
						'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_h+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
							'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
							'<div class="row">'+
								'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
									'<a class="comment" style="display:block; color:#444; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
								'</div>'+ 
							'</div>'+
						'</div>'+
						'</div>'+
					'</div>'+
				'</div>';
					
				}else if(status == "Aborted"){
	
					countAborted++;
					uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+ 
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
				}else if(status == "Failed"){
					countFail++;
					uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
					'<div class="panel" style="width:100%;margin-bottom:0;">'+
						'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
							'<div class="row">'+
								'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
								'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
									'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
								'</div>'+
							'</div>'+
						'</div>'+
						' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
							'<div style="text-align:left;">'+
								'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
							'</div>'+
							'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
						'</div>'+
						'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
							'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
							'<div class="row">'+
								'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
									'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
								'</div>'+ 
							'</div>'+
						'</div>'+
						'</div>'+
					'</div>'+
				'</div>';
					
				}else if(status == "Passes"){
					countPass++;
					uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
					'<div class="panel" style="width:100%;margin-bottom:0;">'+
						'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
							'<div class="row">'+
								'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
								'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
									'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
								'</div>'+
							'</div>'+
						'</div>'+
						' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
							'<div style="text-align:left;">'+
								'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
							'</div>'+
							'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
						'</div>'+
						'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
							'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
							'<div class="row">'+
								'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
									'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
								'</div>'+ 
							'</div>'+
						'</div>'+
						'</div>'+
					'</div>'+
				'</div>';

				}else if(status == "Testing"){
					countTest++;
					uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
					'<div class="panel" style="width:100%;margin-bottom:0;">'+
						'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
							'<div class="row">'+
								'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
								'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
									'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
								'</div>'+
							'</div>'+
						'</div>'+
						' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
							'<div style="text-align:left;">'+
								'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
							'</div>'+
							'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
						'</div>'+
						'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
							'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
							'<div class="row">'+
								'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
									'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
								'</div>'+ 
							'</div>'+
						'</div>'+
						'</div>'+
					'</div>'+
				'</div>';
					
				}else if(status == "Failing"){
					countFailing++;
					uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
					'<div class="panel" style="width:100%;margin-bottom:0;">'+
						'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
							'<div class="row">'+
								'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
								'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
									'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
								'</div>'+
							'</div>'+
						'</div>'+
						' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
							'<div style="text-align:left;">'+
								'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
							'</div>'+
							'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
						'</div>'+
						'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
							'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
							'<div class="row">'+
								'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
									'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
								'</div>'+ 
							'</div>'+
						'</div>'+
						'</div>'+
					'</div>'+
				'</div>';   
					
				}else if(status == "Scanning" || status == "Aborting" || status == "Deleting" || status == "Checking out"){	
					uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
					'<div class="panel" style="width:100%;margin-bottom:0;">'+
						'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
							'<div class="row">'+
								'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
								'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
									'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
								'</div>'+
							'</div>'+
						'</div>'+
						' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
							'<div style="text-align:left;">'+
								'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><img style=\"float:right;margin-top:10px;margin-right:10px;\" src=\"Images/ing.gif\" width=\"27\" height=\"27\"/></span>'+
							'</div>'+
							'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
						'</div>'+
						'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
							'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span style="float:right;margin-right:15px;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>-->'+
							'<div class="row">'+
								'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
									'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
								'</div>'+ 
							'</div>'+
						'</div>'+
						'</div>'+
					'</div>'+
				'</div>';
					
				}else if(status == "Used"){	
					uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#444">'+
					'<div class="panel" style="width:100%;margin-bottom:0;">'+
						'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
							'<div class="row">'+
								'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
								'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
									'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
								'</div>'+
							'</div>'+
						'</div>'+
						' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
							'<div style="text-align:left;">'+
								'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
							'</div>'+
							'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
						'</div>'+
						'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
							'<div class="row">'+
								'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
									'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
								'</div>'+ 
							'</div>'+
						'</div>'+
						'</div>'+
					'</div>'+
				'</div>';
				} 

			}else{
		
				if(UserType == "6"){
					if(status == "-"){	
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#444">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_h+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_h+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_h+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:#444; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:'+color_h+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button id="abortSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirm" data-id="'+slot+'||'+commentTxt+'" onmousedown=setAbortData("'+test_id+'")>Force Abort</button><button id="deliverySN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmDelivery" data-id="'+slot+'||'+commentTxt+'" onmousedown=setDeliveryData("'+test_id+'","'+diskIp+'","'+slot+'","'+serialnumber+'")>Force Delete</button><button id="checkoutSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmCheckOut" data-id="'+slot+'||'+commentTxt+'" onmousedown=setCheckOutData("'+test_id+'","'+diskIp+'","'+slot+'","'+serialnumber+'")>Force CheckOut</button><button id="resetSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmClear" data-id="'+slot+'||'+commentTxt+'" onmousedown=setClearData("'+test_id+'")>Force Clear</button></div>\'><span style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
						
					}else if(status == "New"){	
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#444">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_h+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_h+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_h+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:#444; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:'+color_h+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button id="abortSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirm" data-id="'+slot+'||'+commentTxt+'" onmousedown=setAbortData("'+test_id+'")>Force Abort</button><button id="deliverySN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmDelivery" data-id="'+slot+'||'+commentTxt+'" onmousedown=setDeliveryData("'+test_id+'","'+diskIp+'","'+slot+'","'+serialnumber+'")>Force Delete</button><button id="checkoutSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmCheckOut" data-id="'+slot+'||'+commentTxt+'" onmousedown=setCheckOutData("'+test_id+'","'+diskIp+'","'+slot+'","'+serialnumber+'")>Force CheckOut</button><button id="resetSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmClear" data-id="'+slot+'||'+commentTxt+'" onmousedown=setClearData("'+test_id+'")>Force Clear</button></div>\'><span style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
						
					}else if(status == "Aborted"){
		
						countAborted++;
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:'+color_b+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button id="abortSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirm" data-id="'+slot+'||'+commentTxt+'" onmousedown=abortFunc("'+diskIp+'","'+slot+'","'+serialnumber+'")>Force Abort</button><button id="deliverySN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmDelivery" data-id="'+slot+'||'+commentTxt+'" onmousedown=setDeliveryData("'+test_id+'","'+diskIp+'","'+slot+'","'+serialnumber+'")>Force Delete</button><button id="checkoutSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmCheckOut" data-id="'+slot+'||'+commentTxt+'" onmousedown=setCheckOutData("'+test_id+'","'+diskIp+'","'+slot+'","'+serialnumber+'")>Force CheckOut</button><button id="resetSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmClear" data-id="'+slot+'||'+commentTxt+'" onmousedown=setClearData("'+test_id+'")>Force Clear</button></div>\'><span  style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
						
					}else if(status == "Failed"){
						countFail++;
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:'+color_b+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose"name="'+serialnumber+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button id="abortSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirm" data-id="'+slot+'||'+commentTxt+'" onmousedown=abortFunc("'+diskIp+'","'+slot+'","'+serialnumber+'")>Force Abort</button><button id="deliverySN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmDelivery" data-id="'+slot+'||'+commentTxt+'" onmousedown=setDeliveryData("'+test_id+'","'+diskIp+'","'+slot+'","'+serialnumber+'")>Force Delete</button><button id="checkoutSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmCheckOut" data-id="'+slot+'||'+commentTxt+'" onmousedown=setCheckOutData("'+test_id+'","'+diskIp+'","'+slot+'","'+serialnumber+'")>Force CheckOut</button><button id="resetSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmClear" data-id="'+slot+'||'+commentTxt+'" onmousedown=setClearData("'+test_id+'")>Force Clear</button></div>\'><span  style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
						
					}else if(status == "Passes"){
						countPass++;
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:'+color_b+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button disabled id="abortSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirm" data-id="'+slot+'||'+commentTxt+'" onmousedown=abortFunc("'+diskIp+'","'+slot+'","'+serialnumber+'")>Force Abort</button><button id="deliverySN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmDelivery" data-id="'+slot+'||'+commentTxt+'" onmousedown=setDeliveryData("'+test_id+'","'+diskIp+'","'+slot+'","'+serialnumber+'")>Force Delete</button><button id="checkoutSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmCheckOut" data-id="'+slot+'||'+commentTxt+'" onmousedown=setCheckOutData("'+test_id+'","'+diskIp+'","'+slot+'","'+serialnumber+'")>Force CheckOut</button><button id="resetSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmClear" data-id="'+slot+'||'+commentTxt+'" onmousedown=setClearData("'+test_id+'")>Force Clear</button></div>\'><span  style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
					
					}else if(status == "Testing"){
						countTest++;
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:'+color_b+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button id="abortSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirm" data-id="'+slot+'||'+commentTxt+'" onmousedown=abortFunc("'+diskIp+'","'+slot+'","'+serialnumber+'")>Force Abort</button><button id="deliverySN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmDelivery" data-id="'+slot+'||'+commentTxt+'" onmousedown=setDeliveryData("'+test_id+'","'+diskIp+'","'+slot+'","'+serialnumber+'")>Force Delete</button><button id="checkoutSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmCheckOut" data-id="'+slot+'||'+commentTxt+'" onmousedown=setCheckOutData("'+test_id+'","'+diskIp+'","'+slot+'","'+serialnumber+'")>Force CheckOut</button><button id="resetSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmClear" data-id="'+slot+'||'+commentTxt+'" onmousedown=setClearData("'+test_id+'")>Force Clear</button></div>\'><span  style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
						
					}else if(status == "Failing"){
						countFailing++;
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:'+color_b+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button id="abortSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirm" data-id="'+slot+'||'+commentTxt+'" onmousedown=abortFunc("'+diskIp+'","'+slot+'","'+serialnumber+'")>Force Abort</button><button id="deliverySN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmDelivery" data-id="'+slot+'||'+commentTxt+'" onmousedown=setDeliveryData("'+test_id+'","'+diskIp+'","'+slot+'","'+serialnumber+'")>Force Delete</button><button id="checkoutSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmCheckOut" data-id="'+slot+'||'+commentTxt+'" onmousedown=setCheckOutData("'+test_id+'","'+diskIp+'","'+slot+'","'+serialnumber+'")>Force CheckOut</button><button id="resetSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmClear" data-id="'+slot+'||'+commentTxt+'" onmousedown=setClearData("'+test_id+'")>Force Clear</button></div>\'><span  style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';  
						
					}else if(status == "Scanning" || status == "Aborting" || status == "Deleting" || status == "Checking out"){	
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><img style=\"float:right;margin-top:10px;margin-right:10px;\" src=\"Images/ing.gif\" width=\"27\" height=\"27\"/></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2 stating" style="text-align:right;">'+
										'<a style="color:'+color_b+';" tabindex="0" role="button" class="aclose" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom" data-html="true" data-content=\'<div class="list-group"><button id="abortSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirm" data-id="'+slot+'||'+commentTxt+'" onmousedown=abortFunc("'+diskIp+'","'+slot+'","'+serialnumber+'")>Force Abort</button><button id="deliverySN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmDelivery" data-id="'+slot+'||'+commentTxt+'" onmousedown=setDeliveryData("'+test_id+'","'+diskIp+'","'+slot+'","'+serialnumber+'")>Force Delete</button><button id="checkoutSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmCheckOut" data-id="'+slot+'||'+commentTxt+'" onmousedown=setCheckOutData("'+test_id+'","'+diskIp+'","'+slot+'","'+serialnumber+'")>Force CheckOut</button><button id="resetSN" href="#" class="list-group-item" data-toggle="modal" data-target="#myConfirmClear" data-id="'+slot+'||'+commentTxt+'" onmousedown=setClearData("'+test_id+'")>Force Clear</button></div>\'><span style="float:right;margin-right:15px;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
						
					}else if(status == "Used"){	
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#444">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2 stating" style="text-align:right;">'+
										'<a style="color:#666;" tabindex="0" role="button" class="aclose" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom" data-html="true" data-content=\'<div class="list-group"><button disabled href="#" class="list-group-item" style="color:#999999">View</button><button href="#" class="list-group-item" data-toggle="modal" data-target="#myModal" data-id="'+slot+'||'+commentTxt+'" onmousedown=scanin("'+operation+'","'+operator_id+'","'+batchId+'","'+serialnumber+'","'+test_id+'","'+logIp+'","'+diskIp+'","'+commentTxt+'")>Scan-in</button><button disabled href="#" class="list-group-item" style="color:#999999" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button disabled href="#" style="color:#999999" class="list-group-item">Delivery</button><button disabled style="color:#999999" href="#" class="list-group-item">Interaction</button></div>\'><span style="float:right;margin-right:15px;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
						
					}

				}else if(UserType == "7"){
					if(status == "-"){	
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#444">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_h+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_h+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_h+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:#444; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2 stating" style="text-align:right;">'+
										'<a style="color:#444; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" at="'+comment_lock+'" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group" id="lockCom"><button id="locksi" href="#" class="list-group-item" data-toggle="modal" data-target="#modalComment" onmousedown=setComment("'+test_id+'") data-id="'+slotCom+'||'+commentTxt+'">Comment</button></div>\'><span  style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
					}else if(status == "New"){	
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#444">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_h+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_h+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_h+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:#444; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:#444; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" at="'+comment_lock+'" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group" id="lockCom"><button id="locksi" href="#" class="list-group-item" data-toggle="modal" data-target="#modalComment" onmousedown=setComment("'+test_id+'") data-id="'+slotCom+'||'+commentTxt+'">Comment</button></div>\'><span  style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
						
					}else if(status == "Aborted"){
		
						countAborted++;
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
							'<div class="panel" style="width:100%;margin-bottom:0;">'+
								'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
									'<div class="row">'+
										'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
										'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
											'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
										'</div>'+
									'</div>'+
								'</div>'+
								' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
									'<div style="text-align:left;">'+
										'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
									'</div>'+
									'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
								'</div>'+
								'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
									'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
									'<div class="row">'+
										'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
											'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
										'</div>'+
										'<div class="col-md-2" style="text-align:right;">'+
											'<a style="color:'+color_b+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" at="'+comment_lock+'" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group" id="lockCom"><button id="locksi" href="#" class="list-group-item" data-toggle="modal" data-target="#modalComment" onmousedown=setComment("'+test_id+'") data-id="'+slotCom+'||'+commentTxt+'">Comment</button></div>\'><span  style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
										'</div>'+
									'</div>'+
								'</div>'+
								'</div>'+
							'</div>'+
						'</div>';
					}else if(status == "Failed"){
						countFail++;
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:'+color_b+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" at="'+comment_lock+'" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group" id="lockCom"><button id="locksi" href="#" class="list-group-item" data-toggle="modal" data-target="#modalComment" onmousedown=setComment("'+test_id+'") data-id="'+slotCom+'||'+commentTxt+'">Comment</button></div>\'><span  style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
						
					}else if(status == "Passes"){
						countPass++;
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:'+color_b+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" at="'+comment_lock+'" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group" id="lockCom"><button id="locksi" href="#" class="list-group-item" data-toggle="modal" data-target="#modalComment" onmousedown=setComment("'+test_id+'") data-id="'+slotCom+'||'+commentTxt+'">Comment</button></div>\'><span  style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';

					}else if(status == "Testing"){
						countTest++;
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:'+color_b+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" at="'+comment_lock+'" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group" id="lockCom"><button id="locksi" href="#" class="list-group-item" data-toggle="modal" data-target="#modalComment" onmousedown=setComment("'+test_id+'") data-id="'+slotCom+'||'+commentTxt+'">Comment</button></div>\'><span  style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
						
					}else if(status == "Failing"){
						countFailing++;
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:'+color_b+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" at="'+comment_lock+'" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group" id="lockCom"><button id="locksi" href="#" class="list-group-item" data-toggle="modal" data-target="#modalComment" onmousedown=setComment("'+test_id+'") data-id="'+slotCom+'||'+commentTxt+'">Comment</button></div>\'><span  style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';  
						
					}else if(status == "Scanning" || status == "Aborting" || status == "Deleting" || status == "Checking out"){	
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><img style=\"float:right;margin-top:10px;margin-right:10px;\" src=\"Images/ing.gif\" width=\"27\" height=\"27\"/></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2 stating" style="text-align:right;">'+
										'<a style="color:'+color_b+';" tabindex="0" role="button" class="aclose" at="'+comment_lock+'" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom" data-html="true" data-content=\'<div class="list-group"><button disabled href="#" class="list-group-item" style="color:#999999">View</button><button disabled href="#" class="list-group-item" style="color:#999999" data-toggle="modal" data-target="#myModal" data-id="'+slot+'">Scan-in</button><button disabled href="#" class="list-group-item" style="color:#999999" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button disabled href="#" style="color:#999999" class="list-group-item">Delivery</button><button disabled style="color:#999999" href="#" class="list-group-item">Interaction</button></div>\'><span style="float:right;margin-right:15px;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
						
					}else if(status == "Used"){	
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#444">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2 stating" style="text-align:right;">'+
										'<a style="color:#666;" tabindex="0" role="button" class="aclose" at="'+comment_lock+'" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom" data-html="true" data-content=\'<div class="list-group" id="lockCom"><button disabled href="#" class="list-group-item" data-toggle="modal" data-target="#modalComment" data-id="'+slotCom+'||'+commentTxt+'">Comment</button></div>\'><span style="float:right;margin-right:15px;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
					}
					
					

				}else{
				
					if(status == "-"){	
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#444">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_h+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_h+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_h+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:#444; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2 stating" style="text-align:right;">'+
										'<a style="color:'+color_h+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" at="'+lock+'" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button disabled href="#" class="list-group-item" style="color:#999999">View</button><button id="locksi" href="#" class="list-group-item" data-toggle="modal" data-target="#myModal" data-id="'+slot+'||'+commentTxt+'" onmousedown=scanin("'+operation+'","'+operator_id+'","'+batchId+'","'+serialnumber+'","'+test_id+'","'+logIp+'","'+diskIp+'","'+commentTxt+'")>Scan-in</button><button disabled href="#" class="list-group-item" style="color:#999999" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button disabled href="#" style="color:#999999" class="list-group-item">Delivery</button><button disabled style="color:#999999" href="#" class="list-group-item">Interaction</button></div>\'><span style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
					}else if(status == "New"){	
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#444">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_h+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_h+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_h+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:#444; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:#444; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" at="'+lock+'" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button disabled href="#" class="list-group-item" style="color:#999999">View</button><button id="locksi" href="#" class="list-group-item" data-toggle="modal" data-target="#myModal" data-id="'+slot+'||'+commentTxt+'" onmousedown=scanin("'+operation+'","'+operator_id+'","'+batchId+'","'+serialnumber+'","'+test_id+'","'+logIp+'","'+diskIp+'","'+commentTxt+'")>Scan-in</button><button disabled href="#" class="list-group-item" style="color:#999999" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button disabled href="#" style="color:#999999" class="list-group-item">Delivery</button><button disabled style="color:#999999" href="#" class="list-group-item">Interaction</button></div>\'><span style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
						
					}else if(status == "Aborted"){
		
						countAborted++;
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
							'<div class="panel" style="width:100%;margin-bottom:0;">'+
								'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
									'<div class="row">'+
										'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
										'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
											'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
										'</div>'+
									'</div>'+
								'</div>'+
								' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
									'<div style="text-align:left;">'+
										'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
									'</div>'+
									'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
								'</div>'+
								'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
									'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
									'<div class="row">'+
										'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
											'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
										'</div>'+
										'<div class="col-md-2" style="text-align:right;">'+
											'<a style="color:'+color_b+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span  style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
										'</div>'+
									'</div>'+
								'</div>'+
								'</div>'+
							'</div>'+
						'</div>';
					}else if(status == "Failed"){
						countFail++;
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:'+color_b+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span  style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
						
					}else if(status == "Passes"){
						countPass++;
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:'+color_b+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span  style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';

					}else if(status == "Testing"){
						countTest++;
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:'+color_b+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button class="list-group-item" data-toggle="modal" data-target="#myConfirm" data-id="'+slot+'||'+commentTxt+'" onmousedown=abortFunc("'+diskIp+'","'+slot+'","'+serialnumber+'")>Abort</button><button disabled style="color:#999999" class="list-group-item">Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span  style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
						
					}else if(status == "Failing"){
						countFailing++;
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span class="glyphicon glyphicon-th-list" aria-hidden="true"></span><span style="float:left;color:#fff">'+time+'</span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2" style="text-align:right;">'+
										'<a style="color:'+color_b+'; padding:0;float:right;margin-right:15px;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button class="list-group-item" data-toggle="modal" data-target="#myConfirm" data-id="'+slot+'||'+commentTxt+'" onmousedown=abortFunc("'+diskIp+'","'+slot+'","'+serialnumber+'")>Abort</button><button disabled style="color:#999999" class="list-group-item">Delivery</button><button data-id="'+slot+'||'+commentTxt+'" class="list-group-item" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span style="float:right;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';   
						
					}else if(status == "Scanning" || status == "Aborting" || status == "Deleting" || status == "Checking out"){	
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#ffffff">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><img style=\"float:right;margin-top:10px;margin-right:10px;\" src=\"Images/ing.gif\" width=\"27\" height=\"27\"/></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<!--<a style="color:#fff;" tabindex="0" role="button" class="aclose" at="'+lock+'" data-toggle="popover" data-placement="bottom"  data-html="true" data-content=\'<div class="list-group"><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("viewNodeTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>View</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myModal">Scan-in</button><button disabled style="color:#999999" class="list-group-item" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("deliveryTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Delivery</button><button class="list-group-item" data-id="'+slot+'||'+commentTxt+'" onmousedown=getList("interactionTab","'+diskIp+'","'+serialnumber+'","'+status+'","'+test_id+'","'+slot+'")>Interaction</button></div>\'><span style="float:right;margin-right:15px;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>-->'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2 stating" style="text-align:right;">'+
										'<a style="color:'+color_b+';" tabindex="0" role="button" class="aclose" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom" data-html="true" data-content=\'<div class="list-group"><button disabled href="#" class="list-group-item" style="color:#999999">View</button><button disabled href="#" class="list-group-item" style="color:#999999" data-toggle="modal" data-target="#myModal" data-id="'+slot+'">Scan-in</button><button disabled href="#" class="list-group-item" style="color:#999999" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button disabled href="#" style="color:#999999" class="list-group-item">Delivery</button><button disabled style="color:#999999" href="#" class="list-group-item">Interaction</button></div>\'><span style="float:right;margin-right:15px;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
						
					}else if(status == "Used"){	
						uutData = uutData + '<div class="col-sm-3" style="padding:0;color:#444">'+
						'<div class="panel" style="width:100%;margin-bottom:0;">'+
							'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
								'<div class="row">'+
									'<div class="col-md-6" style="font-size:24px;font-weight:bold;" id="'+slot+'">'+slot+'</div>'+
									'<div class="col-md-6" style="font-size:12px;font-weight:bold;text-align:right;">'+
										'<span style="font-weight: bold;font-size:12px;">'+status+'</span><br><span style="font-weight: normal;font-size:12px;">'+time+'</span>'+
									'</div>'+
								'</div>'+
							'</div>'+
							' <div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-style: 3px solid; border-radius: 3px;">'+
								'<div style="text-align:left;">'+
									'<span style="font-size:16px;margin:5px;color:'+color_b+';"><b>'+serialnumber+'</a></b><span id="'+serialnumber+'"></span>'+
								'</div>'+
								'<div style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:12px;margin:5px;color:#000;float:center;">'+part+'</p></div>'+
							'</div>'+
							'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-style: 3px solid; border-radius: 3px;"><a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:11px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'"> '+commentTxt+'</a>'+
								'<div class="row">'+
									'<div class="col-md-10" style="font-size:18px;font-weight:bold;">'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:11px;font-weight:normal; text-align:left; margin:5px; padding:0;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
									'<div class="col-md-2 stating" style="text-align:right;">'+
										'<a style="color:'+color_b+';" tabindex="0" role="button" class="aclose" name="'+serialnumber+'" data-toggle="popover" data-placement="bottom" data-html="true" data-content=\'<div class="list-group"><button disabled href="#" class="list-group-item" style="color:#999999">View</button><button disabled href="#" class="list-group-item" style="color:#999999" data-toggle="modal" data-target="#myModal" data-id="'+slot+'">Scan-in</button><button disabled href="#" class="list-group-item" style="color:#999999" data-toggle="modal" data-target="#myConfirm" onmousedown=setClickedslot("'+slot+'")>Abort</button><button disabled href="#" style="color:#999999" class="list-group-item">Delivery</button><button disabled style="color:#999999" href="#" class="list-group-item">Interaction</button></div>\'><span style="float:right;margin-right:15px;" class="glyphicon glyphicon-th-list" aria-hidden="true"></span></a>'+
									'</div>'+
								'</div>'+
							'</div>'+
							'</div>'+
						'</div>'+
					'</div>';
					}
				}
			}
            
	        $("#operation").val(operation);
	        $("#versionIp").val(versionIp);
	        window.versionIP = diskIp;
	        //var version = $('#diskIp').val();
	    	//var version = document.getElementById("versionIp").value;

	        
		});
		
		//console.log(json);
		$("#uutList").html((uutData));
	    var hideAllPopovers = function() {
	    	
		       $('.aclose').each(function() {
		   
		            $(this).popover('hide');
		        });  

		};
		$(document).on('click', function(e) {
		        hideAllPopovers();   
		});

		$('.aclose').popover({	
	        trigger: 'manual'
	    }).on('click', function(e) {
	    	
			$(".aclose").not(this).popover("hide");
			$(this).popover('show');
			
			 var chkType = $("#userType").val();
	 			console.log("m1"+chkType);
	 			var chkSN = $(this).attr('name');
	 			console.log("chkSN"+chkSN);
	 			
	 			
	 			if(chkType != "6"){
	 				console.log("disable");
	 				$("#resetSN").attr('disabled', true);
	 				$("#resetSN").css('color', '#999999');
	 			}
	 			
	 			console.log("999999"+$(this).attr('at'));
				if($(this).attr('at') == "True"){
					console.log("disableat");
	 				$(".list-group #locksi").attr('disabled', true);
	 				$(".list-group #locksi").css('color', '#999999');
	 				$("#lockCom").attr('disabled', true);
				}
			e.stopPropagation();
			
			
			
		});
        $("#test-counter").html(countTest);
		$("#fail-counter").html(countFail);
		$("#failing-counter").html(countFailing);
		$("#abort-counter").html(countAborted);
		$("#pass-counter").html(countPass);
		
        
        countTest = 0;
        countFail = 0;
        countFailing = 0;
        countAborted = 0;
        countPass = 0;
        
	        $.each(data, function (key, value) {
				var slot = value.slot;
				var serialnumber = value.serialnumber;
	            var diskIp = value.server_ip;
	            if(serialnumber != "-"){
	            	isInteraction(slot,diskIp,serialnumber);
	            }
	        });
	       
	        console.log("versionIp"+versionIP);
	        $.ajax({
	            url: "http://"+ip_local+":8008/getversion?ip="+versionIP+"",
	            //url: "http://10.196.11.137:8008/getversion?ip="+versionIP+"",
	        }).done(function(json) {
	            var data = JSON.parse(json);
	            var uutData = "";
	            $.each(data, function (key, value) {
	                console.log("version"+value);
	                document.getElementById("version").innerHTML = value;
	            });
	        });
	});

}



function radioClear(){
	$(".deleted").attr('checked', false);
	$(".resetBatch").attr('checked', false);
	$(".checkItem").attr('checked', false);
	$("#checkoutAll").attr('checked', false);
	$("#resetAll").attr('checked', false);
	$("#deleteAll").attr('checked', false);
	$("#dtype").val("retest");
	
	$("#commitPost").attr('disabled', false);
    $("#resetPost").attr('disabled', false);
	
	var radioBtns = $('#retestBtn:checked').length ;
	console.log("radioClear-retest"+radioBtns);
	
	if(radioBtns == "0"){ // disabled
		console.log("disable");
    	
	    $("#commitPost").prop("disabled", true);
	    $("#resetPost").prop("disabled", true);
    }else{
    	$("#commitPost").attr("disabled", false);
	    $("#resetPost").attr("disabled", false);
    }
}
function radioClearType(type,disBtn){
	
	console.log("disBtn"+disBtn);
	if(disBtn == false){ // disabled
		console.log("disable");
    	$("#commitPost").attr("disabled", true);
	    $("#resetPost").attr("disabled", true);
    }else{
    	$("#commitPost").prop("disabled", false);
	    $("#resetPost").prop("disabled", false);
    }
	
	if(type=="deleteAll"){
		$(".resetBatch").attr('checked', false);
		$(".checkItem").attr('checked', false);
		$(".deleted").attr('checked', true);
		$(".retest").attr('checked', false);
		
		$("#checkoutAll").attr('checked', false);
		$("#resetAll").attr('checked', false);

	}
	if(type=="checkoutAll"){
		$(".resetBatch").attr('checked', false);
		$(".checkItem").attr('checked', true);
		$(".deleted").attr('checked', false);
		$(".retest").attr('checked', false);
		
		$("#deleteAll").attr('checked', false);
		$("#resetAll").attr('checked', false);

	}
	if(type=="resetAll"){
		$(".deleted").attr('checked', false);
		$(".resetBatch").attr('checked', true);
		$(".checkItem").attr('checked', false);
		$(".retest").attr('checked', false);
		
		$("#deleteAll").attr('checked', false);
		$("#checkoutAll").attr('checked', false);

	}
	console.log("checkboxALL");
}

function setClickedslot(slot){
	$('#clicked_slot').val(slot);
}


function getList(showtab,diskIp,serialnumber,chkStatus,test_id,slot)
{
	$('#clicked_slot').val(slot);
	
	document.getElementById("tablist").style.display = "block";
	$('#tabcontent_id').show();
	
	var User = $("#userType").val();
	document.getElementById("checkoutAll").checked = false;
	
	if(User == "2" || User == "3"){
		document.getElementById("deleteAll").checked = false;
	}
	if(User == "2"){
		document.getElementById("resetAll").checked = false;
	}
	
	var ip_local = $('#ip_local').val();
	console.log("ip_localAPI"+ip_local);
    $("#nodeIP").val(diskIp);
    // node list tab -----------------------------------------------------------------
	$.ajax({
		url: "http://"+ip_local+":8008/getList?ip_core="+diskIp+"&sn="+serialnumber+"&test_id="+test_id+"&location="+slot
		//url: "http://10.196.11.137:8008/getList?ip_core="+diskIp+"&sn="+serialnumber+"&test_id="+test_id
		//url: "http://localhost/ISS-Mockup/jsonData3",
	}).done(function(data) 
	{
		
		if (showtab=="viewNodeTab"){
			
			$("#viewNodeTab").tab('show');
			document.getElementById("node").style.display = "block";
			document.getElementById("delivery").style.display = "none";
			document.getElementById("interaction").style.display = "none";
			
			document.getElementById("allNodeBtn").style.display = "block";
			
			console.log("chkStatus"+chkStatus);
			if(chkStatus == "Aborted" || chkStatus == "Passes" || chkStatus == "Failed"){
				document.getElementById("commitDevButton").style.display = "block";
				document.getElementById("resetDevButton").style.display = "block";

			}else{
				
					document.getElementById("commitDevButton").style.display = "none";
					document.getElementById("resetDevButton").style.display = "none";
				
				
			}
		}

		var json = JSON.parse(data);
		var listnode = "";
		$.each(json, function (key,value){
	
			var location = value.location;
			var status = value.status;
			var sn = value.serialnumber;
			var chassis = value.chassis_sn;
			var operation = value.operation;
			var started = value.started;
			var finished = value.finished;
			var nccode = value.nccode;
			var reason = value.reason;
			
			//console.log("listnode");
			var color ="";
			if(status == "abort" || status == "Aborted"){
				color = "#FF9900";
			}
			else if (status == "fail" || status == "Failed"){
				color = "#FF0000";
			}
			else if (status == "failing" || status == "Failing"){
				color = "#990033";
			}
			else if (status == "testing" || status == "Testing"){
				color = "#DFCF00";
			}
			else{
				color = "#009933";
			}

            listnode = listnode + "<tr><td><a  target=\"_blank\" href=\"http://"+diskIp+":8080/iss/view?type=viewer&unit="+sn+"\">"+location+"</a></td>"+
						     "<td id=\""+status+"\" style=\"color:"+color+";font-weight: bold\">"+status+"</td>"+
						     "<td>"+sn+"</td>"+
						     "<td>"+chassis+"</td>"+
						     "<td>"+operation+"</td>"+
						     "<td>"+started+"</td>"+
						     "<td>"+finished+"</td>"+
						     "<td>"+nccode+"</td>"+
						     "<td>"+reason+"</td></tr>";

           
		});
		$("#bodyNode").html(listnode);
		
		$("html, body").animate({
			scrollTop : $(document).height()
		}, "slow");
		
		clearInterval(myInterval);
		openInterval();
		
	});
	
	// delivery tab ---------------------------------------------------------------
	$.ajax({
		url: "http://"+ip_local+":8008/getDelivery?ip_core="+diskIp+"&sn="+serialnumber+"&test_id="+test_id+"&location="+slot
		//url: "http://10.196.11.137:8008/getDelivery?ip_core="+diskIp+"&sn="+serialnumber+"&test_id="+test_id
		//url: "http://localhost/ISS-Mockup/jsonData2",
	}).done(function(data) 
	{
		
		if (showtab=="deliveryTab"){
			
			$("#deliveryTab").tab('show');
			document.getElementById("node").style.display = "none";
			document.getElementById("delivery").style.display = "block";
			document.getElementById("interaction").style.display = "none";
			
			document.getElementById("allNodeBtn").style.display = "block";
			document.getElementById("commitDevButton").style.display = "block";
			document.getElementById("resetDevButton").style.display = "block";
		}
		var json = JSON.parse(data);
		var deliveryList = "";
		var commitbutton = "";
		var resetbutton = "";
		var ssn = new Array();
		$.each(json, function (key,value){
	
			var location = value.location;
			var status = value.status;
			var sn = value.serialnumber;
			var chassis = value.chassis_sn;
			var operation = value.operation;
			var started = value.started;
			var finished = value.finished;
			var nccode = value.nccode;
			var reason = value.reason;
			var test_id = value.test_id;
			
			ssn.push(sn);
			
			var UserType = $("#userType").val();
			console.log("UserType"+UserType);
			console.log("chkStatusDev"+chkStatus);
			
			if(chkStatus == "Failing" || chkStatus == "Testing"){
				deliveryList = "";
		             
				}else{
					if(UserType == "2"){
						console.log("2222")
					    deliveryList = deliveryList + "<tr><td><a  target=\"_blank\" href=\"http://"+diskIp+":8080/iss/view?type=viewer&unit="+sn+"\">"+location+"</a></td>"+
										 "<td id="+sn_dev+">"+sn+"</td>"+
									     "<td>"+chassis+"</td>"+
									     "<td id="+status+">"+status+"</td>"+
									     "<td>"+nccode+"</td>"+
									     "<td>"+reason+"</td>"+
									     "<input type='hidden' id="+ip_dev+">"+reason+">"+
									     "<td><input type=\"checkbox\"  class=\"checkItem\" onClick=\"radioAll('checkItem')\" disabled  /></td>"+
										 "<td><input type=\"checkbox\"  class=\"deleted\"  onClick=\"radioAll('deleted')\" disabled /></td>"+
									     "<td><input type=\"checkbox\"  class=\"resetBatch\"  onClick= \"radioAll('resetBatch')\" disabled /></td>"+
										 "<td><input type=\"checkbox\" id=\"retestBtn\" class=\"retest\" onClick=\"radioClear()\" value=\""+sn+"\" /></td></tr>";
					}else if(UserType == "3"){
						console.log("333")
					    deliveryList = deliveryList + "<tr><td><a  target=\"_blank\" href=\"http://"+diskIp+":8080/iss/view?type=viewer&unit="+sn+"\">"+location+"</a></td>"+
						 "<td id="+sn_dev+">"+sn+"</td>"+
					     "<td>"+chassis+"</td>"+
					     "<td id="+status+">"+status+"</td>"+
					     "<td>"+nccode+"</td>"+
					     "<td>"+reason+"</td>"+
					     "<input type='hidden' id="+ip_dev+">"+reason+">"+
					     "<td><input type=\"checkbox\"  class=\"checkItem\" onClick=\"radioAll('checkItem')\" disabled  /></td>"+
						 "<td><input type=\"checkbox\"  class=\"deleted\"  onClick=\"radioAll('deleted')\" disabled /></td>";
					}else{
						console.log("eeee")
						deliveryList = deliveryList + "<tr><td><a  target=\"_blank\" href=\"http://"+diskIp+":8080/iss/view?type=viewer&unit="+sn+"\">"+location+"</a></td>"+
						 "<td id="+sn_dev+">"+sn+"</td>"+
					     "<td>"+chassis+"</td>"+
					     "<td id="+status+">"+status+"</td>"+
					     "<td>"+nccode+"</td>"+
					     "<td>"+reason+"</td>"+
					     "<input type='hidden' id="+ip_dev+">"+reason+">"+
					     "<td><input type=\"checkbox\"  class=\"checkItem\" onClick=\"radioAll('checkItem')\" disabled  /></td>";

					}

			}	
				
		    $("#chassis").val(chassis);
			$("#dsn").val(ssn);
			//$("#ddiskip").val(diskIp);
			$("#test_id").val(test_id);
			
			console.log("ID"+test_id);

		});
		
		/*<input type="hidden" value="" id="chassis" />
	        <input type="hidden" value="" id="dtype" />
	        <input type="hidden" value="" id="dsn" />*/
		
		commitbutton = commitbutton + "<input type='button' class='btn btn-success' value='Commit'id='commitPost' onclick=\"commitDev()\" style='float: right; margin-right: 0px;' disabled/>";
		$("#commitbutton").html(commitbutton);
		
		resetbutton = resetbutton + "<input type='button' class='btn btn-success' value='Reset Form' id='resetPost' style='float: right; margin-right: 30px;' onClick=\"resetDer()\" disabled/>";
		$("#resetbutton").html(resetbutton);
		
		
		
		$("#bodyDelivery").html(deliveryList);
		
		$("html, body").animate({
			scrollTop : $(document).height()
			
		}, "slow");
		clearInterval(myInterval);
		openInterval();
		
	});
	
	
	
	// interactions tab ---------------------------------------------------------------
	$.ajax({
		url: "http://"+ip_local+":8008/getInteraction?ip="+diskIp+"&sn="+serialnumber+"&location="+slot
		//url: "http://10.196.11.137:8008/getInteraction?ip="+diskIp+"&sn="+serialnumber
	}).done(function(data) 
	{
		
		if (showtab=="interactionTab"){
			
			$("#interactionTab").tab('show');
			document.getElementById("node").style.display = "none";
			document.getElementById("delivery").style.display = "none";
			document.getElementById("interaction").style.display = "block";
			
			document.getElementById("allNodeBtn").style.display = "block";
			console.log("chkStatus"+chkStatus);
			if(chkStatus == "Aborted" || chkStatus == "Passes" || chkStatus == "Failed"){
				document.getElementById("commitDevButton").style.display = "block";
				document.getElementById("resetDevButton").style.display = "block";
			}else{

				document.getElementById("commitDevButton").style.display = "none";
				document.getElementById("resetDevButton").style.display = "none";


				}
		}
        var json = JSON.parse(data);
        var interactionList = "";
        $.each(json, function (key,value){
            
              var json = data;    
              var parsed = $.parseJSON(json);
              var $code1 = "";
    	
            var unit = value.unit;
            var location = value.location;
            var interaction = value.interaction;
            var title = value.title;
            var time = value.time;
            var status = value.status;
            var serial = value.serial;

            interactionList = interactionList + "<tr><td><a target=\"_blank\" href=\"http://"+diskIp+":8080/iss/user_interaction?action=display_question&UNIT_TO_BATCH="+unit+"&LOCATION="+location+"&QUESTION_ID="+interaction+"\">"+unit+"</a></td>"+
                             "<td id=\""+location+"\">"+location+"</td>"+
                             "<td>"+interaction+"</td>"+
                             "<td>"+title+"</td>"+
                             "<td>"+time+"</td>"+
                             "<td>"+status+"</td>";

        });

		$("#bodyInteraction").html(interactionList);
		
		$("html, body").animate({
			scrollTop : $(document).height()
		}, "slow");
		clearInterval(myInterval);
		openInterval();
		

	});

	$("#ddiskip").val(diskIp);
	//setTimeout(openInterval(), 30000);
	$(".aclose").popover("hide");
    
}

		function resetDer() {
			
			$('input[type=checkbox]').attr('checked', false);
			$("#commitPost").attr('disabled', true);
    	    $("#resetPost").attr('disabled', true);

		}
		
		function scanin(operation,operator_id,batchId,serialnumber,test_id,logIp,diskIp,comment){
//          console.log(operation);
//          console.log(diskIp);
//          console.log(operatorID);
//          console.log(logIp);
//	        console.log(batchId);
	        $("#batchid").val(batchId);
	        $("#diskIp").val(diskIp);
	        $("#test_id").val(test_id);
	        $("#logIP").val(logIp);
	 	//$("#projectname").val(comment);
	        /// copy staion name to uses as chassis number ///
	        var station_name = $("#station_ses").val();
	        station_name = station_name.replace('/r','/').replace(/\-/g,"");
	        $("#sn_test").val(station_name);
          
      }

           // userInteraction();
            function stopUpdate() {
			    clearTimeout(timeout);
			}
            
            function commitDev(){
            	
            	var chassis = $("#chassis").val();
            	var type = $("#dtype").val();
            	var sn = $("#dsn").val();
            	var diskIP = $("#ddiskip").val();
            	var location = $('#clicked_slot').val();
            	
            	console.log("type"+type);
            	console.log("sn"+sn);
            	console.log("diskIP"+diskIP);
            	console.log("chassis"+chassis);
            	
            	var ip_local = $("#ip_local").val();
            	console.log(ip_local);
            	
            	var test_id = $("#test_id").val(); 
    			console.log("testID"+test_id);
	            
            	if(type == "retest"){

            		var checkedValues = $('input:checkbox:checked').map(function() {
            		    return this.value;
            		}).get();	

            		console.log('Btns-retest' + checkedValues);
            		console.log('length' + checkedValues.length);
    						for (i = 0; i < checkedValues.length; i++) {
    							console.log('retest' + checkedValues[i]);
    							$.ajax({
    				    			
    				    			url : "http://"+ip_local+":8008/retest",
    				        		type : 'GET', 
    				    			data:{"ip":diskIP,"type":type,"sn":checkedValues[i]},
    				    			
    				    			beforeSend: function(){
    									$('#myModalLoading').modal({backdrop: 'static', keyboard: false});
    									setTimeout(function() {
    										$('#myModalLoading').modal('hide');
    										$('#tablist').hide();
    					    				$('#tabcontent_id').hide();
    									}, 1000)
    								},
    				    			
    				    			success : function(data) {
    				    				var errordata = JSON.parse(data);
    				    				if (errordata.data.error == null) {
    				    					$('#myModalLoading').modal('hide');
    				    				}else{
    				    					var $code = '<p>' + errordata.data.error + '</p>'; 
    				    					$('#myModalLoading').modal('hide');
    										$('#myModalError').modal('show');
    										$('#test11').html($code);
    				    				}
    				    			},
    				    			error : function(xhr, status, error) {
    				    				///var err = eval("(" + xhr.responseText + ")");
    				    				
    				    			}
    				    		});
    						}
                	    console.log("retest");
                	//});
            		
	            	
            	}else if(type == "retestBatch"){
            		$.ajax({

						 url : "http://"+ip_local+":8008/retestbatch", 

						 data:{
	 							"SN" : chassis,
	 							"ip":diskIP,
	 							"location": location,
	 							"Action" : "retest"
						 }, 
						 //data:{sn: unit,ip:ip,ipdist:ip_local,type:"retest"},
						 type : "GET",
							//data : JSON.stringify(TestData),
							//dataType: 'plain/text',
							//contentType : 'text/plain',
						 
						 beforeSend: function(){
								$('#myModalLoading').modal({backdrop: 'static', keyboard: false});
								setTimeout(function() {
									$('#myModalLoading').modal('hide');
									$('#tablist').hide();
				    				$('#tabcontent_id').hide();
								}, 1000)
						 },
			    			
			    			success : function(data) {
			    				var errordata = JSON.parse(data);
			    				if (errordata.data.error == null) {
			    					$('#myModalLoading').modal('hide');
			    				}else{
			    					var $code = '<p>' + errordata.data.error + '</p>'; 
			    					$('#myModalLoading').modal('hide');
									$('#myModalError').modal('show');
									$('#test11').html($code);
			    				}
			    			},
			    			error : function(xhr, status, error) {
			    				///var err = eval("(" + xhr.responseText + ")");
			    				
			    			}

						 });
            	}else{
            		$.ajax({
		    			
		    			url : "http://"+ip_local+":8008/delivery",
		        		type : 'GET', 
		    			data:{"ip":diskIP,"type":type,"sn":chassis,"test_id":test_id,"location": location},
		
		    			beforeSend: function(){
							$('#myModalLoading').modal({backdrop: 'static', keyboard: false});
							setTimeout(function() {
								$('#myModalLoading').modal('hide');
								//openInterval();
								getUUT();
			    				//openInterval();
			    				$('#tablist').hide();
			    				$('#tabcontent_id').hide();
							}, 1000)
							
		    			},
		    			
		    			success : function(data) {
		    				console.log('success');
		    				//getUUT();
		    				//openInterval();
		    				
		    				var errordata = JSON.parse(data);
		    				console.log("myModalChkout"+errordata.data.status_code);
		    				if (errordata.data.status_code == null) {
		    					console.log("myModalChkout No Response");
		    				}else{
		    					var $chk = '<p>' + errordata.data.status_code + '</p>'; 
		    					var $chassis = '<p>Serial Number :' + chassis + '</p>'; 
								console.log("myModalChkout"+$chk);
								console.log("myModalChkout"+$chassis);
								$('#myModalChkout').modal('show');
								$('#chkOut').html($chk);
								$('#chkChassis').html($chassis);
		    				}
		    				console.log("Delivery!!!!!errordata"+errordata.data.error);
		    				if (errordata.data.error == null || errordata.data.error == "Cannot connect Dist Server") {
		    					$('#myModalLoading').modal('hide');
		    					//openInterval();
		    				}else{
		    					
		    					var $code = '<p>' + errordata.data.error + '</p>'; 
		    					$('#myModalLoading').modal('hide');
								$('#myModalError').modal('show');
								$('#test11').html($code);
		    				}
		    			},
		    			error : function(xhr, status, error) {
		    				///var err = eval("(" + xhr.responseText + ")");
		    				
		    			}
		    		});
            	}
            }
            
            function abortFunc(ip,slot,serialnumber){
//            	console.log("abortIP"+ip);
//            	$.ajax({
//					//url : "http://" + ip + "/cgi-bin/abort",
//					
//					url:"http://" + ip + "/cgi-bin/abort?unit="+serialnumber+"&slot="+slot,
//					//url:"http://localhost/cgi-bin/abort?unit="+name+"?slot="+slot,
//					dataType : "text",
//					type : "POST",
//					data : {
//						slot : slot,
//						unit : serialnumber
//					},
//					//data:abortData,
//					//dataType: 'json',
//
//					success : function(data) {
//						console.log('test');
//						setTimeout(function() {
//							//window.location.reload(true);
//						}, 5000);
//
//					},
//				});
            	$('#clicked_slot').val(slot);
    	        $("#abortDiskIp").val(ip);
    	        $("#abortSlot").val(slot);
    	        $("#abortSerialnumber").val(serialnumber);
    	        
    	        $(".aclose").popover("hide");

            }
            
            function setClearData(test_id){
            	console.log("setClearData"+test_id);
            	$("#test_id").val(test_id);
            	//$("#abortSerialnumber").val(serialnumber);
            	$(".aclose").popover("hide");
            }

            function setAbortData(test_id){
            	console.log("setAbortData"+test_id);
            	$("#test_id").val(test_id);
            	$(".aclose").popover("hide");
            }
            
            function setDeliveryData(test_id,ip,slot,serialnumber){
            	$('#clicked_slot').val(slot);
            	console.log("setDeliveryData"+test_id);
            	console.log("setDeliveryIP"+ip);
            	$("#test_id").val(test_id);
            	$("#ddiskip").val(ip); 
    	        $("#dtype").val("DELETE");
    	        $("#chassis").val(serialnumber);
            	
    	        $(".aclose").popover("hide");
            	
            }
            function setCheckOutData(test_id,ip,slot,serialnumber){
            	$('#clicked_slot').val(slot);
            	console.log("setDeliveryData"+test_id);
            	console.log("setDeliveryIP"+ip);
            	$("#test_id").val(test_id);
            	$("#ddiskip").val(ip); 
    	        $("#dtype").val("STOP");
    	        $("#chassis").val(serialnumber);

    	        $(".aclose").popover("hide");
            }
            
            function setComment(test_id){
            	console.log("setComment"+test_id);
            	$("#test_id").val(test_id);
            	
            	$(".aclose").popover("hide");
            }
            
