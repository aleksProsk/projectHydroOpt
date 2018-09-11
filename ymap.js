$(document).ready(function () {
	function drawYMap() {
	    if (document.body.style.visibility == "hidden") {
			window.setTimeout(drawYMap, 100);
			return;
        }
		ymaps.ready(function() {
			var tmp = document.getElementById('ymap-container');
			if (tmp == null) {
				return;
			}
			var myMap;
			var divs = [];
			myMap = new ymaps.Map("ymap-container", {
					center: [46.864081, 8.2187543],
					zoom: 7,
					controls: []
				}, {
					searchControlProvider: 'yandex#search'
			});

			function updateMapContent(map) {
				map.geoObjects.removeAll();
				divs = document.getElementsByTagName("div");
				for (var i = 0; i < divs.length; i++) {
                    if (divs[i].id.length == 0) {
                        continue;
                    }
                    arr = divs[i].id.split('-');
                    if (arr.length > 1 && arr[0] == 'ymapsmark') {
                        var circleLayout = ymaps.templateLayoutFactory.createClass('<div class="placemark_layout_container"><div class="circle_layout">' + arr[1] + '</div></div>');
                        var drag = false;
                        if (arr.length > 4) {
                            drag = true;
                        }
                        var BalloonContentLayout;
                        var pageName = location.pathname.substring(1);
                        if (document.getElementById("revenueAndRiskGraphFigure-CHist-index") != null) {
                            BalloonContentLayout = ymaps.templateLayoutFactory.createClass(
                                '<div style="margin: 10px;">' +
                                '<b>' + arr[1] + '</b><br />' +
                                '<button onclick="location.href=\'http://localhost:5000/d/DisplayScreen@screen=details&asset=' + arr[1] + '\';">Details</button>' +
                                '</div>', {
                                    build: function () {
                                        BalloonContentLayout.superclass.build.call(this);
                                    },
                                    clear: function () {
                                        BalloonContentLayout.superclass.clear.call(this);
                                    },
                                });
                        }
                        else {
                            BalloonContentLayout = ymaps.templateLayoutFactory.createClass(
                                '<div style="margin: 10px;">' +
                                '<b>' + arr[1] + '</b><br />' +
                                '<button onclick="location.href=\'http://localhost:5000/d/DisplayScreen@screen=editor&asset=' + arr[1] + '\';">Details</button>' +
                                '</div>', {
                                    build: function () {
                                        BalloonContentLayout.superclass.build.call(this);
                                    },
                                    clear: function () {
                                        BalloonContentLayout.superclass.clear.call(this);
                                    },
                                });
                        }
                        var myGeoObject = new ymaps.GeoObject({
                            geometry: {
                                type: "Point",
                                coordinates: [parseFloat(arr[2]), parseFloat(arr[3])]
                            },
                            properties: {
                                iconContent: arr[1],
                            }
                        }, {
                            draggable: drag,
                            iconLayout: circleLayout,
                            iconShape: {
                                type: 'Circle',
                                coordinates: [0, 0],
                                radius: 25
                            },
                            balloonContentLayout: BalloonContentLayout,
                            balloonPanelMaxMapArea: 0
                        });
                        myGeoObject.events.add("dragend", function (e) {
                            coords = this.geometry.getCoordinates();
                            console.log(this.properties.get('iconContent'));
                            console.log(coords);
                            $.post("/postmethod", {
                                shortname: this.properties.get('iconContent'),
                                lat: coords[0],
                                lon: coords[1],
                            });
                        }, myGeoObject);
                        myMap.geoObjects.add(myGeoObject);
                    }
                }
			}

			elem = document.getElementById('ymap-placemarks-container');
			elem.addEventListener("DOMSubtreeModified", function (e) {
			    updateMapContent(myMap);
            }, false);

			updateMapContent(myMap);
		});
	};
	drawYMap();
});
