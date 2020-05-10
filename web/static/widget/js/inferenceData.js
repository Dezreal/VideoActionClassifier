var data_json = {};

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

function update_data_json() {
    $.ajax({
        type: 'get',
        url: '/analysis',
        async: false,
        dataType : "json",
        success: function(result) {
            data_json = result;
        }
    });
}
update_data_json();

var inferenceData = {};

//pie Chart sample data and options
inferenceData.constructPieChartData = function() {
    n = [0, 0, 0, 0, 0, 0, 0, 0, 0];
    for (index in data_json["result"]) {
        for (var i = 0; i < 9; i++) {
            if (data_json["result"][index] == action_name[i]) {
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
//[{
//	data : [[0, 4]],
//	label : "Comedy"
//}, {
//	data : [[0, 3]],
//	label : "Action"
//}, {
//	data : [[0, 1.03]],
//	label : "Romance",
//	pie : {
//		explode : 50
//	}
//}, {
//	data : [[0, 3.5]],
//	label : "Drama"
//}];

inferenceData.pieChartOptions = {
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

//Pie chart sample data ends here

//bar Chart sample data and options

inferenceData.constructBubbleChartData = function() {
    var d1 = [];
	var result = data_json["result"];
	var detail = data_json["detail"];
	for (var i = 0; i < result.length; i++) {
	    var n = 0;
	    for (var j = 0; j < 9; j++) {
	        if (result[i] == action_name[j]) {
	            n = j;
	            break;
	        }
	    }
	    d1.push([i + 1, n, detail[i][n] * 10]);
	}
	return [d1];
//
//	var d1 = [];
//	var d2 = []
//	var point
//	var i;
//
//	for ( i = 0; i < 10; i++) {
//		point = [i, Math.ceil(Math.random() * 10), Math.ceil(Math.random() * 10)];
//		d1.push(point);
//
//		point = [i, Math.ceil(Math.random() * 10), Math.ceil(Math.random() * 10)];
//		d2.push(point);
//	}
//	return [d1, d2];
};

inferenceData.bubbleChartOptions = {
	bubbles : {
		show : true,
		baseRadius : 5
	},
	xaxis : {
		min : 0,
//		max : 14
	},
	yaxis : {
		min : -2,
		max : 8
	},
	mouse : {
		track : true,
		relative : true
	}
};

//bar chart sample data ends here

//bar Chart sample data and options

inferenceData.constructBarChartData = function() {
	var d1 = [];
	var result = data_json["result"];
	var detail = data_json["detail"];
	for (var i = 0; i < result.length; i++) {
	    var n = 0;
	    for (var j = 0; j < 9; j++) {
	        if (result[i] == action_name[j]) {
	            n = j;
	            break;
	        }
	    }
	    d1.push([detail[i][n], i + 1]);
	}
	return [d1];
};

inferenceData.barChartOptions = {
	bars : {
		show : true,
		horizontal : true,
		shadowSize : 0,
		barWidth : 0.5
	},
	mouse : {
		track : true,
		relative : true
	},
	yaxis : {
		min : 0,
		autoscaleMargin : 1
	}
};

//bar chart sample data ends here

//line Chart sample data and options

inferenceData.constructLineChartData = function() {
    var detail = data_json["detail"];
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


inferenceData.lineChartOptions = {
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

//inferenceData.constructTableWidgetData = function(){
//	return ["Trident"+Math.ceil(Math.random() * 10), "IE" + Math.ceil(Math.random() * 10), "Win"+Math.ceil(Math.random() * 10)]
//};

inferenceData.constructTableWidgetData = function() {
    var aaDataResult = [];
    for (var i = 0; i < data_json["result"].length; i++) {
        aaDataResult.push([i+1, data_json["result"][i]])
    }
    return aaDataResult;
}

inferenceData.tableWidgetData = {
    "aaData": inferenceData.constructTableWidgetData(),
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

inferenceData.constructImgData1 = function() {
    var code = data_json['code']
    if (code == false) {
        return ""
    }
    return "data:image/jpeg;base64," + code[0];
};

inferenceData.constructImgData2 = function() {
    var code = data_json['code']
    if (code == false) {
        return ""
    }
    return "data:image/jpeg;base64," + code[1];
};