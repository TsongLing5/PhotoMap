import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

mapsFrame = '''<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no, width=device-width">
    <title>卫星图</title>
    <link rel="stylesheet" href="https://a.amap.com/jsapi_demos/static/demo-center/css/demo-center.css"/>
    <style>
        html,body,#container{
            height:100%;
            width:100%;
        }
    </style>
    <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
  <title>卫星图</title>
    <style>
        html,
        body,
        #container {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
        }
    </style>
        <script>
        window.onload = function () {
            new QWebChannel(qt.webChannelTransport, function (channel) {
                window.pyjs = channel.objects.pyjs;
                pyjs.myHello(alert);
            });
        }
    </script>
</head>
<body>
<div id="container"></div>
<div class="info" id="text">
    请点击覆盖物试试
</div>

<script type="text/javascript" src="https://webapi.amap.com/maps?v=1.4.15&key=您申请的key值"></script>
<script src="https://a.amap.com/jsapi_demos/static/demo-center/js/demoutils.js"></script>
<script language="javascript" src="./qwebchannel.js"></script>
<script language="javascript" src = "./control.js"></script>
<script type="text/javascript">
    //初始化地图对象，加载地图

    //var my_object = channel.objects.MyObject;

var markerArr = [];
    var lon=113,lat=22;
    var map = new AMap.Map('container', {
        center: [lon, lat],                   //map center
        layers: [new AMap.TileLayer()],  //layer set
        zoom: 13,
      resizeEnable: true
    });
  //   var marker = new AMap.Marker({
  //       map: map,
  //
  //       position: [116.405467, 39.907761]
  //
  //   });
  // marker.content='222'
  //   //map.setFitView();
  //
  //
  //
  //    marker.on('click', showInfoM);
  //
  //
  // var marker = new AMap.Marker({
  //       map: map,
  //
  //       position: [116.405467, 39.807761]
  //
  //   });
  // marker.content='??sd?'
  // marker.on('click', showInfoM);
    //map.setFitView();

    // var marker = new AMap.Marker({
    // position: new AMap.LngLat(113.94930470452066, 22.486056774576173),   // 经纬度对象，也可以是经纬度构成的一维数组[116.39, 39.9]
    // title: '深圳湾'
    // });
    // map.add(marker);
    for (var i = 0; i < markerArr.length; i++) {
    //     var marker = new AMap.Marker({
    // position: new AMap.LngLat(markerArr[i].point.split(",")[0], markerArr[i].point.split(",")[1]),   // 经纬度对象，也可以是经纬度构成的一维数组[116.39, 39.9]
    // title: markerArr[i].title.split(":")[0]
    // });
    // map.add(marker);
          var marker = new AMap.Marker({
        map: map,

        position: [markerArr[i].point.split(",")[0], markerArr[i].point.split(",")[1]] , //marker locatin
        title:    markerArr[i].title.split(":")[0]

    });
      marker.content= markerArr[i].title.split(":")[0]
      marker.on('click', showInfoM);
            }

  //   var marker = new AMap.Marker({
  //       map: map,
  //
  //       position: [116.405467, 39.807761]
  //
  //   });
  // marker.content='??sd?'
  // marker.on('click', showInfoM);




    function showInfoM(e){

        var text = '您在 [ '+e.lnglat.getLng()+','+e.lnglat.getLat()+' ] 的位置点击了marker！'
    var text = e.target.content
        //control.sendData(text);
        //onShowMsgBox();
       // control.sendData(text);
       qt5test(text);
        document.querySelector("#text").innerText = text;
        //my_object.consolePrint(text);
    }




    // 给按钮绑定事件

</script>
<script>
    function qt5test(msg) {
       pyjs.myTest(msg);
    
    }
    function uptext(msg) {
        document.getElementById('test').innerHTML=msg;
    }
</script>
</body>
</html>'''