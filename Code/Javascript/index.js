  console.log("Hello World!")

function getCount() {
    var counts = '{{=count}}';
    document.getElementById("countTag").textContent = "count is: 42";
    console.log(counts);
    return 42;
}