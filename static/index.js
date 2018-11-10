// DO NOT DELETE
// IS REQUIRED FOR CORRECT CSRF in AJAX
$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});


function initImage(input) {
	if (!(input.files && input.files[0])) {
		return
	}

	var canvas = document.getElementById("canvas")
	var ctx = canvas.getContext("2d")

	var fileReader = new FileReader()
	fileReader.onload = function () {
		var img = new Image()


		img.onload = function() {
			W = img.width
        	H = img.height

        	canvas.width = W
        	source.width = W
        	mask.width = W
        	canvas.height = H
        	source.height = H
        	mask.height = H

        	ctx.drawImage(img, 0, 0, W, H)

        	var imageData = ctx.getImageData(0, 0, W, H)
        	sourceCtx.putImageData(imageData, 0, 0)
        	maskCtx.putImageData(imageData, 0, 0)

        	clearMask()
		}

		img.src = fileReader.result
	}
	fileReader.readAsDataURL(input.files[0])

	document.getElementById("mainBlock").style.display = "block"
}

function clearMask() {
	var maskData = maskCtx.getImageData(0, 0, W, H)
	var data = maskData.data
    for (var i = 0; i < data.length; i += 4) {
    	data[i] = 0
        data[i + 1] = 0
        data[i + 2] = 0
	}
	
	maskCtx.putImageData(maskData, 0, 0)
}

function wipePixels(event) {
	var ctx = document.getElementById("canvas").getContext("2d")
	var image = ctx.getImageData(0, 0, W, H)
	var data = image.data

	pos_x = event.offsetX?(event.offsetX):event.pageX-img.offsetLeft
	pos_y = event.offsetY?(event.offsetY):event.pageY-img.offsetTop

	// TODO: fix index out of bounds
	for (var j = pos_x - r; j < pos_x + r; j++) {
		for (var i = pos_y - r; i < pos_y + r; i++) {
			data[i * 4 * image.width + j * 4] = 255
			data[i * 4 * image.width + j * 4 + 1] = 255
			data[i * 4 * image.width + j * 4 + 2] = 255
			data[i * 4 * image.width + j * 4 + 3] = 255
		}
	}

    ctx.putImageData(image, 0, 0)
 }

function copyResultToSource(event) {
	var canvas = document.getElementById("canvas")
	sourceCtx.putImageData(canvas.getContext('2d').getImageData(0, 0, W, H), 0, 0)
}

function showSource() {
	clearMask()
	var ctx = document.getElementById("canvas").getContext("2d")
	ctx.putImageData(sourceCtx.getImageData(0, 0, W, H), 0, 0);
}

function saveImage(hook) {
	$.ajax({
		type: "POST",
		url: "/photo_corrector/upload/",
		data: source.toDataURL()
	}).fail(function(response) {
		console.error("Failed to upload ficture")
	}).done(function(response) {
		hook(response)
	})
}

function detect(fileDir) {
	console.log(fileDir)
	return
}

function inpaint(fileDir) {
	$.ajax({
		type: "POST",
		url: "/photo_corrector/inpaint/",
		data: {
			dir: fileDir,
			mask: mask.toDataURL()
		}
	}).fail(function(response) {
		console.error("Failed to inpaint")
	}).done(function(response) {
		loadImageFromPath(response)
	})

	return
}

function loadImageFromPath(path) {
	var img = new Image()
	img.width = W
	img.height = H

	img.onload = function() {
		var ctx = document.getElementById("canvas").getContext("2d")
		ctx.drawImage(img, 0, 0)
	}
	img.src = path
}