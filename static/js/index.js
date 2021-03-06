// DO NOT DELETE
// IS REQUIRED FOR CORRECT CSRF in AJAX
$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
     	"{% csrf_token %}"
         xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
         // console.log(Cookies.get('csrftoken'))
     } 
});


function loadDefaultImage() {
	img = document.getElementById("mainImage")
	canvas = document.getElementById("canvas")
	canvas.width = canvas.getBoundingClientRect().width
	canvas.height = canvas.getBoundingClientRect().height

	W = canvas.width
	H = canvas.height

	canvas.getContext('2d').drawImage(img,0,0, 
		canvas.getBoundingClientRect().width,
		canvas.getBoundingClientRect().height);
}


function initImage(input) {
        $('.button').show();
	if (!(input.files && input.files[0])) {
		return
	}

	var canvas = document.getElementById("canvas")
	var ctx = canvas.getContext("2d")

	var fileReader = new FileReader()
	fileReader.onload = function () {
		var img = new Image()


		img.onload = function() {
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

		$('#inpaintButton').prop("disabled", false)
		$('#undoButton').prop("disabled", false)
		$('#detectButton').prop("disabled", false)
		$('#saveButton').prop("disabled", false)
	}
	fileReader.readAsDataURL(input.files[0])

	// document.getElementById("mainBlock").style.display = "block"
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
	var canvas = $("#canvas")

	var ctx = document.getElementById("canvas").getContext("2d")
	var image = ctx.getImageData(0, 0, W, H)
	var data = image.data

	var maskImage = maskCtx.getImageData(0, 0, W, H)

	var offset = canvas.offset()

	pos_x = Math.trunc(event.pageX - offset.left)
	pos_y = Math.trunc(event.pageY - offset.top)

	// TODO: fix index out of bounds
	for (var j = pos_x - r; j < pos_x + r; j++) {
		for (var i = pos_y - r; i < pos_y + r; i++) {
			data[i * 4 * W + j * 4] = 255
			data[i * 4 * W + j * 4 + 1] = 255
			data[i * 4 * W + j * 4 + 2] = 255

			maskImage.data[i * 4 * W + j * 4] = 255
			maskImage.data[i * 4 * W + j * 4 + 1] = 255
			maskImage.data[i * 4 * W + j * 4 + 2] = 255
		}
	}

    ctx.putImageData(image, 0, 0)
    maskCtx.putImageData(maskImage, 0, 0)
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
		data: source.toDataURL("image/jpeg")
	}).fail(function(response) {
		console.error("Failed to upload ficture")
	}).done(function(response) {
		hook(response)
	})

	var modal = $("#detectObjectsModal")
	var modalBody = $("#modalBody")

	modalBody.empty()
	modalBody.append("<p>Sending image...")
	modal.modal('toggle')
}

function detect(fileDir) {
	var modal = $("#detectObjectsModal")
	var modalBody = $("#modalBody")

	modalBody.empty()
	modalBody.append("<p>Detecting objects. Please wait...")

	$.get("/photo_corrector/detect/", {path: fileDir})
		.fail(function(response) {
			var modalBody = $("#modalBody")
			modalBody.empty()
			modalBody.append("<p>Error occured while detecting objects")

			console.error("Failed to detect objects")
			console.log(response)
		}).done(function(response) {
			var modal = $("#detectObjectsModal")
			var modalBody = $("#modalBody")
			var modalContent = $("#modalContent")

			modalBody.empty()
			modalBody.append("<table>")

			var arr = response.split(';')

			if (arr.length != 0) {
				modal.css("height", `${Math.min(800, 400 * Math.max(1, arr.length / 3))}px`)
			}

			var toAppend = ``

			for (var i = 0; i < arr.length; i++) {
				if (i % 3 == 0) {
					if (i == 0) {
						toAppend += "<tr>"
					} else {
						toAppend += "</tr><tr>"
					}
				}
				var s = arr[i]
				var imageId = "modalImage_" + i

				toAppend += "<td>"
				toAppend += `<img id="${imageId}" src="${s}" height=200 width=300></img>`
				toAppend += `<input type="checkbox" class="form-check-input" id="checkbox_${i}"/>`
				toAppend += `</td>`
			}

			toAppend += "</tr></table>"
			modalBody.append(toAppend)

			for (var i = 0; i < arr.length; i++) {
				$(`#modalImage_${i}`).on('click', function(event) {
					var checkobxIdx = "checkbox_" + event.target.id.split("_")[1]
					var checkbox = $(`#${checkobxIdx}`)
					checkbox.prop("checked", !checkbox.prop("checked"))
				})
			}

			$("#applyButton").on('click', function(event) {
				var checkboxes = document.querySelectorAll("input[id^='checkbox_']")

				modalBody.empty()
				modalBody.append("<p>Server is processing yout request. Please wait...")

				console.log(checkboxes)

				var indexes = ""
				checkboxes.forEach(checkbox => {
					if (checkbox.checked) {
						indexes = indexes + checkbox.id.split('_')[1] + ":"
					}
				})

				inpaint(fileDir, indexes)
			})
		})
}

function inpaint(fileDir, maskIdx) {
	var modal = $("#detectObjectsModal")
	var modalBody = $("#modalBody")

	modalBody.empty()
	modalBody.append("<p>Inpainting. Please wait...")

	var idx = -1
	if (maskIdx) {
		idx = maskIdx
	}

	console.log("maskIdx")
	console.log(maskIdx)

	$.ajax({
		type: "POST",
		url: "/photo_corrector/inpaint/",
		data: {
			dir: fileDir,
			idx: maskIdx,
			mask: mask.toDataURL("image/jpeg")
		}
	}).fail(function(response) {
		console.error("Failed to inpaint")
		$("#modalBody").empty()
		$("#modalBody").append("Server error. Please try with other with other image or mask.")
	}).done(function(response) {
		loadImageFromPath(response)
		$("#detectObjectsModal").modal('hide')
	})
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
