window.onload = function() {
    var rsiElements = document.getElementsByClassName('rsi');

    for (var i = 0; i < rsiElements.length; i++) {
        var rsiValue = parseFloat(rsiElements[i].innerText);

        if (rsiValue < 50 && rsiValue >= 0) {
            // Adjust the calculation of the red component
            // If RSI is 30, red will be 0 (black)
            // If RSI is 0, red will be 255 (red)
            let red = Math.floor(((rsiValue - 20) / 30)*100)/2 + 50;
            rsiElements[i].style.backgroundColor = 'hsl(0, ' + red + '% ,' + red + '% )';
            //console.log('hsl(0, ' + red + '% ,' + red + '% )');

        }
        else if(rsiValue > 50 && rsiValue <= 100) {
            // Adjust the calculation of the green component
            // If RSI is 30, green will be 255 (green)
            // If RSI is 100, green will be 0 (black)
            let green = (50 - Math.floor(((rsiValue - 50) / 30)*100)/2) + 50;
            rsiElements[i].style.backgroundColor = 'hsl(120, ' + green + '% ,' + green + '% )';

        }
        else if (rsiValue < 0){
            rsiElements[i].style.backgroundColor = "yellow";
        }
    }

    var monthElements = document.getElementsByClassName('month');
    var weekElements = document.getElementsByClassName('week');
    var tickerElements = document.getElementsByClassName('stock');
    var weekmax = NaN;
    var weekmin = NaN;
    var monthmax = NaN;
    var monthmin = NaN;
    var weekmaxvalue = -120;
    var monthmaxvalue = -120;
    var weekminvalue = 2500;
    var monthminvalue = 2500;


    for (var i = 0; i < weekElements.length; i++) {
        var weekValue = parseFloat(weekElements[i].innerText.replace('%', ''));
        var monthValue = parseFloat(monthElements[i].innerText.replace('%', ''));

        if (weekValue < 0) {
            let red = (50-Math.floor(Math.min((-1*weekValue/7.0),1)*100.0)/2.0) + 50;
            //console.log(red);
            
            weekElements[i].style.backgroundColor = 'hsl(0, ' + red + '% ,' + Math.min(red,96) + '% )';
            
            console.log(weekminvalue);
            if(weekValue < weekminvalue){
                weekmin = i;
                weekminvalue = weekValue;
                console.log("IN");
            }
            
        }
        console.log(weekmaxvalue);
        if (weekValue > 0) {
            let green = (50-Math.floor(Math.min((weekValue/7.0),1)*100)/2) + 50;
            //console.log(green);
            
            if(weekValue > weekmaxvalue){
                weekmax = i;
                weekmaxvalue = weekValue;
            }

            
            weekElements[i].style.backgroundColor = 'hsl(120, ' + green + '% ,' + Math.min(green,96) + '% )';
        }


        if (monthValue < 0) {
            let red = (50-Math.floor(Math.min(((-1*monthValue) / 10.0),1)*100.0)/2.0) + 50;
            //console.log(red);
            
            monthElements[i].style.backgroundColor = 'hsl(0, ' + red + '% ,' + Math.min(red,96) + '% )';
            
            if(monthValue < monthminvalue){
                monthmin = i;
                monthminvalue = monthValue;
            }
        }
        if (monthValue > 0) {
            let green = (50-Math.floor(Math.min((monthValue/10.0),1)*100)/2) + 50;
            //console.log(green);
            
            monthElements[i].style.backgroundColor = 'hsl(120, ' + green + '% ,' + Math.min(green,96) + '% )';

            if(monthValue > monthmaxvalue){
                monthmax = i;
                monthmaxvalue = monthValue;
            }
        }

    }
    console.log(weekmax,weekmin,monthmax,monthmin);
    if(!isNaN(weekmax)){
        let maxv = document.getElementById('Wweekv');
        let max = document.getElementById('Wweek');
        maxv.innerText = weekmaxvalue + '%';
        max.innerText = tickerElements[weekmax].innerText;
    }
    if(!isNaN(weekmin)){
        let minv = document.getElementById('Lweekv');
        minv.innerText = weekminvalue + '%';
        let min = document.getElementById('Lweek');
        min.innerText = tickerElements[weekmin].innerText;

    }
    if(!isNaN(monthmax)){
        let maxv = document.getElementById('Wmonthv');
        maxv.innerText = monthmaxvalue + '%';
        let max = document.getElementById('Wmonth');
        max.innerText = tickerElements[monthmax].innerText;
        
    }
    if(!isNaN(monthmin)){
        let minv = document.getElementById('Lmonthv');
        minv.innerText = monthminvalue + '%';
        let min = document.getElementById('Lmonth');
        min.innerText = tickerElements[monthmin].innerText;
    }



};