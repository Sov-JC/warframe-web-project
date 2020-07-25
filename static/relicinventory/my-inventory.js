// Show type constants
var SHOW_CHECKED = "Show Checked"
var SHOW_ALL = "Show All"
var SHOW_UNCHECKED = "Show Unchecked"


function show(showTypeConstant){
	/*Filter the list of relics by the show type constants.
	For example, show(SHOW_CHECKED) displays all the relics that are
	checked.
	*/
	var RELIC_CHECKBOX_DEFAULT_DISPLAY = "block"
	

	$(".relics-container .relic").filter(
		function(index, element){
			//The relic's corresponding checkbox
			elCheckbox = element.firstElementChild

			var checked = elCheckbox.checked

			console.log("checked[" + index + "]: " + checked)

			if(showTypeConstant === SHOW_CHECKED)
				if(checked === true)
					element.style.display = RELIC_CHECKBOX_DEFAULT_DISPLAY
				else 
					element.style.display = "none"
			else if(showTypeConstant === SHOW_UNCHECKED)
				if(checked === false){
					element.style.display = RELIC_CHECKBOX_DEFAULT_DISPLAY
				}else
					element.style.display = "none"
			else if(showTypeConstant === SHOW_ALL)
				element.style.display = RELIC_CHECKBOX_DEFAULT_DISPLAY
		}
	)
}

function showUnchecked(event){
	show(SHOW_UNCHECKED)
}

function showAll(event){
	show(SHOW_ALL)
}

function showChecked(event){
	show(SHOW_CHECKED)
}

function getCheckedRelicIds(){
	//console.log("call::getCheckedRelicIds()")
	$relics = $(".relic input:checkbox")

	//console.log("$relics length is: " + $relics.length)
	$checkedRelics = $relics.filter(
		function(index, value){
			// console.log("index: " + index)
			// if(value.checked){
			// 	console.log(document.getElementById(value.id).nextElementSibling.textContent + " is checked")
			// }else{
			// 	console.log(document.getElementById(value.id).nextElementSibling.textContent + " is NOT checked")
			// }
			return value.checked
		}
	)

	var checkedRelicIds = []
	// console.log("$checkedRelics length is: " + $checkedRelics.length)
	$.each($checkedRelics, function(index, value){
		checkedRelicIds.push(parseInt(value.id))
	});

	console.log("checked relic ids::: ")
	console.log(checkedRelicIds)

	console.log("CheckedRelicIds -> " + JSON.stringify(checkedRelicIds))

	return checkedRelicIds
}

$('#save button').on('click', function(event){
	//relicCheckStates = getRelicCheckStates()
	//var jsonStr = JSON.stringify(relicCheckStates)
	//console.log("[jsonStr:"+jsonStr+"]")
	var checkedRelicIds = getCheckedRelicIds()
	var saveUrl = $(".relics-container").attr('data-save-url')
	//console.log("saveUrl = " + saveUrl)
	console.log("checkedRelicIds: ") 
	console.log(checkedRelicIds)
	console.log("typeof(checkedRelicIds)")
	console.log(typeof(checkedRelicIds))
	//JSON.stringify(checkedRelicIds)
	console.log("type of [1,2,3] is: " + typeof([1,2,3]))
	$.ajax({
		url: saveUrl,
		data: JSON.stringify(checkedRelicIds),
		type: 'PUT',
		dataType: 'json',
		timeout: 2000,
		success: function(data) {
			console.log("Successfully updated inventory.")
			//console.log("error: " + data["error"])
			//console.log("success: " + data["success"])
		},
		error: function(data){
			console.log("error: " + data["error"])
			//console.log("success: " + data["success"])
			console.log("Attempts to update inventory failed.")
		}
	});
});

// checked, all, and unchecked links
$('#all-relics').on('click', function(event){
	showAll()
	event.preventDefault()
});

$('#checked-relics').on('click', function(event){
	console.log("checked clicked")
	showChecked()
	event.preventDefault()
});
$('#unchecked-relics').on('click', function(event){
	showUnchecked()
	event.preventDefault()
});