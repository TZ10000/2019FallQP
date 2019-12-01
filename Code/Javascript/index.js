  console.log("Hello World!")

function getCount() {
    var count = readTextFile("../Testlog.txt");
    
    document.getElementById("countTag").textContent = "count is: " + count;
    console.log(counts);
    return 42;
}

function readTextFile(file)
{
    console.log("called");
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                alert(allText);
                return allText;
            }
        }
    }
    rawFile.send(null);
}