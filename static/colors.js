window.onload = function(){
    var percentages = document.getElementsByClassName('change');
    for (var i = 0; i < percentages.length; i++) {
        var percentageValue = parseFloat(percentages[i].innerText.replace('%', ''));

        if (percentageValue < 0) {
            
            percentages[i].style.color = 'red';

        }
        if (percentageValue > 0) {
            percentages[i].style.color = 'green';
        }
    }
}