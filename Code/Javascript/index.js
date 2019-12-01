  console.log("Hello World!")

function getCount() {
    var count = readTextFile("../Testlog.txt");
    
    document.getElementById("countTag").textContent = "count is: " + count;
    console.log(count);
    return 42;
}

function readTextFile(file)
{
    // Requiring fs module in which  
    // readFile function is defined. 
    const fs = require('fs') 
  
    fs.readFile(file, (err, data) => { 
        if (err) throw err; 
  
        console.log(data.toString()); 
    }) 
}