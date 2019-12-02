  console.log("Hello World!")

function getCount() {
    

    const fs = require('fs');

    let rawdata = fs.readFileSync('data.json');
    let cnt = JSON.parse(rawdata);
    console.log(cnt);
    
    document.getElementById("countTag").textContent = "count is: " + cnt;
}

