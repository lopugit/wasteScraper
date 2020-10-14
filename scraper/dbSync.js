/*
- Waste Managers - 
Nikolaj Frey, Mathen Jose, Alvin Zhao
FIT3162
This program manipulates our scraped data into a suitable format
and syncs it with a MongoDB.
*/

console.log("Starting wasteScraper dbSync...")

// so process never dies
process.on('uncaughtException', function (err) {
  console.log('Caught exception: ', err);
});

console.log("Started wasteScraper dbSync!")

let fs = require('fs')
let config = require('config')

// Parse scraped data for better databasing

let json = require('../data.json')
let parsed = []

Object.keys(json).forEach((categoryName)=>{
	let category = json[categoryName]
	Object.keys(category).forEach(itemName=>{
		let item = {
			name: itemName,
			category: categoryName,
			...category[itemName]
		}

		if(item.alias){
			item.aliases = item.alias.split(",")
			
			item.aliases.forEach((e,i)=>{
				item.aliases[i] = e.trim().replace(/\w\S*/g, (w) => (w.replace(/^\w/, (c) => c.toUpperCase())));
			})

			delete item.alias
		}
		
		parsed.push(item)

	})
})

let string = JSON.stringify(parsed, null, "\t")

fs.writeFileSync(__dirname+'/../dbData.json', string)

// create mongoDB connection
let MongoClient = require('mongodb').MongoClient;
let uri = config.uri
let client = new MongoClient(uri, { 
	useNewUrlParser: true, 
	useUnifiedTopology: true 
});

// connect to mongodb connection
client.connect(async err => {
	if(err) console.error(err)
	
  let db = client.db("wastee");
	let items = db.collection("items")

	await asyncForEach(parsed, async item=>{
		let found = await items.findOneAndUpdate(
			{
				name: item.name,
				category: item.category
			}, 
			{
				$set: item
			},
			{
				upsert: true,
				returnNewDocument: true
			}).catch(console.error)
		console.log(found)
	})
	
  // close the connection
  client.close();

});


async function asyncForEach(array, callback) {
	
  for (let index = 0; index < array.length; index++) {
		
    await callback(array[index], index, array);
		
  }
	
}