
/*
Represents a relic that is either checked (owned) in its corresponding
checkbox element or unchecked (not owned)
*/
class RelicCheckState {
	relicId;
	isChecked;
	constructor(relicId, isChecked){
		this.relic_id=relicId
		this.isChecked=isChecked
	}
}

/*
Returns a list of RelicCheckStates. Each element
representing a relic that is either owned or not owned
by the user based on 'My Inventory' client-side state.
*/
function getRelicCheckStates(){
	$relicCheckBoxes = $('.relic input:checkbox')

	var relicCheckStates = []

	$relicCheckBoxes.each(
		function(index, value){
			relicCheckState = new RelicCheckState(value.id, value.checked)
			relicCheckStates.push(relicCheckState)
		}
	)

	return relicCheckStates
}

$('#save button').on('click', function(event){
	relicCheckStates = getRelicCheckStates()
	var jsonStr = JSON.stringify(relicCheckStates)
	console.log("[jsonStr:"+jsonStr+"]")

	var saveUrl = $(".relics-container").attr('data-save-url')
	console.log("$saveUrl = " + saveUrl)
	$.ajax({
		url: saveUrl,
		data: {'relicCheckStates': relicCheckStates},
		type: 'PUT',
		dataType: 'json',
		success: function(data) {
			console.log("successful ajax call")
		},
		error: function(data){
			console.log("ajax call failed")
		}
	});
});