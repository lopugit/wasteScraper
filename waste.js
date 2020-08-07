// With help from https://www.scrapehero.com/how-to-build-a-web-scraper-using-puppeteer-and-node-js/
const puppeteer = require('puppeteer');

let pageUrl = 'https://www.recycling.vic.gov.au/can-i-recycle-this';
(async () => {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });
    await page.goto(pageUrl);

    // get page details
    let itemData = await page.evaluate(() => {
        let items = [];
        // get the page elements
        let itemElem = document.querySelectorAll('div.tile');
        console.log(itemElem);
        // get the page data
        itemElem.forEach((item) => {
            let itemJson = {};
            try {
                let tile = item.querySelector('a.tile__link').querySelector('div.tile__content').querySelector('div.tile__heading');
                itemJson.name = tile.querySelector('span.tile__title').innerText;
                //itemJson.alias = tile.querySelector('span.tile__subtitle').innerText;
                
            }
            catch (exception){

            }
            items.push(itemJson);
        });
        return items;
    });

    console.dir(itemData);
})();