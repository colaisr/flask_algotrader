var domane = 'https://colak.eu.pythonanywhere.com/';

if(window.location.hostname == '127.0.0.1'){
    domane = 'http://localhost:8000/';
}

$(document).ready(function () {
echartsLineChartInit();


});

function echartsLineChartInit() {
  var $lineChartEl = document.querySelector('.echart-line-chart-example');

  if ($lineChartEl) {
      $.getJSON(url, function(data) {
        data=data['historical']
        var arr = [];
        var score_arr = [];
        for (d of data)
        {
            parsed_d=Date.parse(d.date);
            arr.push( [parsed_d , d.close ]);
        }
        dateList = arr.map(function (item) {
          return item[0];
        });
        valueList = arr.map(function (item) {
          return item[1];
        });
//        hist_data=jQuery.parseJSON(hist_data)
//        for (t of hist_data){
////            if(t[1]>0){
////                parsed_d=Date.parse(t[0]);
////                score_arr.push( [parsed_d , t[1] ]);
////            }
//            parsed_d=Date.parse(t[0]);
//            score_arr.push( [parsed_d , t[1] ]);
//        }

            // Get options from data attribute
    var userOptions = utils.getData($lineChartEl, 'options');
    var chart = window.echarts.init($lineChartEl);

    var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    var data = [1272, 1301, 1402, 1216, 1086, 1236, 1219, 1330, 1367, 1416, 1297, 1204];

    var _tooltipFormatter2 = function _tooltipFormatter2(params) {
      return "\n      <div>\n          <h6 class=\"fs--1 text-700 mb-0\">\n            <span class=\"fas fa-circle me-1\" style='color:".concat(params[0].borderColor, "'></span>\n            ").concat(params[0].name, " : ").concat(params[0].value, "\n          </h6>\n      </div>\n      ");
    };

    var getDefaultOptions = function getDefaultOptions() {
      return {
        tooltip: {
          trigger: 'axis',
          padding: [7, 10],
          backgroundColor: utils.getGrays()['100'],
          borderColor: utils.getGrays()['300'],
          textStyle: {
            color: utils.getColors().dark
          },
          borderWidth: 1,
          formatter: _tooltipFormatter2,
          transitionDuration: 0,
          position: function position(pos, params, dom, rect, size) {
            return getPosition(pos, params, dom, rect, size);
          },
          axisPointer: {
            type: 'none'
          }
        },
        xAxis: {
          type: 'category',
          data: dateList,
          boundaryGap: false,
          axisLine: {
            lineStyle: {
              color: utils.getGrays()['300']
            }
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            color: utils.getGrays()['400'],
            formatter: function formatter(value) {
              return value.substring(0, 3);
            },
            margin: 15
          },
          splitLine: {
            show: false
          }
        },
        yAxis: {
          type: 'value',
          splitLine: {
            lineStyle: {
              type: 'dashed',
              color: utils.getGrays()['200']
            }
          },
          boundaryGap: false,
          axisLabel: {
            show: true,
            color: utils.getGrays()['400'],
            margin: 15
          },
          axisTick: {
            show: false
          },
          axisLine: {
            show: false
          },
          min: 600
        },
        series: [{
          type: 'line',
          data: valueList,
          itemStyle: {
            color: utils.getGrays().white,
            borderColor: utils.getColor('primary'),
            borderWidth: 2
          },
          lineStyle: {
            color: utils.getColor('primary')
          },
          showSymbol: false,
          symbol: 'circle',
          symbolSize: 10,
          smooth: false,
          hoverAnimation: true
        }],
        grid: {
          right: '3%',
          left: '10%',
          bottom: '10%',
          top: '5%'
        }
      };
    };

    echartSetOption(chart, userOptions, getDefaultOptions);

    })


  }
};