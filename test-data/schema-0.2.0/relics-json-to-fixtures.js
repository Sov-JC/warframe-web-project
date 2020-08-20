// NodeJS file to create a fixtures for all relics in the game
// using warframe-items NodeJS package.

const Items = require('warframe-items')
const items = new Items(['All'])

console.log(items[0].category)

relics = new Set()

// Extract all the relics and place them in the 'relics' set
for(i=0; i<items.length; i++){
	if(items[i].category === 'Relics'){
		var relic = items[i].name

		if(relic.includes('Orokin') 
			|| relic.includes('Requiem')
			|| relic.includes('Derelict')
		){
			// Skip these, these aren't the relic's we're interested in
			continue
		}

		var relic = relic.replace('Exceptional', '')
		var relic = relic.replace('Intact', '')
		var relic = relic.replace('Radiant', '')
		var relic = relic.replace('Flawless', '')

		relic = relic.trim()
		relics.add(relic)
	}
}

console.log("--- List of Unique Relics ---")

//Generate the text for the fixture of the relics
i=1
fixture = []
for(let r of relics){
	MODEL_NAME = 'relicinventory.relic'
	var modelFields = {relic_name:r, wiki_url:"#"}
	var primaryKey = i
	var modelName = MODEL_NAME

	row = {model: modelName, pk: primaryKey, fields: modelFields}

	console.log("Adding row: " + row.model + " | " + row.pk)

	fixture.push(row)

	i+=1
}

//Create and save the fixtures as a json file in this directory
const fs = require('fs')
const storeData = (data, path) => {
  try {
    fs.writeFileSync(path, JSON.stringify(data))
  } catch (err) {
    console.error(err)
  }
}

//If you run the code below, it will replace relics-fixture.json. If you do so,
//make sure you visit a site to 'pretty up' the json if you decide to generate 
//the fixtures again by using a web based "beautify" services.
storeData(fixture, 'relics-fixture.json')