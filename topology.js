$(document).ready(function () {
	function drawTopology() {
        if (document.body.style.visibility == "hidden") {
            window.setTimeout(drawTopology, 100);
            return;
        }

        var tmp = document.getElementById('fabricjs-canvas');
        if (tmp == null) {
            return;
        }
        var canvas = new fabric.Canvas('fabricjs-canvas', { width: 800, height: 450 });
        fabric.Object.prototype.originX = fabric.Object.prototype.originY = 'center';
        canvas.selection = false;

        var redact = document.getElementById("fabricjs-redactor");
        var redactor = false;
        if (redact != null) {
            redactor = true;
        }
        function makeTurbine(left, top, linesTo, linesFrom, text, id) {
            var c = new fabric.Rect({
              strokeWidth: 3,
              width: text.length * 25,
              height: 30,
              fill: '#fff',
              stroke: '#201BB5',
              originX: 'center',
              originY: 'center',
              rx: 5,
            });
            c.hasControls = c.hasBorders = false;
            var t = new fabric.Text(text, {
                fontFamily: 'Arial',
                fontSize: 25,
                textAlign: 'center',
                originX: 'center',
                originY: 'center',
            });
            var g = new fabric.Group([c, t],{
              left: left,
              top: top,
                selectable: true,
                lockMovementX: !redactor,
                lockMovementY: !redactor,
            });
            g.linesTo = linesTo;
            g.linesFrom = linesFrom;
            g.hasControls = g.hasBorders = false;
            g.setShadow({
                color: 'rgba(0,0,0,1)',
                offsetX: 1,
                offsetY: 1,
                blur: 5,
            });
            g.name = text;
            g.id = id;
            g.typ = 'turbine';
            return g;
        }

        function makeReservoir(left, top, linesTo, linesFrom, text, id) {
            var c = new fabric.Rect({
              strokeWidth: 3,
              width: text.length * 25,
              height: 30,
              fill: '#fff',
              stroke: '#51A5E5',
              originX: 'center',
              originY: 'center',
              rx: 5,
            });
            c.hasControls = c.hasBorders = false;
            var t = new fabric.Text(text, {
                fontFamily: 'Arial',
                fontSize: 25,
                textAlign: 'center',
                originX: 'center',
                originY: 'center',
            });
            var g = new fabric.Group([c, t],{
              left: left,
              top: top,
                selectable: true,
                lockMovementX: !redactor,
                lockMovementY: !redactor,
            });
            g.linesTo = linesTo;
            g.linesFrom = linesFrom;
            g.hasControls = g.hasBorders = false;
            g.setShadow({
                color: 'rgba(0,0,0,1)',
                offsetX: 1,
                offsetY: 1,
                blur: 5,
            });
            g.name = text;
            g.id = id;
            g.typ = 'reservoir';
            return g;
        }

        function makePump(left, top, linesTo, linesFrom, text, id) {
            var c = new fabric.Rect({
              strokeWidth: 3,
              width: text.length * 25,
              height: 30,
              fill: '#fff',
              stroke: '#1B72B5',
              originX: 'center',
              originY: 'center',
              rx: 5,
            });
            c.hasControls = c.hasBorders = false;
            var t = new fabric.Text(text, {
                fontFamily: 'Arial',
                fontSize: 25,
                textAlign: 'center',
                originX: 'center',
                originY: 'center',
            });
            var g = new fabric.Group([c, t],{
              left: left,
              top: top,
                selectable: true,
                lockMovementX: !redactor,
                lockMovementY: !redactor,
            });
            g.linesTo = linesTo;
            g.linesFrom = linesFrom;
            g.hasControls = g.hasBorders = false;
            g.setShadow({
                color: 'rgba(0,0,0,1)',
                offsetX: 1,
                offsetY: 1,
                blur: 5,
            });
            g.name = text;
            g.id = id;
            g.typ = 'pump';
            return g;
        }

        function makeFlow(left, top, linesTo, linesFrom, text, id) {
            var c = new fabric.Rect({
              strokeWidth: 3,
              width: text.length * 25,
              height: 30,
              fill: '#fff',
              stroke: '#644CB2',
              originX: 'center',
              originY: 'center',
              rx: 5,
            });
            c.hasControls = c.hasBorders = false;
            var t = new fabric.Text(text, {
                fontFamily: 'Arial',
                fontSize: 25,
                textAlign: 'center',
                originX: 'center',
                originY: 'center',
            });
            var g = new fabric.Group([c, t],{
              left: left,
              top: top,
                selectable: true,
                lockMovementX: !redactor,
                lockMovementY: !redactor,
            });
            g.linesTo = linesTo;
            g.linesFrom = linesFrom;
            g.hasControls = g.hasBorders = false;
            g.setShadow({
                color: 'rgba(0,0,0,1)',
                offsetX: 1,
                offsetY: 1,
                blur: 5,
            });
            g.name = text;
            g.id = id;
            g.typ = 'flow';
            return g;
        }

        function makeLine(coords, clr, wdt) {
            return new fabric.Line(coords, {
              fill: clr,
              stroke: clr,
              strokeWidth: wdt,
              selectable: false
            });
        }

        function updateCanvas() {
            canvas.clear();
            divs = document.getElementById("fabricjs-objects-container").children;
            x = new Map();
            y = new Map();
            pos = new Map();
            names = new Map();
            type = new Map();
            ids = new Map();
            var cnt = 0;
            for (var i = 0; i < divs.length; i++) {
                arr = divs[i].id.split('-');
                if (arr.length > 3 && arr[0] == 'fabricjs') {
                    name = arr[2];
                    cx = parseFloat(arr[3]) * canvas.getWidth();
                    cy = parseFloat(arr[4]) * canvas.getHeight();
                    x.set(name, cx);
                    y.set(name, cy);
                    pos.set(name, cnt);
                    names.set(cnt, name);
                    ids.set(name, divs[i].id);
                    type.set(cnt, arr[1]);
                    cnt++;
                }
            }
            var edges = [];
            var edgesNums = [];
            for (var i = 0; i < cnt; i++) {
                edges.push([]);
                edgesNums.push([]);
                for (var j = 0; j < cnt; j++) {
                    edges[edges.length - 1].push(0);
                    edgesNums[edges.length - 1].push(0);
                }
            }
            for (var i = 0; i < divs.length; i++) {
                if (divs[i].id.length == 0) {
                    continue;
                }
                arr = divs[i].id.split('-');
                if (arr.length > 3 && arr[0] == 'fabricjs') {
                    name = arr[2];
                    v = pos.get(name);
                    name_from = arr[5];
                    name_to = arr[6];
                    if (name_from != 'null' && pos.has(name_from)) {
                        u = pos.get(name_from);
                        edges[u][v] = 1;
                    }
                    if (name_to != 'null' && pos.has(name_to)) {
                        u = pos.get(name_to);
                        edges[v][u] = 1;
                    }
                }
            }
            lines = [];
            for (var i = 0; i < cnt; i++) {
                for (var j = 0; j < cnt; j++) {
                    if (edges[i][j] == 0) {
                        continue;
                    }
                    name_from = names.get(i);
                    name_to = names.get(j);
                    var clr = 'grey';
                    var wdt = 4;
                    if (type.get(i) == 'reservoir' && type.get(j) == 'reservoir') {
                        clr = '#C4C3C4';
                        wdt = 3.5;
                    }
                    else if (type.get(i) == 'flow' || type.get(j) == 'flow') {
                        clr = '#C4C3C4';
                    }
                    lines.push(makeLine([x.get(name_from), y.get(name_from), x.get(name_to), y.get(name_to)], clr, wdt));
                    edgesNums[i][j] = lines.length;
                    edgesNums[j][i] = -lines.length;
                }
            }
            for (var i = 0; i < lines.length; i++) {
                canvas.add(lines[i]);
            }
            for (var i = 0; i < cnt; i++) {
                linesTo = [];
                linesFrom = [];
                for (var j = 0; j < cnt; j++) {
                    if (edgesNums[i][j] == 0) {
                        continue;
                    }
                    if (edgesNums[i][j] > 0) {
                        linesFrom.push(lines[edgesNums[i][j] - 1]);
                    }
                    else {
                        linesTo.push(lines[-edgesNums[i][j] - 1]);
                    }
                }
                typ = type.get(i);
                name = names.get(i);
                cx = x.get(name);
                cy = y.get(name);
                id = ids.get(name);
                if (typ == 'reservoir') {
                    canvas.add(makeReservoir(cx, cy, linesTo, linesFrom, name, id));
                }
                else if (typ == 'pump') {
                    canvas.add(makePump(cx, cy, linesTo, linesFrom, name, id));
                }
                else if (typ == 'turbine') {
                    canvas.add(makeTurbine(cx, cy, linesTo, linesFrom, name, id));
                }
                else {
                    canvas.add(makeFlow(cx, cy, linesTo, linesFrom, name, id));
                }
            }
        }

        updateCanvas();

        var moving = false;
        var selectedId;
        var mode = null;
        var editing = false;

        canvas.on('object:moving', function(e) {
            var container = document.getElementById("fabricjs-canvas-container");
            while (container.children.length > 2) {
                container.removeChild(container.lastChild);
            }
            moving = true;
            var p = e.target;
            if (p.linesTo != null) {
                for (var i = 0; i < p.linesTo.length; i++) {
                    p.linesTo[i].set({'x2': Math.max(p.width / 2, Math.min(p.left, canvas.width - p.width / 2)), 'y2': Math.max(15, Math.min(p.top, canvas.height - 15))});
                }
            }
            if (p.linesFrom != null) {
                for (var i = 0; i < p.linesFrom.length; i++) {
                    p.linesFrom[i].set({'x1': Math.max(p.width / 2, Math.min(p.left, canvas.width - p.width / 2)), 'y1': Math.max(15, Math.min(p.top, canvas.height - 15))});
                }
            }
            if (p.get('top') > canvas.height) {
                p.set({'top': canvas.height - 15});
            }
            else if (p.get('top') < 15) {
                p.set({'top': 15});
            }
            if (p.get('left') > canvas.width - p.width / 2) {
                p.set({'left': canvas.width - p.width / 2});
            }
            else if (p.get('left') <= p.width / 2) {
                p.set({'left': p.width / 2});
            }

            var elem = document.getElementById(p.id);
            if (elem != null) {
                elem.parentNode.removeChild(elem);
            }
            canvas.renderAll();
        });

        canvas.on('object:moved', function(e) {
            var p = e.target;
            var arr = p.id.split('-');
            newId = arr[0] + '-' + arr[1] + '-' + arr[2] + '-' + (p.get('left') / canvas.width).toString() + '-' + (p.get('top') / canvas.height).toString() + '-' + arr[5] + '-' + arr[6];
            var container = document.getElementById("fabricjs-objects-container");
            elem = document.createElement("div");
            elem.id = newId;
            container.appendChild(elem);
            updateCanvas();
        });

        canvas.on('mouse:over', function(e) {
            if (e.target == null || e.target.get('type') == 'line') {
                return;
            }
            e.target.setShadow({
                color: 'rgba(0,0,0,1)',
                offsetX: 2.5,
                offsetY: 2.5,
                blur: 5,
            });
            canvas.renderAll();
        });

        canvas.on('mouse:out', function(e) {
            if (e.target == null || e.target.get('type') == 'line') {
                return;
            }
            e.target.setShadow({
                color: 'rgba(0,0,0,1)',
                offsetX: 1,
                offsetY: 1,
                blur: 5,
            });
            canvas.renderAll();
        });

        canvas.on('mouse:up', function(e) {
            if (editing == true) {
                editing = false;
                return;
            }
            if (e.target == null || e.target.get('type') == 'line') {
                return;
            }
            if (moving == true) {
                moving = false;
                return;
            }
            var container = document.getElementById("fabricjs-canvas-container");
            while (container.children.length > 2) {
                container.removeChild(container.lastChild);
            }
            p = e.target;
            var elem = document.createElement('div');
            selectedId = e.target.id;
            arr = selectedId.split('-');
            el = document.getElementById("fabricjs-canvas");
            for (var lx=0, ly=0;
                 el != null;
                 lx += el.offsetLeft, ly += el.offsetTop, el = el.offsetParent);
            elem.style.cssText = 'position:absolute;z-index:1000000;background:white;left:'+e.pointer.x.toString()+'px;top:'+(e.pointer.y+ly).toString()+'px;box-shadow:0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);border-radius: 10px; padding: 5px';
            elem.innerHTML = p.name;
            if (redactor == false) {
                page = (((window.location.href).split('@')[1]).split('&')[0]).split('=')[1];
                if (page == 'details') {
                    elem.innerHTML += '<button onclick="$.post(\'/selectElement\', {name: \'' + p.name + '\', type: \'' + p.typ + '\'}); ' +
                        'document.getElementById(\'hiddenButton-CButton-details\').click(); ' +
                        'var container = document.getElementById(\'fabricjs-canvas-container\');' +
                        '            while (container.children.length > 2) {\n' +
                        '                container.removeChild(container.lastChild);\n' +
                        '            }">Show chart</button>';
                }
                else {
                    elem.innerHTML += '<button onclick="location.href=\'http://localhost:5000/d/DisplayScreen@' + p.name + '\';">Details</button>';
                }
            }
            elem.innerHTML += '<div id="fabricjs-closer">Close</div>';
            if (redactor == true) {
                elem.innerHTML += '<div id="fabricjs-remover">Remove</div>';
                if (arr[1] == 'reservoir') {
                    elem.innerHTML += '<div>Spills To: '+arr[6]+'<button id="fabricjs-edit-connection-to">Edit</button></div>';
                }
                else {
                    elem.innerHTML += '<div>Operates From: '+arr[5]+'<button id="fabricjs-edit-connection-from">Edit</button></div>';
                    elem.innerHTML += '<div>Operates To: '+arr[6]+'<button id="fabricjs-edit-connection-to">Edit</button></div>';
                }
            }
            container.appendChild(elem);
        });

        canvas.on('mouse:down', function(e) {
            var container = document.getElementById("fabricjs-canvas-container");
            while (container.children.length > 2) {
                container.removeChild(container.lastChild);
            }
            if (e.target == null || e.target.get('type') == 'line') {
                if (mode == "TO") {
                    var elem = document.getElementById(selectedId);
                    elem.parentNode.removeChild(elem);
                    var container = document.getElementById("fabricjs-objects-container");
                    elem = document.createElement("div");
                    arr = selectedId.split('-');
                    elem.id = arr[0] + '-' + arr[1] + '-' + arr[2] + '-' + arr[3] + '-' + arr[4] + '-' + arr[5] + '-null';
                    container.appendChild(elem);
                    updateCanvas();
                }
                else if (mode == "FROM") {
                    var elem = document.getElementById(selectedId);
                    elem.parentNode.removeChild(elem);
                    var container = document.getElementById("fabricjs-objects-container");
                    elem = document.createElement("div");
                    arr = selectedId.split('-');
                    elem.id = arr[0] + '-' + arr[1] + '-' + arr[2] + '-' + arr[3] + '-' + arr[4] + '-null-' + arr[6];
                    container.appendChild(elem);
                    updateCanvas();
                }
                mode = null;
                return;
            }
            if (mode == "TO") {
                mode = null;
                p = e.target;
                toId = p.id;
                fromId = selectedId;
                if (toId == fromId) {
                    return;
                }
                to = toId.split('-');
                from = fromId.split('-');
                var elem = document.getElementById(selectedId);
                elem.parentNode.removeChild(elem);
                var container = document.getElementById("fabricjs-objects-container");
                elem = document.createElement("div");
                arr = selectedId.split('-');
                elem.id = arr[0] + '-' + arr[1] + '-' + arr[2] + '-' + arr[3] + '-' + arr[4] + '-' + arr[5];
                if (to[1] == 'reservoir') {
                    elem.id += '-' + to[2];
                }
                else {
                    elem.id += '-null';
                }
                container.appendChild(elem);
                updateCanvas();
            }
            else if (mode == "FROM") {
                mode = null;
                p = e.target;
                toId = p.id;
                fromId = selectedId;
                if (toId == fromId) {
                    return;
                }
                to = toId.split('-');
                from = fromId.split('-');
                var elem = document.getElementById(selectedId);
                elem.parentNode.removeChild(elem);
                var container = document.getElementById("fabricjs-objects-container");
                elem = document.createElement("div");
                arr = selectedId.split('-');
                elem.id = arr[0] + '-' + arr[1] + '-' + arr[2] + '-' + arr[3] + '-' + arr[4];
                if (to[1] == 'reservoir') {
                    elem.id += '-' + to[2];
                }
                else {
                    elem.id += '-null';
                }
                elem.id += '-' + arr[6];
                container.appendChild(elem);
                updateCanvas();
            }
            return;
        });

        $(document).on("click", "#fabricjs-closer", function() {
            var container = document.getElementById("fabricjs-canvas-container");
            while (container.children.length > 2) {
                container.removeChild(container.lastChild);
            }
        });

        $(document).on("click", "#fabricjs-remover", function() {
            var container = document.getElementById("fabricjs-canvas-container");
            while (container.children.length > 2) {
                container.removeChild(container.lastChild);
            }
            var element = document.getElementById(selectedId);
            name = selectedId.split('-')[2];
            element.parentNode.removeChild(element);
            container = document.getElementById("fabricjs-objects-container");
            var divs = container.children;
            var newDivs = [];
            for (var i = 0; i < divs.length; i++) {
                arr = divs[i].id.split('-');
                newId = arr[0] + '-' + arr[1] + '-' + arr[2] + '-' + arr[3] + '-' + arr[4];
                if (arr[5] != name) {
                    newId += '-' + arr[5];
                }
                else {
                    newId += '-null';
                }
                if (arr[6] != name) {
                    newId += '-' + arr[6];
                }
                else {
                    newId += '-null';
                }
                var elem = document.createElement("div");
                elem.id = newId;
                newDivs.push(elem);
            }
            while(container.firstChild) {
                container.removeChild(container.firstChild);
            }
            for (var i = 0; i < newDivs.length; i++) {
                container.appendChild(newDivs[i]);
            }
            updateCanvas();
        });

        var cntRes = 0;
        $(document).on("click", "#fabricjs-add-reservoir", function() {
            cntRes++;
            var container = document.getElementById("fabricjs-objects-container");
            var elem = document.createElement("div");
            elem.id = "fabricjs-reservoir-"+"newR"+cntRes.toString()+"-0.5-0.5-null-null";
            container.appendChild(elem);
            updateCanvas();
        });

        var cntTurb = 0;
        $(document).on("click", "#fabricjs-add-turbine", function() {
            cntTurb++;
            var container = document.getElementById("fabricjs-objects-container");
            var elem = document.createElement("div");
            elem.id = "fabricjs-turbine-"+"newT"+cntTurb.toString()+"-0.5-0.5-null-null";
            container.appendChild(elem);
            updateCanvas();
        });

        var cntPump = 0;
        $(document).on("click", "#fabricjs-add-pump", function() {
            cntPump++;
            var container = document.getElementById("fabricjs-objects-container");
            var elem = document.createElement("div");
            elem.id = "fabricjs-pump-"+"newP"+cntPump.toString()+"-0.5-0.5-null-null";
            container.appendChild(elem);
            updateCanvas();
        });

        var cntFlow = 0;
        $(document).on("click", "#fabricjs-add-flow", function() {
            cntPump++;
            var container = document.getElementById("fabricjs-objects-container");
            var elem = document.createElement("div");
            elem.id = "fabricjs-flow-"+"newF"+cntPump.toString()+"-0.5-0.5-null-null";
            container.appendChild(elem);
            updateCanvas();
        });

        $(document).on("click", "#fabricjs-edit-connection-to", function() {
            editing = true;
            mode = "TO";
            return;
        });

        $(document).on("click", "#fabricjs-edit-connection-from", function() {
            editing = true;
            mode = "FROM";
            return;
        });

        $(document).on("click", "#fabricjs-redactor-save", function() {
            var divs = document.getElementById("fabricjs-objects-container").children;
            var names = [];
            var types = [];
            var x = [];
            var y = [];
            var operatesTo = [];
            var operatesFrom = [];
            for (var i = 0; i < divs.length; i++) {
                arr = divs[i].id.split('-');
                types.push(arr[1]);
                names.push(arr[2]);
                x.push(parseFloat(arr[3]));
                y.push(parseFloat(arr[4]));
                operatesFrom.push(arr[5]);
                operatesTo.push(arr[6]);
            }
            assetName = (window.location.href.split('&')[1]).split('=')[1];
            $.post("/postTopology", {
                names: names,
                types: types,
                x: x,
                y: y,
                operatesFrom: operatesFrom,
                operatesTo: operatesTo,
                assetName: assetName,
            });
        });

        function selectAsset(name) {
            $.post("/selectAsset", {
                name: name,
            });
            document.getElementById('hiddenButton-CButton-details').click();
        }
    }
    drawTopology();
});