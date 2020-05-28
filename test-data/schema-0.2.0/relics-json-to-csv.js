const Items = require('warframe-items')
const items = new Items(['All'])

console.log(items[0].category)

relics = new Set()


for(i=0; i<items.length; i++){
	if(items[i].category === 'Relics'){
		var relic = items[i].name

		if(relic.includes('Orokin') 
			|| relic.includes('Requiem')
			|| relic.includes('Derelict')
		){
			//skip these, these aren't the relic's we're interested in
			continue
		}

		var relic = relic.replace('Exceptional', '')
		var relic = relic.replace('Intact', '')
		var relic = relic.replace('Radiant', '')
		var relic = relic.replace('Flawless', '')

		relic.trim()
		relics.add(relic)
	}
}

console.log("--- List of Unique Relics ---")

for(let r of relics){
	console.log(r)
}



