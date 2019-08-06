var id = null

function uploadGeoFile() {
	move()
	$('#geofile_error').empty().hide()
	let form = new FormData();
    form.append('geofile', document.getElementById('geofile').files[0])
    $.ajax({
        type:'POST',
        url: "/upload/geofile",
        processData : false,
        contentType : false,
        data: form,
		statusCode: {
            400: function(xhr, textStatus) {
            	$('#geofile_error').html(xhr.responseText.split(":")[1].replace('["', '').replace('"]}','')).show()
            	$('.result-container').hide()
            }
        },
        success: function (response) {
            $('#geofile_error').empty().hide()
            $('#geofile').val('')
            clearInterval(id)
            var elem = document.getElementById("myBar")
            elem.style.width = '100%' 
      		elem.innerHTML = '100%'
      		$('#progress-text').html('Completed. Rendering data')
            setTimeout(() => {
            	update_result(response)
            	$('.modal').hide()
			}, 1000)
            
        },
    });
    return false
}

function update_result(response) {
	$('.result-container').show()
    $('#tbody').empty()
    var tbody = document.getElementById('tbody')
    var resp = ''
    for (let index=0; index < response.data.length; index++) {
    	let row = response.data[index]
        let tr = "<tr>"
        tr += "<td>" + row.address + "</td>"
        tr += "<td>" + row.lat + "</td>"
        tr += "<td>" + row.lng + "</td>"
        tr += '<td><a href="https://www.google.com/maps/@'+row.lat+',' + row.lng +',15z">Open in Maps</td>'
        tr += '</tr>'
        resp += tr
    }
    tbody.innerHTML = resp
    document.getElementById('coorindates').href = response.filepath
}

function move() {
	$('.modal').show()
  	var elem = document.getElementById("myBar");   
  	var width = 1;
  	id = setInterval(frame, 10);
  	function frame() {
    	if (width >= 98) {
      		clearInterval(id);
    	} else {
      		width++; 
      		elem.style.width = width + '%'; 
      		elem.innerHTML = width * 1  + '%';
      		if (width === 30) {
      			$('#progress-text').html('Upload success')
      		} else if (width === 40) {
      			$('#progress-text').html('Reading file')
      		} else if (width === 60) {
      			$('#progress-text').html('Getting coorindates for locations')
      		}
    	}
  	}
}



