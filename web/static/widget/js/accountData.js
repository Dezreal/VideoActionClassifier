var user_data_json = {};

var action_name = {
        0: "wave 挥手",
        1: "drink from a bottle 喝水",
        2: "answer phone 接电话",
        3: "clap 拍手",
        4: "tight lace 系鞋带",
        5: "sit down 坐下",
        6: "stand up 站起",
        7: "read watch 看表",
        8: "bow 鞠躬"
};

function update_user_json() {
    $.ajax({
        type: 'get',
        url: '/account',
        async: false,
        dataType : "json",
        success: function(result) {
            user_data_json = result;
        }
    });
}
update_user_json();

var accountData = {};

//pie Chart sample data and options
accountData.constructPieChartData = function() {
    n = [0, 0, 0, 0, 0, 0, 0, 0, 0];
    var files = user_data_json['files'];
    for (index in files) {
        for (var i = 0; i < 9; i++) {
            if (files[index]['t'] == action_name[i]) {
                n[i] = n[i] + 1;
                break;
            }
        }
    }
    data = [];
    for (var i = 0; i < 9; i++) {
        data.push({
            data:[[action_name[i], n[i]]],
            label: action_name[i]
        });
    }
    return data;
};

accountData.pieChartOptions = {
	HtmlText : false,
	grid : {
		verticalLines : false,
		horizontalLines : false
	},
	xaxis : {
		showLabels : false
	},
	yaxis : {
		showLabels : false
	},
	pie : {
		show : true,
		explode : 6
	},
	mouse : {
		track : true
	},
	legend : {
		position : "se",
		backgroundColor : "#D2E8FF"
	}
};

//accountData.constructBubbleChartData = function() {
//    var d1 = [];
//	var result = data_json["result"];
//	var detail = data_json["detail"];
//	for (var i = 0; i < result.length; i++) {
//	    var n = 0;
//	    for (var j = 0; j < 9; j++) {
//	        if (result[i] == action_name[j]) {
//	            n = j;
//	            break;
//	        }
//	    }
//	    d1.push([i + 1, n, detail[i][n] * 10]);
//	}
//	return [d1];
////
////	var d1 = [];
////	var d2 = []
////	var point
////	var i;
////
////	for ( i = 0; i < 10; i++) {
////		point = [i, Math.ceil(Math.random() * 10), Math.ceil(Math.random() * 10)];
////		d1.push(point);
////
////		point = [i, Math.ceil(Math.random() * 10), Math.ceil(Math.random() * 10)];
////		d2.push(point);
////	}
////	return [d1, d2];
//};
//
//accountData.bubbleChartOptions = {
//	bubbles : {
//		show : true,
//		baseRadius : 5
//	},
//	xaxis : {
//		min : 0,
////		max : 14
//	},
//	yaxis : {
//		min : -2,
//		max : 8
//	},
//	mouse : {
//		track : true,
//		relative : true
//	}
//};

accountData.constructBarChartData = function() {
	var d1 = [];
	var group = user_data_json["group_date"];
	for (var i = 0; i < group.length; i++) {
	    d1.push([group[i]['days'], group[i]['count']]);
	}
	return [d1];
};

accountData.barChartOptions = {
	bars : {
		show : true,
		horizontal : false,
		shadowSize : 0,
		barWidth : 0.05
	},
	mouse : {
		track : true,
		relative : true
	},
	yaxis : {
//		min : 0,
		autoscaleMargin : 1
	}
};

accountData.constructLineChartData = function() {
    var l1 = [];
    if (user_data_json['last_file'] == false)
        return l1;
    var detail = user_data_json['last_file']['detail'].split(",");
    for (var i = 0; i < detail.length; i++) {
        l1.push(detail[i].split(" "))
    }
    var detail = l1;
    console.log(detail);
    var data = [];
    for (var n = 0; n < 9; n++) {
        tmp = [[0, 0]];
        for (var i = 0; i < detail.length; i++) {
            tmp.push([i + 1, detail[i][n]])

        }
        data.push(tmp);
    }
    return data;
};


accountData.lineChartOptions = {
	xaxis : {
		minorTickFreq : 4
	},
	grid : {
		minorVerticalLines : true
	},
	selection : {
		mode : "x",
		fps : 30
	}
};

//line chart sample data ends here

//table Widget sample data and options

//accountData.constructTableWidgetData = function(){
//	return ["Trident"+Math.ceil(Math.random() * 10), "IE" + Math.ceil(Math.random() * 10), "Win"+Math.ceil(Math.random() * 10)]
//};

accountData.constructTableWidgetData = function() {
    var files = user_data_json["files"];
    var aaDataResult = [];
    for (var i = 0; i < files.length; i++) {
        aaDataResult.push([files[i]['f'], files[i]['t']])
    }
    return aaDataResult;
}

accountData.tableWidgetData = {
    "aaData": accountData.constructTableWidgetData(),
	"aoColumns" : [{
		"sTitle" : "窗口"
	}, {
		"sTitle" : "预测结果"
	}],
	"iDisplayLength": 25,
	"aLengthMenu": [[1, 25, 50, -1], [1, 25, 50, "All"]],
	"bPaginate": true,
	"bAutoWidth": false
};

accountData.constructTextWidgetData = function() {
    var last = user_data_json["last_file"];
    if (last == false)
        return "尚无数据！"
    var str = "使用时间：" + last["date"] + "<br/>";
    str = str + "数据：" + last["filename"] + "<br/>";
    str = str + "预测值：" + last['result'] + '<br/>';
    return str;
}
