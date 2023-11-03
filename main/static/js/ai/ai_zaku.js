document.getElementById('start-ai').addEventListener('click', function() {
console.log('hi');
    $.ajax({
        url: '/ai_start/',
        type: 'GET',
        success: function(response) {
            console.log('OK');
        }
    });
});