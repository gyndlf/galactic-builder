var myGamePiece;
var myShip = new Array(10);
var shipNumber = 3;
var enemyShip = new Array(10)
function startGame() {
	
	for (i = 0; i < shipNumber; i++){
		myShip[i] = new component(30, 30, "red", 40, 40 * i, 100, 50);
	}
	for (i = 0; i < shipNumber; i++){
		enemyShip[i] = new component(30, 30, "red", 200, 40 * i, 100, 50);
	}

	timer = new update();
    myGameArea.start(); 
}


var myGameArea = {
	
    canvas : document.createElement("canvas"),
    start : function() {
        this.canvas.width = 480;
        this.canvas.height = 270;
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
function update(){
	this.time = 0;
	this.update = function() {
		var timer = false;
		this.time += 1;
		if (this.time == 10){
			timer = true;
			this.time = 0;
		}else{
			timer = false;
		}
		return timer;
	}
}
function component(width, height, color, x, y, health, range) {
	this.futureX = x;
	this.futureY = y;
	this.health = health;
	this.range = range;
    this.width = width;
    this.height = height;
    this.speedX = 0;
    this.speedY = 0;
	this.color = color;
	this.futureY = 120;
	this.futureX = 10;
    this.x = x;
    this.y = y;  
	this.alive = true;	
	var number = 0;
	var number1 = 0;
		this.update = function() {
			if(this.health < 0){
				this.alive = false;
			}
			if(this.alive == true) {
			number += 1;
			number1 += 1;
			ctx = myGameArea.context;
			ctx.fillStyle = this.color;
			ctx.fillRect(this.x - this.width / 2, this.y - this.height / 2, this.width, this.height);
			ctx.beginPath();
			ctx.arc(this.x, this.y, this.range,0 , 2*Math.PI);
			ctx.stroke();
			ctx.font = "10px Arial";
			ctx.strokeText(this.health,this.x - 15, this.y);
			}
		}
		this.clicked = function() {
			var myleft = this.x - this.width / 2;
			var myright = this.x + (this.width) - this.width / 2;
			var mytop = this.y - this.height / 2;
			var mybottom = this.y + (this.height) - this.height / 2;
			var clicked = true;
			if ((mybottom < myGameArea.y) || (mytop > myGameArea.y) || (myright < myGameArea.x) || (myleft > myGameArea.x)) {
				clicked = false;
			}
			return clicked;
		}
		this.newPos = function() {
			if(this.alive == true) {
			this.x += this.speedX;
			this.y += this.speedY;  
			}
		}
		this.attack = function(enemy) {
			if(this.alive == true) {
			if (enemy.x > this.x - this.range && enemy.x < this.x + this.range && enemy.y > this.y - this.range && enemy.y < this.y + this.range ) {enemy.health -= 1;}
			}
		}
		this.move = function() {
			this.speedX = 0;
			this.speedY = 0;    
			if (this.x > this.futureX) {this.speedX = -1; }
			if (this.x < this.futureX) {this.speedX = 1; }
			if (this.y > this.futureY) {this.speedY = -1; }
			if (this.y < this.futureY) {this.speedY = 1; } 
		}
		this.setfuture = function(other) {
			if (this.clicked() && this.color == "red" && number1 > 10) {
				this.color = "blue";
				number = 0;
			} else if (this.color == "blue" && this.clicked() && number > 10){
			this.color = "red";
			number1 = 0;
			}
			else if (this.color == "blue"){
				this.futureX = other.x;
				this.futureY = other.y;
				if (this.futureX > myGameArea.canvas.width){
				this.futureX = myGameArea.canvas.width - 10;
				}else if (this.futureX < 0){
				this.futureX = 10;
				}else if (this.futureY > myGameArea.canvas.height){
				this.futureY = myGameArea.canvas.height - 10;
				}else if (this.futureY < 0){
				this.futureX = 10;
				}
			} else {}
		}
	
}
function updateGameArea() {
    myGameArea.clear();
	
    if (myGameArea.x && myGameArea.y) {
		for (i = 0; i < shipNumber; i++){
		myShip[i].setfuture(myGameArea);
		}
    }
	for (i = 0; i < shipNumber; i++){
		myShip[i].move();
		}
	if (timer.update()){
	for (i = 0; i < shipNumber; i++){
	for (y = 0; y < shipNumber; y++){
					enemyShip[y].attack(myShip[i]);
		}
		}
		for (i = 0; i < shipNumber; i++){
		for (y = 0; y < shipNumber; y++){
		myShip[i].attack(enemyShip[y]);
		}
		myShip[i].newPos();
		}
	}
	for (i = 0; i < shipNumber; i++){
		myShip[i].update();
		}
		for (i = 0; i < shipNumber; i++){
		enemyShip[i].update();
		}
}