document.getElementById('ai-start').addEventListener('click', function() {
    $.ajax({
        url: 'ai_start/',
        type: 'GET',
        success: function(response) {
            console.log('OK');
        }
    });
});