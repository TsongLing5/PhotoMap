mapsFrame='''<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no, width=device-width">
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
</head>
<body>
<div id="container"></div>
<script src="https://webapi.amap.com/maps?v=1.4.15&key=您申请的key值"></script>
<script>
var markerArr = [];
    var lon=113,lat=22;           
    var map = new AMap.Map('container', {
        center: [lon, lat],
        layers: [new AMap.TileLayer()], 
        zoom: 13
    });
     AMap.plugin([
        'AMap.ToolBar',
    ], function(){
        // 在图面添加工具条控件，工具条控件集成了缩放、平移、定位等功能按钮在内的组合控件
        map.addControl(new AMap.ToolBar({
            // 简易缩放模式，默认为 false
            liteStyle: true
        }));
    });

      var marker = new AMap.Marker({
    position: new AMap.LngLat(113.94930470452066, 22.486056774576173),   // 经纬度对象，也可以是经纬度构成的一维数组[116.39, 39.9]
    title: '深圳湾'
    });

      map.add(marker);

      //add points
      for (var i = 0; i < markerArr.length; i++) {  
        var marker = new AMap.Marker({
    position: new AMap.LngLat(markerArr[i].point.split(",")[0], markerArr[i].point.split(",")[1]),   // 经纬度对象，也可以是经纬度构成的一维数组[116.39, 39.9]
    title: markerArr[i].title.split(":")[0]
    });
    map.add(marker);
            }
// 将创建的点标记添加到已有的地图实例：

// 移除已创建的 marker

</script>
</body>

</html>'''