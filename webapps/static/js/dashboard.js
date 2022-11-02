var milliseconds = 30000;
var myInterval;
var showtab;

function getDashboard(){
	
	var showtab = $('#typeSession').val();
	
	console.log("getDashboard"+showtab);
	var ip_local = $('#ip_local').val();

	if(showtab == "1"){
		console.log("showtab111");
		$("#typeSession").val("1");
		$.ajax({
			url: "http://"+ip_local+":8008/dashboard?type="+showtab
			//url: "http://10.196.11.137:8008/getUUT?station="+sessionStorage.getItem("station_ses")
			//url: "http://localhost:8080/iss/jsonDataDashboard",
		}).done(function(json) {
			var data = JSON.parse(json);
			console.log("test"+Object.keys(data).length);
			var uutData = "";
			var ipData = "";	
			var cutData ="";
			var chkList = "";
				$.each(data, function (key, value) {
					console.log(key);
	//				if(chkList === ""){
	//					chkList = key;
	//					uutData += '<div class="row"><h3 class="heading-1" ><span>'+key+'</span></h1>';
	//				}else if(chkList !== key){
	//					uutData += '</div><div class="row"><h3 class="heading-1"><span>'+key+'</span></h1>';
	//				}
					//ipData = ipData + '<h1 class="heading-1"><span>'+key+'</span></h1>';
					$.each(value, function (subkey, val) {
						
						//console.log(subkey);
						//console.log(value);
						console.log("subkey"+Object.keys(value).length);
						
						var status = val.status;
						var slot = val.slot;
						var station = val.station;
						var serialnumber = val.serialnumber;
						var vm = val.vm;
						var interaction = val.interaction;
						var commentTxt = val.comment;
						var comment_re = val.comment_re;
						var release = val.release;
					    var test_ip = val.test_ip;
					    var testtime = val.testtime;
						//console.log(status);
						//console.log(station)
						
						
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
			                var color_h = "#A9A9AA";
			                var color_b = "#CCCCCC";
			            }else if(status == "-"){
			                var color_h = "#A9A9AA";
			                var color_b = "#CCCCCC";
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
			                var color_h = "#A9A9AA";
			                var color_b = "#A9A9AA";
			            }
			            
			            if (commentTxt == "-"){
		            		imgComment = ''

						}else{
							imgComment = '<img src="Images/comment-icon.png" width="15" height="10"/>'
							
						}
	//		            
	//		            if(subkey == "0"){
	//		            	uutData = uutData + '<h1 class="heading-1"><span>'+key+'</span></h1>'+
	//						'<div class="col-sm-2" style="padding:0;">'+
	//							'<div class="panel" style="width:100%;margin-bottom:0;">'+
	//								'<div class="panel-heading" style="background-color:'+color_h+';"><div style="font-size:15px;font-weight:bold;" id="testSlot">'+slot+'<span style="float:right;">'+status+'</span></div></div>'+
	//								'<div class="panel-body" style="background-color:'+color_b+';">'+
	//									'<div style="text-align:center;">'+
	//										'<span style="font-size:13px;"><b>'+serialnumber+'</b></span>'+
	//									'</div>'+
	//									'<div style="text-align:center;font-size:13px;">'+
	//										'<p>'+station+'</p>'+
	//									'</div>'+
	//								'</div>'+
	//							'</div>'+
	//						'</div>';
	//		            	
	//		            }else{
			            
			            //ipData = ipData + '<div class="panel-heading" style="background-color:'+color_h+';"><div style="font-size:15px;font-weight:bold;" id="testSlot"><span style="float:center;">'+key+'</span></div></div>';
			            if(status == "-" || status == "New"){	
			            	uutData =  uutData+
			            	'<div class="col-8" style="padding:0;color:#ffffff">'+
							'<div class="panel" style="width:100%;margin-bottom:0;">'+
								'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
									'<div class="row">'+
										'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
										'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
											'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
										'</div>'+
									'</div>'+
								'</div>'+
								'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
									'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
									'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
										'<div class="row">'+
											'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
											'<div class="col-md-4"></div>'+
										'</div>'+	
									'</div>'+
								'</div>'+
								'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
									'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0; width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
									'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0; width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
								'</div>'+
							'</div>'+
						'</div>';
			            }
			            else if(status == "Testing" ){	
			            	if (interaction == "True"){
			            		bg = '<img style="float:right;margin-top:2px;margin-right:2px;" src="Images/interAc.png" width="22" height="22"/>'
	
							}else{
								bg = ''
								
							}
			            	
			            	uutData = uutData+ 
							'<div class="col-8" style="padding:0;color:#ffffff">'+
								'<div class="panel" style="width:100%;margin-bottom:0;">'+
									'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
										'<div class="row">'+
											'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
											'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
												'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
											'</div>'+
										'</div>'+
									'</div>'+
									'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
										'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
											'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
											'<div class="row">'+
												'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
												'<div class="col-md-4">'+bg+'</div>'+
											'</div>'+	
										'</div>'+
									'</div>'+
									'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
										'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0; width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0; width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
								'</div>'+
							'</div>';
							
	
			            }
			            else if(status == "Failing"){	
			            	if (interaction == "True"){
			            		bg = '<img style="float:right;margin-top:2px;margin-right:2px;" src="Images/interAc.png" width="22" height="22"/>'
	
							}else{
								bg = ''
								
							}		            	
			            	uutData = uutData+ 
							'<div class="col-8" style="padding:0;color:#ffffff">'+
								'<div class="panel" style="width:100%;margin-bottom:0;">'+
									'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
										'<div class="row">'+
											'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
											'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
												'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
											'</div>'+
										'</div>'+
									'</div>'+
									'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
										'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
											'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
											'<div class="row">'+
												'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
												'<div class="col-md-4">'+bg+'</div>'+
											'</div>'+	
										'</div>'+
									'</div>'+
									'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
										'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
								'</div>'+
							'</div>';
			            	
			            }else if(status == "Aborted"){	
			            	
								uutData = uutData+ 
								'<div class="col-8" style="padding:0;color:#ffffff">'+
									'<div class="panel" style="width:100%;margin-bottom:0;">'+
										'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
											'<div class="row">'+
												'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
												'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
													'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
												'</div>'+
											'</div>'+
										'</div>'+
										'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
											'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
											'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
												'<div class="row">'+
													'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
													'<div class="col-md-4"></div>'+
												'</div>'+	
											'</div>'+
										'</div>'+
										'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
											'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
											'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
										'</div>'+
									'</div>'+
								'</div>';
							
			            }else if(status == "Passes"){	
			            	
			            	uutData = uutData+ 
			            	'<div class="col-8" style="padding:0;color:#ffffff">'+
							'<div class="panel" style="width:100%;margin-bottom:0;">'+
								'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
									'<div class="row">'+
										'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
										'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
											'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
										'</div>'+
									'</div>'+
								'</div>'+
								'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
									'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
									'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
										'<div class="row">'+
											'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
											'<div class="col-md-4"></div>'+
										'</div>'+	
									'</div>'+
								'</div>'+
								'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
									'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
									'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
								'</div>'+
							'</div>'+
						'</div>';
							
			            }
			            else if(status == "Failed"){	
			            	
								uutData = uutData+ 
								'<div class="col-8" style="padding:0;color:#ffffff">'+
								'<div class="panel" style="width:100%;margin-bottom:0;">'+
									'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
										'<div class="row">'+
											'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
											'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
												'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
											'</div>'+
										'</div>'+
									'</div>'+
									'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
										'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
										'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
											'<div class="row">'+
												'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
												'<div class="col-md-4"></div>'+
											'</div>'+	
										'</div>'+
									'</div>'+
									'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
										'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
								'</div>'+
							'</div>';
							
			            }else{
			            	if (status =="Checking out"){
			            			status = "Delivering"
			            	}
			            	uutData = uutData+ 
			            	'<div class="col-8" style="padding:0;color:#ffffff">'+
							'<div class="panel" style="width:100%;margin-bottom:0;">'+
								'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
									'<div class="row">'+
										'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
										'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
											'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
										'</div>'+
									'</div>'+
								'</div>'+
								'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
									'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
									'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
										'<div class="row">'+
											'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
											'<div class="col-md-4"></div>'+
										'</div>'+	
									'</div>'+
								'</div>'+
								'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
									'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
									'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
								'</div>'+
							'</div>'+
						'</div>';
			            }
			            //}
			            //clearInterval(myInterval);
			    		//openInterval();
							
							
							
						
							
						//$("#uutList").html((uutData));
					});
					//$("#ip_server").html("ip_server");
					//$("#ip_server").html(ipData);
					//$("#uutList").html((uutData));
				});
				//uutData += '</div>';
				console.log(Object.keys(data));
	//			jQuery.each(Object.keys(data), function(i, val) {
	//				ipData += '<span>'+val+'</span>';
	//		    });
				$("#listProc").html((uutData));
				//$("#ip_server").html(ipData);
				//$("#cutData").html(cutData);
		});
		
	}else if(showtab == "2"){
		console.log("showtab222");
		$.ajax({
			  url: "http://"+ip_local+":8008/dashboard?type="+showtab
				//url: "http://10.196.11.137:8008/getUUT?station="+sessionStorage.getItem("station_ses")
				//url: "http://localhost:8080/iss/jsonDataDashboard",
			}).done(function(json) {
				var data = JSON.parse(json);
				console.log("test"+Object.keys(data).length);
				var uutData = "";
				var ipData = "";	
				var cutData ="";
				var chkList = "";
					$.each(data, function (key, value) {
						console.log(key);
		//				if(chkList === ""){
		//					chkList = key;
		//					uutData += '<div class="row"><h3 class="heading-1" ><span>'+key+'</span></h1>';
		//				}else if(chkList !== key){
		//					uutData += '</div><div class="row"><h3 class="heading-1"><span>'+key+'</span></h1>';
		//				}
						//ipData = ipData + '<h1 class="heading-1"><span>'+key+'</span></h1>';
						$.each(value, function (subkey, val) {
							
							//console.log(subkey);
							//console.log(value);
							console.log("subkey"+Object.keys(value).length);
							
							var status = val.status;
							var slot = val.slot;
							var station = val.station;
							var serialnumber = val.serialnumber;
							var vm = val.vm;
							var interaction = val.interaction;
							var commentTxt = val.comment;
							var comment_re = val.comment_re;
							var release = val.release;
						    var test_ip = val.test_ip;
						    var testtime = val.testtime;
							//console.log(status);
							//console.log(station)
							
							
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
				                var color_h = "#A9A9AA";
				                var color_b = "#CCCCCC";
				            }else if(status == "-"){
				                var color_h = "#A9A9AA";
				                var color_b = "#CCCCCC";
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
				                var color_h = "#A9A9AA";
				                var color_b = "#A9A9AA";
				            }
				            
				            if (commentTxt == "-"){
			            		imgComment = ''

							}else{
								imgComment = '<img src="Images/comment-icon.png" width="15" height="10"/>'
								
							}
		//		            
		//		            if(subkey == "0"){
		//		            	uutData = uutData + '<h1 class="heading-1"><span>'+key+'</span></h1>'+
		//						'<div class="col-sm-2" style="padding:0;">'+
		//							'<div class="panel" style="width:100%;margin-bottom:0;">'+
		//								'<div class="panel-heading" style="background-color:'+color_h+';"><div style="font-size:15px;font-weight:bold;" id="testSlot">'+slot+'<span style="float:right;">'+status+'</span></div></div>'+
		//								'<div class="panel-body" style="background-color:'+color_b+';">'+
		//									'<div style="text-align:center;">'+
		//										'<span style="font-size:13px;"><b>'+serialnumber+'</b></span>'+
		//									'</div>'+
		//									'<div style="text-align:center;font-size:13px;">'+
		//										'<p>'+station+'</p>'+
		//									'</div>'+
		//								'</div>'+
		//							'</div>'+
		//						'</div>';
		//		            	
		//		            }else{
				            
				            //ipData = ipData + '<div class="panel-heading" style="background-color:'+color_h+';"><div style="font-size:15px;font-weight:bold;" id="testSlot"><span style="float:center;">'+key+'</span></div></div>';
				            if(status == "-" || status == "New"){	
				            	uutData =  uutData+
				            	'<div class="col-8" style="padding:0;color:#ffffff">'+
								'<div class="panel" style="width:100%;margin-bottom:0;">'+
									'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
										'<div class="row">'+
											'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
											'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
												'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
											'</div>'+
										'</div>'+
									'</div>'+
									'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
										'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
										'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
											'<div class="row">'+
												'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
												'<div class="col-md-4"></div>'+
											'</div>'+	
										'</div>'+
									'</div>'+
									'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
										'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
								'</div>'+
							'</div>';
				            }
				            else if(status == "Testing" ){	
				            	if (interaction == "True"){
				            		bg = '<img style="float:right;margin-top:2px;margin-right:2px;" src="Images/interAc.png" width="22" height="22"/>'
		
								}else{
									bg = ''
									
								}
				            	
				            	uutData = uutData+ 
								'<div class="col-8" style="padding:0;color:#ffffff">'+
									'<div class="panel" style="width:100%;margin-bottom:0;">'+
										'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
											'<div class="row">'+
												'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
												'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
													'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
												'</div>'+
											'</div>'+
										'</div>'+
										'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
											'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
												'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
												'<div class="row">'+
													'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
													'<div class="col-md-4">'+bg+'</div>'+
												'</div>'+	
											'</div>'+
										'</div>'+
										'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
											'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
											'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
										'</div>'+
									'</div>'+
								'</div>';
								
		
				            }
				            else if(status == "Failing"){	
				            	if (interaction == "True"){
				            		bg = '<img style="float:right;margin-top:2px;margin-right:2px;" src="Images/interAc.png" width="22" height="22"/>'
		
								}else{
									bg = ''
									
								}		            	
				            	uutData = uutData+ 
								'<div class="col-8" style="padding:0;color:#ffffff">'+
									'<div class="panel" style="width:100%;margin-bottom:0;">'+
										'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
											'<div class="row">'+
												'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
												'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
													'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
												'</div>'+
											'</div>'+
										'</div>'+
										'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
											'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
												'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
												'<div class="row">'+
													'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
													'<div class="col-md-4">'+bg+'</div>'+
												'</div>'+	
											'</div>'+
										'</div>'+
										'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
											'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
											'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
										'</div>'+
									'</div>'+
								'</div>';
				            	
				            }else if(status == "Aborted"){	
				            	
									uutData = uutData+ 
									'<div class="col-8" style="padding:0;color:#ffffff">'+
										'<div class="panel" style="width:100%;margin-bottom:0;">'+
											'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
												'<div class="row">'+
													'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
													'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
														'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
													'</div>'+
												'</div>'+
											'</div>'+
											'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
												'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
												'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
													'<div class="row">'+
														'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
														'<div class="col-md-4"></div>'+
													'</div>'+	
												'</div>'+
											'</div>'+
											'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
												'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
												'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
											'</div>'+
										'</div>'+
									'</div>';
								
				            }else if(status == "Passes"){	
				            	
				            	uutData = uutData+ 
				            	'<div class="col-8" style="padding:0;color:#ffffff">'+
								'<div class="panel" style="width:100%;margin-bottom:0;">'+
									'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
										'<div class="row">'+
											'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
											'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
												'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
											'</div>'+
										'</div>'+
									'</div>'+
									'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
										'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
										'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
											'<div class="row">'+
												'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
												'<div class="col-md-4"></div>'+
											'</div>'+	
										'</div>'+
									'</div>'+
									'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
										'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
								'</div>'+
							'</div>';
								
				            }
				            else if(status == "Failed"){	
				            	
									uutData = uutData+ 
									'<div class="col-8" style="padding:0;color:#ffffff">'+
									'<div class="panel" style="width:100%;margin-bottom:0;">'+
										'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
											'<div class="row">'+
												'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
												'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
													'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
												'</div>'+
											'</div>'+
										'</div>'+
										'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
											'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
											'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
												'<div class="row">'+
													'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
													'<div class="col-md-4"></div>'+
												'</div>'+	
											'</div>'+
										'</div>'+
										'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
											'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
											'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
										'</div>'+
									'</div>'+
								'</div>';
								
				            }else{
				            	if (status =="Checking out"){
				            			status = "Delivering"
				            	}
				            	uutData = uutData+ 
				            	'<div class="col-8" style="padding:0;color:#ffffff">'+
								'<div class="panel" style="width:100%;margin-bottom:0;">'+
									'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
										'<div class="row">'+
											'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
											'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
												'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
											'</div>'+
										'</div>'+
									'</div>'+
									'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
										'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
										'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
											'<div class="row">'+
												'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
												'<div class="col-md-4"></div>'+
											'</div>'+	
										'</div>'+
									'</div>'+
									'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
										'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
								'</div>'+
							'</div>';
				            }
				            //}
				            //clearInterval(myInterval);
				    		//openInterval();
								
								
								
							
								
							//$("#uutList").html((uutData));
						});
						//$("#ip_server").html("ip_server");
						//$("#ip_server").html(ipData);
						//$("#uutList").html((uutData));
					});
					//uutData += '</div>';
					console.log(Object.keys(data));
		//			jQuery.each(Object.keys(data), function(i, val) {
		//				ipData += '<span>'+val+'</span>';
		//		    });
					$("#listDev").html((uutData));
					//$("#ip_server").html(ipData);
					//$("#cutData").html(cutData);
			});
		
	}else if(showtab == "3"){
		console.log("showtab333");
		$.ajax({
			  url: "http://"+ip_local+":8008/dashboard?type="+showtab
				//url: "http://10.196.11.137:8008/getUUT?station="+sessionStorage.getItem("station_ses")
				//url: "http://localhost:8080/iss/jsonDataDashboard",
			}).done(function(json) {
				var data = JSON.parse(json);
				console.log("test"+Object.keys(data).length);
				var uutData = "";
				var ipData = "";	
				var cutData ="";
				var chkList = "";
					$.each(data, function (key, value) {
						console.log(key);
		//				if(chkList === ""){
		//					chkList = key;
		//					uutData += '<div class="row"><h3 class="heading-1" ><span>'+key+'</span></h1>';
		//				}else if(chkList !== key){
		//					uutData += '</div><div class="row"><h3 class="heading-1"><span>'+key+'</span></h1>';
		//				}
						//ipData = ipData + '<h1 class="heading-1"><span>'+key+'</span></h1>';
						$.each(value, function (subkey, val) {
							
							//console.log(subkey);
							//console.log(value);
							console.log("subkey"+Object.keys(value).length);
							
							var status = val.status;
							var slot = val.slot;
							var station = val.station;
							var serialnumber = val.serialnumber;
							var vm = val.vm;
							var interaction = val.interaction;
							var commentTxt = val.comment;
							var comment_re = val.comment_re;
							var release = val.release;
						    var test_ip = val.test_ip;
						    var testtime = val.testtime;
							//console.log(status);
							//console.log(station)
							
							
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
				                var color_h = "#A9A9AA";
				                var color_b = "#CCCCCC";
				            }else if(status == "-"){
				                var color_h = "#A9A9AA";
				                var color_b = "#CCCCCC";
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
				                var color_h = "#A9A9AA";
				                var color_b = "#A9A9AA";
				            }
				            
				            if (commentTxt == "-"){
			            		imgComment = ''

							}else{
								imgComment = '<img src="Images/comment-icon.png" width="15" height="10"/>'
								
							}
		//		            
		//		            if(subkey == "0"){
		//		            	uutData = uutData + '<h1 class="heading-1"><span>'+key+'</span></h1>'+
		//						'<div class="col-sm-2" style="padding:0;">'+
		//							'<div class="panel" style="width:100%;margin-bottom:0;">'+
		//								'<div class="panel-heading" style="background-color:'+color_h+';"><div style="font-size:15px;font-weight:bold;" id="testSlot">'+slot+'<span style="float:right;">'+status+'</span></div></div>'+
		//								'<div class="panel-body" style="background-color:'+color_b+';">'+
		//									'<div style="text-align:center;">'+
		//										'<span style="font-size:13px;"><b>'+serialnumber+'</b></span>'+
		//									'</div>'+
		//									'<div style="text-align:center;font-size:13px;">'+
		//										'<p>'+station+'</p>'+
		//									'</div>'+
		//								'</div>'+
		//							'</div>'+
		//						'</div>';
		//		            	
		//		            }else{
				            
				            //ipData = ipData + '<div class="panel-heading" style="background-color:'+color_h+';"><div style="font-size:15px;font-weight:bold;" id="testSlot"><span style="float:center;">'+key+'</span></div></div>';
				            if(status == "-" || status == "New"){	
				            	uutData =  uutData+
				            	'<div class="col-8" style="padding:0;color:#ffffff">'+
								'<div class="panel" style="width:100%;margin-bottom:0;">'+
									'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
										'<div class="row">'+
											'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
											'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
												'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
											'</div>'+
										'</div>'+
									'</div>'+
									'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
										'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
										'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
											'<div class="row">'+
												'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
												'<div class="col-md-4"></div>'+
											'</div>'+	
										'</div>'+
									'</div>'+
									'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
										'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
								'</div>'+
							'</div>';
				            }
				            else if(status == "Testing" ){	
				            	if (interaction == "True"){
				            		bg = '<img style="float:right;margin-top:2px;margin-right:2px;" src="Images/interAc.png" width="22" height="22"/>'
		
								}else{
									bg = ''
									
								}
				            	
				            	uutData = uutData+ 
								'<div class="col-8" style="padding:0;color:#ffffff">'+
									'<div class="panel" style="width:100%;margin-bottom:0;">'+
										'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
											'<div class="row">'+
												'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
												'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
													'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
												'</div>'+
											'</div>'+
										'</div>'+
										'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
											'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
												'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
												'<div class="row">'+
													'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
													'<div class="col-md-4">'+bg+'</div>'+
												'</div>'+	
											'</div>'+
										'</div>'+
										'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
											'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
											'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
										'</div>'+
									'</div>'+
								'</div>';
								
		
				            }
				            else if(status == "Failing"){	
				            	if (interaction == "True"){
				            		bg = '<img style="float:right;margin-top:2px;margin-right:2px;" src="Images/interAc.png" width="22" height="22"/>'
		
								}else{
									bg = ''
									
								}		            	
				            	uutData = uutData+ 
								'<div class="col-8" style="padding:0;color:#ffffff">'+
									'<div class="panel" style="width:100%;margin-bottom:0;">'+
										'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
											'<div class="row">'+
												'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
												'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
													'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
												'</div>'+
											'</div>'+
										'</div>'+
										'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
											'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
												'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
												'<div class="row">'+
													'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
													'<div class="col-md-4">'+bg+'</div>'+
												'</div>'+	
											'</div>'+
										'</div>'+
										'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
											'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
											'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
										'</div>'+
									'</div>'+
								'</div>';
				            	
				            }else if(status == "Aborted"){	
				            	
									uutData = uutData+ 
									'<div class="col-8" style="padding:0;color:#ffffff">'+
										'<div class="panel" style="width:100%;margin-bottom:0;">'+
											'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
												'<div class="row">'+
													'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
													'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
														'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
													'</div>'+
												'</div>'+
											'</div>'+
											'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
												'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
												'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
													'<div class="row">'+
														'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
														'<div class="col-md-4"></div>'+
													'</div>'+	
												'</div>'+
											'</div>'+
											'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
												'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
												'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
											'</div>'+
										'</div>'+
									'</div>';
								
				            }else if(status == "Passes"){	
				            	
				            	uutData = uutData+ 
				            	'<div class="col-8" style="padding:0;color:#ffffff">'+
								'<div class="panel" style="width:100%;margin-bottom:0;">'+
									'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
										'<div class="row">'+
											'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
											'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
												'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
											'</div>'+
										'</div>'+
									'</div>'+
									'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
										'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
										'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
											'<div class="row">'+
												'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
												'<div class="col-md-4"></div>'+
											'</div>'+	
										'</div>'+
									'</div>'+
									'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
										'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
								'</div>'+
							'</div>';
								
				            }
				            else if(status == "Failed"){	
				            	
									uutData = uutData+ 
									'<div class="col-8" style="padding:0;color:#ffffff">'+
									'<div class="panel" style="width:100%;margin-bottom:0;">'+
										'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
											'<div class="row">'+
												'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
												'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
													'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
												'</div>'+
											'</div>'+
										'</div>'+
										'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
											'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
											'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
												'<div class="row">'+
													'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
													'<div class="col-md-4"></div>'+
												'</div>'+	
											'</div>'+
										'</div>'+
										'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
											'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
											'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
										'</div>'+
									'</div>'+
								'</div>';
								
				            }else{
				            	if (status =="Checking out"){
				            			status = "Delivering"
				            	}
				            	uutData = uutData+ 
				            	'<div class="col-8" style="padding:0;color:#ffffff">'+
								'<div class="panel" style="width:100%;margin-bottom:0;">'+
									'<div class="panel-heading" style="background-color:'+color_h+';border-radius:0px !important;">'+
										'<div class="row">'+
											'<div class="col-md-6" style="font-size:22px;font-weight:bold;margin-top:7px;" id="testSlot">'+vm+'</div>'+
											'<div class="col-md-6" style="font-size:10px;font-weight:bold;text-align:right;">'+
												'<span style="font-weight: bold;font-size:12px;">'+slot+'</span><br><span style="font-weight: normal;font-size:10px;">'+'['+status+']'+'</span><br><span style="font-weight: normal;font-size:10px;">'+testtime+'</span>'+
											'</div>'+
										'</div>'+
									'</div>'+
									'<div class="panel-body" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 1px solid #fff; border-top: 3px solid #f5f5f5; border-right: 3px solid #f5f5f5; border-radius: 3px;">'+
										'<div style="text-align:left;"><span style="font-size:14px;margin:5px;"><b><a target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" style="color:'+color_b+'>'+serialnumber+'</a></b></span></div>'+								
										'<span style="font-size:12px;margin:3px;"><b><a class="comment" target="_blank" href="http://'+ip_local+':8080/iss-main/ShowTestingServlet?sname='+station+'" data-toggle="tooltip" data-placement="bottom" title="'+serialnumber+'">'+serialnumber+'</a></b></span>'+
											'<div class="row">'+
												'<div class="col-md-8" style="font-size:10px;" width="18" height="18"><p style="text-align:left;font-size:10px;margin:5px;color:#000;float:center;width:90px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;  " data-toggle="tooltip" data-placement="bottom" title="'+station+'">'+station+'</p></div>'+
												'<div class="col-md-4"></div>'+
											'</div>'+	
										'</div>'+
									'</div>'+
									'<div class="panel-footer" style="background-color:#f5f5f5 ; padding:0; border-left: 3px solid '+color_b+'; border-bottom: 3px solid #f5f5f5; border-top: 1px solid #fff; border-right: 3px solid #f5f5f5;border-radius: 3px;">'+
										'<a class="comment" style="display:block; text-align:left; color:#444; margin:5px;font-size:9px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+commentTxt+'">'+commentTxt+'</a>'+
										'<a class="comment" style="display:block; color:'+color_b+'; font-size:9px;font-weight:normal; text-align:left; margin:5px; padding:0;width:120px;" data-toggle="tooltip" data-placement="bottom" title="'+comment_re+'" href="http://'+test_ip+':8080/iss/view?type=fileDetail&unit='+serialnumber+'&testSuite=&testSet=&testEvent=&file=release.properties" target="_blank">'+release+'</a>'+
									'</div>'+
								'</div>'+
							'</div>';
				            }
				            //}
				            //clearInterval(myInterval);
				    		//openInterval();
								
								
								
							
								
							//$("#uutList").html((uutData));
						});
						//$("#ip_server").html("ip_server");
						//$("#ip_server").html(ipData);
						//$("#uutList").html((uutData));
					});
					//uutData += '</div>';
					console.log(Object.keys(data));
		//			jQuery.each(Object.keys(data), function(i, val) {
		//				ipData += '<span>'+val+'</span>';
		//		    });
					$("#listFa").html((uutData));
					//$("#ip_server").html(ipData);
					//$("#cutData").html(cutData);
			});
	}
}