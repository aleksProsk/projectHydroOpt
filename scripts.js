$(document).ready(function () {
	function updateLabelsMargin() {
        if (document.body.style.visibility == "hidden") {
			window.setTimeout(updateLabelsMargin, 100);
			return;
        }
        var labels = document.getElementsByTagName('label');
        var was = new Map();
        for (var i = 0; i < labels.length; i++) {
            temp = document.createElement("P");
            temp.style.margin = '0';
            temp.style.height = '0';
            labels[i].appendChild(temp);
            if (labels[i].className.length == 0) {
                continue;
            }
            var cur = 0;
            var nums = labels[i].className.split('-');
            if (was.has(labels[i].className)) {
                cur = was.get(labels[i].className);
            }
            labels[i].style.marginBottom = (35 * parseInt(nums[cur] - 1) + 13).toString() + 'px';
            was.set(labels[i].className, cur + 1);
        }
        return;
    }

    updateLabelsMargin();
});