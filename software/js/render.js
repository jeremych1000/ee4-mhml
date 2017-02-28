/**
 * Created by Dominic Kwok on 2/25/2017.
 */
function test(width, height, data) {
    data = data.sort()
    var margin = {top: 20, right: 0, bottom: 20, left: 40}
    var heightScale  = d3.scaleLinear().domain([0, Math.max.apply(null, data)*1.1]).range([ height,0])
    var widthScale = d3.scaleLinear().domain([0 ,data.length+1]).range([0,width ])
    var xlist = d3.keys(data).map(
        function(d){return parseFloat(d)})
        xlist.push(xlist[xlist.length-1]+1)
    var xAxis = d3.axisBottom(widthScale).tickValues(xlist)
    var yAxis = d3.axisLeft(heightScale)
    var color = d3.scaleLinear().domain([Math.min.apply(null, data), Math.max.apply(null, data)]).range(["blue", "red"])
    var DrawingArea = d3.select("body").append("svg").attr("width", width).attr("height", height).append('g').attr("transform","translate("+margin["left"]+",0)")
    var bars = DrawingArea.selectAll("rect").data(data).enter()
        .append("rect")
        .attr("height", function (d) {
        return height-heightScale(d)
        })
        .attr("width", 50)
        .attr('x', function (d, i) {
        return widthScale(i+1)-25
        })
        .attr("fill", function (d) {
        return color(d)
        })
        .attr("y",function(d){
        return heightScale(d)-margin["bottom"]
        })
    var circle=DrawingArea.selectAll("circle").data(data).enter()
        .append("circle")
        .attr('cx',function(d,i){
            return widthScale(i+1)
        })
        .attr('cy',function(d){
            return heightScale(d)-margin["bottom"]
        })
        .attr('r',5)
        .attr('fill','black')


    DrawingArea.append("g").attr("transform","translate(0,"+(-margin["top"])+")").call(yAxis)
    DrawingArea.append("g").attr("transform","translate(0,"+(height-margin["bottom"])+")").call(xAxis)
}


function lineChartWthToolTip(){
    // Set the dimensions of the canvas / graph
    var margin = {top: 30, right: 20, bottom: 30, left: 50},
        width = 600 - margin.left - margin.right,
        height = 270 - margin.top - margin.bottom;

// Parse the date / time
    var parseDate = d3.timeParse("%d/%m/%y %H:%M:%S");
    var formatTime = d3.timeFormat("%H:%M:%S");

// Set the ranges
    var x = d3.scaleTime().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

// Define the axes
    var xAxis = d3.axisBottom(x).ticks(5);

    var yAxis = d3.axisLeft(y).ticks(5);

// Define the line
    var valueline = d3.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.close); })
        .curve(d3.curveStep)

// Define the div for the tooltip
    var div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

// Adds the svg canvas
    var svg = d3.select("body")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

// Get the data
    d3.csv("MSBand2_ALL_data_23_02_17.csv", function(error, data) {
        data.forEach(function(d) {
            d.date = parseDate(d["Time"]);
            d.close = +d["SkinT"];
        });

        // Scale the range of the data
        x.domain(d3.extent(data, function(d) { return d.date; }));
        y.domain([0, d3.max(data, function(d) { return d.close; })]);

        // Add the valueline path.
        svg.append("path")
            .attr("class", "line")
            .attr("d", valueline(data));

        svg.selectAll("rect")
            .data(data)
            .enter().append("rect")
            .attr("r", 2)
            .attr("fill","transparent")
            .attr("x", function(d) { return x(d.date); })
            .attr("y", function(d) { return y(d.close)-10; })
            .attr("width",1)
            .attr("height",20)
            .on("mouseover", function(d) {
                div.transition()
                    .duration(200)
                    .style("opacity", .9);
                div	.html("Time: "+formatTime(d.date) + "<br/>"  +"Temp:  "+ d.close)
                    .style("left", (d3.event.pageX) + "px")
                    .style("top", (d3.event.pageY - 28) + "px");
            })
            .on("mouseout", function(d) {
                div.transition()
                    .duration(500)
                    .style("opacity", 0);
            });


        // Add the X Axis
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        // Add the Y Axis
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis);

    });

}