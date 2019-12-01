  console.log("Hello World!")

function getCount() {
    var my_js_data = JSON.parse('{"field1": "string value", "field2": 42}');

    var name = my_js_data["field1"];
    var count = my_js_data["field2"];
    
    document.getElementById("countTag").textContent = "count is: " + count;
    console.log(counts);
    return 42;
}