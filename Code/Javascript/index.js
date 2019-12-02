  console.log("Hello World!")

function getCount() {
    fetch('../data.json')
        .then(result=>result.json())
        .then(console.log);

    // const fs = require('fs');

    // let rawdata = fs.readFileSync('count.json');
    // let cnt = JSON.parse(rawdata);
    // console.log(cnt);
    
    document.getElementById("countTag").textContent = "count is: " + cnt;
}

