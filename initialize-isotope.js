$('.grid').isotope({
  // set itemSelector so .grid-sizer is not used in layout
  itemSelector: '.grid-item',
  percentPosition: true,
  masonry: {
	// use element for option
	columnWidth: '.grid-sizer'
  }
})

document.body.style.visibility = "hidden";

<!-- Automatische Groessenaenderung im Isotope-Grid^ -->
function onResize()
{		
	const wpx = $(window).width();
	const eps = 0.1;
	$('[class*="varsize"]').each(function(i,ele) {
		var x = ele.className.match(/varsize-(\d+\.?\d*)-(\d+\.?\d*)-(\d+\.?\d*)-(\d+\.?\d*)/ ).slice(1,5).map(parseFloat);									
		var s = 1;
		if (wpx < 500) {s = x[3];} else if (wpx < 1000)	{s = x[2];}
		w = s*x[0]; h = s*x[1];
		ele.style.width = Math.min(w,100)-eps + "%";
		if (x[1] > 0) {ele.style.height = h + "vw";} else {ele.style.height = "auto";}
		$(ele).height(Math.ceil($(ele).height() / 50) * 50); // snap height to 50px-grid
		$(ele).width($(ele).width() - 25 /*2*$(ele).css("border-top-width")*/); // rand abziehen von grösse todo geht nicht dynamisch
	});
	
	$('[class*="main-carousel"]').each(function(i,ele)
	{
		$(ele).flickity('resize');
	});
};
window.addEventListener('resize', onResize, true);
window.addEventListener('load', onResize, true);

//$(document).ready(function(){setTimeout(function(){onResize()}, 3000);});
//$(document).ready(function(){setTimeout(function(){window.dispatchEvent(new Event('resize')); document.body.scrollTop = document.documentElement.scrollTop = 0; document.body.style.visibility = "visible";}, 5000);});

function onReady(callback) {
    var intervalID = window.setInterval(checkReady, 1000);

    function checkReady() {
        if (
			//document.getElementsByTagName('footer')[0] !== undefined)
			//document.getElementById('_dash-app-content') !== undefined)
			document.getElementsByClassName('modebar-btn plotlyjsicon modebar-btn--logo')[0] !== undefined ||
			document.getElementsByClassName('CStopWaitingForGraphics')[0] !== undefined)
		{
            window.clearInterval(intervalID);
            callback.call(this);
        }
    }
}

function show(id, value) {
    document.getElementById(id).style.display = value ? 'block' : 'none';
}

onReady(function () {
    //show('page', true);
    //onResize();
	//$(window).trigger('resize'); //geht nicht todo (damit es in ie läuft)
	window.dispatchEvent(new Event('resize'));
	document.body.scrollTop = document.documentElement.scrollTop = 0;
	document.body.style.visibility = "visible";
});