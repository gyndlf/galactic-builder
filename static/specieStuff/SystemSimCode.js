var solar_system = new Array();
var astroid = new Array();
var star = new Array();
 /*Shows orbital lines when false*/
 var hideLines = true;
 /*How many times faster the simulation is*/
 var speedSim = 1;
 var time = 0;
function startGame() {
		myGameArea.start(); 
		/*Celestial Objects*/
		solar_system[0] = new Celestial_Ob_Fx(0, 800, 800, 100, 100, "#ffffcc");
		solar_system[1] = new Celestial_Ob(750, solar_system[0], 10, 10, 0.001, "yellow");
		solar_system[2] = new Celestial_Ob(500, solar_system[0], 20, 20, 0.004, "orange");
		solar_system[3] = new Celestial_Ob(300, solar_system[0], 5, 5, 0.008, "red");
		
}
var myGameArea = {
    canvas : document.getElementById("systemSim"),
    start : function() {
        this.canvas.width = 1600;
        this.canvas.height = 1600;
        this.context = this.canvas.getContext("2d");
        document.body.insertBefore(this.canvas, document.body.childNodes[0]);
        this.interval = setInterval(updateGameArea, 20);
        window.addEventListener('mousedown', function (e) {
            myGameArea.x = e.pageX;
            myGameArea.y = e.pageY;
        })
        window.addEventListener('mouseup', function (e) {
            myGameArea.x = false;
            myGameArea.y = false;
        })
        window.addEventListener('touchstart', function (e) {
            myGameArea.x = e.pageX;
            myGameArea.y = e.pageY;
        })
        window.addEventListener('touchend', function (e) {
            myGameArea.x = false;
            myGameArea.y = false;
        })
    }, 
    clear : function(){
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
}
function Celestial_Ob_Fx(distance, x, y, mass, size, colour){
	this.distance = distance;
	this.mass = mass;
	this.size = size;
	this.colour = colour;
	this.x = x;
	this.y = y;
	this.update = function(){
		ctx = myGameArea.context;
		ctx.fillStyle = this.colour;
		ctx.beginPath();
		ctx.arc(this.x, this.y, this.size, 0, 2*Math.PI);
		ctx.fill();
		ctx.closePath();
	}
}
function Astroid_Rg(distance, master, mass, width, colour){
	this.distance = distance;
	this.mass = mass;
	this.colour = colour;
	this.x = 0;
	this.y = 0;
	this.width = width;
	this.update = function(){
		ctx = myGameArea.context;
		ctx.fillStyle = this.colour;
		ctx.beginPath();
		ctx.arc(master.x, master.y, this.distance, 0, 2*Math.PI);
		ctx.fill();
		ctx.closePath();
		ctx.fillStyle = "white";
		ctx.beginPath();
		ctx.arc(master.x, master.y, this.distance - this.width, 0, 2*Math.PI);
		ctx.fill();
		ctx.closePath();
	}
}
function Celestial_Ob(distance, master, mass, size, speed, colour){
	this.distance = distance;
	this.master = master;
	this.mass = mass;
	this.size = size;
	this.speed = speed;
	this.colour = colour;
	this.x = 0;
	this.y = 0;
	this.curcuml = 2 * distance * Math.PI;
	this.rt = this.curcum1 / speed;
	this.rpt = (2 * Math.PI)/this.rt;
	this.rotations = 0;
	if(this.mass >= 1000){
	this.rotations = Math.PI;
	}
	this.update = function(){
		ctx = myGameArea.context;
		var distx;
		var disty;
		this.rotations += this.speed * speedSim;
		distx = Math.sin(this.rotations)*this.distance;
		disty = Math.cos(this.rotations)*this.distance;
		this.x = master.x + distx;
		this.y = master.y + disty;
		if(hideLines == false){
		ctx.beginPath();
		ctx.arc(master.x, master.y, this.distance, 0, 2*Math.PI);
		ctx.stroke();
		ctx.closePath();
		}
		ctx.fillStyle = this.colour;
		ctx.beginPath();
		ctx.arc(this.x, this.y, this.size, 0, 2*Math.PI);
		ctx.fill();
		ctx.closePath();
	}
}
function updateGameArea() {
    myGameArea.clear();
	time += 1*speedSim;
	for(i=0;i < astroid.length; i++){
		astroid[i].update();
	}
	for(i=0;i < solar_system.length; i++){
		solar_system[i].update();
	}
}