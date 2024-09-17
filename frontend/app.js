const app = {};

app.config = {
    apiBaseUrl: 'YOUR_API_BASE_URL',
};

app.uploadLogFile = function(file, callback) {
    const formData = new FormData();
    formData.append('logFile', file);

    fetch(`${app.config.apiBaseUrl}/upload`, {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (callback) callback(null, data);
    }).catch(err => {
        if (callback) callback(err);
    });
};

app.getAnalysisReport = function(reportId, callback) {
    fetch(`${app.config.apiBaseUrl}/reports/${reportId}`)
    .then(response => response.json())
    .then(data => {
        if (callback) callback(null, data);
    }).catch(err => {
        if (callback) callback(err);
    });
};

app.displayResults = function(data) {
    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.innerHTML = '';
    const dataString = JSON.stringify(data, null, 2);
    const pre = document.createElement('pre');
    pre.textContent = dataString;
    resultsContainer.appendChild(pre);
};

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const fileInput = document.getElementById('fileInput');
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        app.uploadLogFile(file, function(err, data) {
            if (err) {
                alert('Error uploading file');
                console.error(err);
            } else {
                alert('File uploaded successfully');
                const reportId = data.reportId;
                app.getAnalysisReport(reportId, function(error, reportData) {
                    if (error) {
                        console.error(error);
                    } else {
                        app.displayResults(reportData);
                    }
                });
            }
        });
    } else {
        alert('Please select a file to upload');
    }
});