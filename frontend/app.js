const app = {};

app.config = {
    apiBaseUrl: 'YOUR_API_BASE_URL',
};

app.log = function(message, level = 'log') {
    console[level](message);
};

app.uploadLogFile = function(file, callback, onProgress) {
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    formData.append('logFile', file);

    xhr.onreadystatechange = () => {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                const data = JSON.parse(xhr.responseText);
                app.log('File uploaded successfully: ' + xhr.responseText, 'info');
                if (callback) callback(null, data);
            } else {
                app.log('Failed to upload file.', 'error');
                if (callback) callback(new Error('Failed to upload.'));
            }
        }
    };

    xhr.upload.onprogress = function(event) {
        if (event.lengthComputable && onProgress) {
            const percentComplete = (event.loaded / event.total) * 100;
            onProgress(percentComplete);
            app.log(`Upload progress: ${Math.round(percentComplete)}%`, 'info');
        }
    };

    xhr.open('POST', `${app.config.apiBaseUrl}/upload`, true);
    xhr.send(formData);
};

app.getAnalysisReport = function(reportId, callback) {
    fetch(`${app.config.apiBaseUrl}/reports/${reportId}`)
        .then(response => response.json())
        .then(data => {
            app.log('Report data retrieved successfully', 'info');
            if (callback) callback(null, data);
        }).catch(err => {
            app.log('Error retrieving report data: ' + err, 'error');
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
    app.log('Results displayed successfully.', 'info');
};

app.updateProgress = function(percentage) {
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = `${percentage}%`;
    progressBar.textContent = `${Math.round(percentage)}%`;
    app.log(`Progress updated: ${Math.round(percentage)}%`, 'info');
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
                app.log('Error during file upload.', 'error');
            } else {
                alert('File uploaded successfully');
                app.log('Upload form submitted successfully.', 'info');
                const reportId = data.reportId;
                app.getAnalysisReport(reportId, function(error, reportData) {
                    if (error) {
                        console.error(error);
                        app.log('Error retrieving analysis report.', 'error');
                    } else {
                        app.displayResults(reportData);
                    }
                });
            }
        }, app.updateProgress);
    } else {
        alert('Please select a file to upload');
    }
});