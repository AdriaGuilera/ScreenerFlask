document.addEventListener('DOMContentLoaded', function() {
    console.log(stockData);
    // Example of using the embedded data
    document.getElementById('Name').innerText = stockData.shortName;
    document.getElementById('summary').innerText = stockData.longBusinessSummary;
    document.getElementById('price').innerText = stockData.open;
    document.getElementById('change').innerText = (stockData.open/stockData.previousClose -1) * 100;

});