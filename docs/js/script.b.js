var serverURL = "https://data.learninginventions.org/channels/";
var getDatepicker=[];
var valueplot = [];
var unitUsedAllInRoom =[[],[]];

var saveData = [{"name":"sumAllUnit","value":"0"},{"name":"avgAllUnit","value":"0"}];
var roomValue = [];
var lastUpdate = 0;
var start = moment().subtract(30, 'days');
var end = moment();

var offsetChannel = 101;
var roomData = [];
createChart2 =  function () {
    $('#container').highcharts({
        chart: {
            type: 'bar',
            height: "800"
        },
        title: {
            text: null
        },
        xAxis: {
            categories: unitUsedAllInRoom[0],
            labels: {
                style: { "fontSize": "18px", "fontWeight": "bold" },
                formatter: function () {
                    return '<a href="'+"meter.html?&roomID=" + this.value + '"target="_blank">' + this.value + '</a>';
                },
                useHTML: true
            },
            title: {
                text: null

            }
        },
        yAxis: {
            plotLines: [{
                value: 0,
                width: 2,
                color: 'white'
            }],
            min: 0,
            opposite:true,
            title: {
                text: 'Unit (KWh)',
                align: 'low',
                enabled: "bottom",
                margin: 20,
                offset: undefined,
                style: { "fontSize": "18px", "fontWeight": "bold" },
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            valueSuffix: ' KWh',
            style: {
                padding: 10,
                fontSize: "16px",
            },
            shared: true,
            useHTML: true,
            headerFormat: '<center><big>{point.key}</big><br/>',
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>',
            footerFormat: '</center>',
            valueDecimals: 2
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                },
                series: {
                pointWidth: 40//width of the column bars irrespective of the chart size
            }
        }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            floating: true,
            borderWidth: 1,
            backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
            shadow: true,
            itemStyle: {
                color: '#000000',
                fontSize: "16px",

            }
        },
        credits: {
            enabled: false
        },
        series: [{name:'Unit',data:unitUsedAllInRoom[1]}]
    });
}





function getTimedate() {
    var json = (function () {
        var json = null;
                    $.ajax({
                        'async': false,
                        
                        'url': "js/config.json",
                        'dataType': "json",
                        'success': function (data) {
                            json = data.room;
                        }
                    });
                return json;
    })(); 
    roomData = json;
    start = getUrlParameter('start');
    end = getUrlParameter('end');
    start = (typeof start == 'string') ? moment(decodeURI(start)) : moment().subtract(30, 'days');
    end = (typeof end == 'string') ? moment(decodeURI(end)) : moment();
    initDatePicker();
    document.getElementById("container").innerHTML = "Please wait a moment";
    cb(start, end);  

}

function cb(start, end) {
    console.log("complete");
    $('#reportrange span').html(start.format('MMMM D, YYYY') + ' to ' + end.format('MMMM D, YYYY'));
       // console.log(moment(start).format('YYYY-MM-DD HH:mm:ss'))
        //console.log(moment(end).format('YYYY-MM-DD HH:mm:ss'))
    

        fetchData({results : 1, end:moment(getTimezone(start)).format('YYYY-MM-DD HH:mm:ss'), type:'unit_start'});
        fetchData({results : 1, end:moment(getTimezone(end)).format('YYYY-MM-DD HH:mm:ss'), type:'unit_end'});
        
        return;
        //Fetch channel information

    }


function initDatePicker(){
        $('#reportrange').daterangepicker({
            startDate: start,
            endDate: end,
            ranges: {
             'Today': [moment().startOf('day'), moment()],
             'Yesterday': [moment().subtract(1, 'days').startOf('day'), moment().subtract(1, 'days').endOf('day')],
             'Last 7 Days': [moment().subtract(6, 'days'), moment()],
             'Last 30 Days': [moment().subtract(29, 'days'), moment()],
             'This Month': [moment().startOf('month'), moment().endOf('month')],
             'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
         },
         timePicker: true,
         timePicker24Hour: true,
     }, function(start,end){
        //console.log(end)
        setQueryParameters({start:start.format('YYYY-MM-DD HH:mm:ss'),end:end.format('YYYY-MM-DD HH:mm:ss')})
    });
}

function setQueryParameters(params) {
      var query = [],
      key, value;
      for(key in params) {
        if(!params.hasOwnProperty(key)) continue;
        value = params[key];
        query.push(key + "=" + value);
    }

    location.search = query.join("&");
}

function fetchData(option){
    //console.log("Loading...");
    
    var roomCounter = 0;

    $.each(roomData, function(room_index, room){
        var sensorCounter = 0;

        $.each(room.list, function(sensor_index, sensor){
            option          = option || {results : 1};
            var channelID   = sensor.channels;
            var field       = option.field || 1;
            var fetch_url   = serverURL+channelID+'/field/'+field+'.json?'+$.param(option);
            room.sum_unit_used = 0;    
            $.getJSON(fetch_url, function (data) {
                sensor[option.type] = (data.feeds.length > 0 ) ? Number(data.feeds[0].field1) : 0;
                if (option.type=='unit_end'){
                    sensor.unit_used = (sensor.unit_end >= sensor.unit_start ) ? (sensor.unit_end - sensor.unit_start):0;
                     room.sum_unit_used += sensor.unit_used;
                    // roomData1.push(room.sum_unit_used);
                    
                    
                }

                }).complete(function() { 
                    sensorCounter += 1;
                    if (sensorCounter === room.list.length) {
                        roomCounter += 1;
                        if (option.type=='unit_end' && roomCounter == roomData.length) {
                            // console.log(roomData);
                            startSort();
                        }    
                    } 
                });
            });
        });
    

    return;
}

function startSort(){
    
    var sorted = _.sortBy(roomData, function(room){ return -1*room.sum_unit_used; });
    unitUsedAllInRoom[0] = []
    unitUsedAllInRoom[1] = []
    for (room_index in sorted){
        var room = sorted[room_index];
        unitUsedAllInRoom[0].push(room.name);
        unitUsedAllInRoom[1].push(Number((room.sum_unit_used).toFixed(2)));
    }     
    calStatic()
    document.getElementById("lastTimeUpdate").innerHTML = end.format('DD MMMM YYYY HH:mm:ss');
    createChart2()
}
function calStatic() {
    sumValue = 0
    for (var i = 0 ; i <= unitUsedAllInRoom[1].length - 1; i++) {
      sumValue += unitUsedAllInRoom[1][i];
    };
    document.getElementById("All.value").innerHTML = sumValue.toFixed(2) + "  (kWh)" 
    document.getElementById("Avarage.value").innerHTML = (sumValue/unitUsedAllInRoom[1].length).toFixed(2)+ "  (kWh)" ;

}
function parseDataLog(data){
    var date = new Date(data.datetime);
    var localdate = date-1*date.getTimezoneOffset()*60*1000;
    data.datetime = localdate;
    data.value    = Number(data.value);
    return data;
}

function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    var datas = {};
    for (var i = 0; i < sURLVariables.length; i++)
    {
        var sParameterName = sURLVariables[i].split('=');
        datas[sParameterName[0]] = sParameterName[1];
        if (sParameterName[0] == sParam)
        {
            return sParameterName[1];
        }
    }
    return datas;
}
function getTimezone(data) {
	var date = new Date(data);
	var localdate = date-(-1*date.getTimezoneOffset()*60*1000);
	return localdate;
}
