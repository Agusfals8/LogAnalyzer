const app = {};

app.config = {
    apiBaseUrl: 'YOUR_API_BASE_URL',
};

app.uploadLogFile = function(file, callback, onProgress) {
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    formData.append('logFile', file);

    xhr.onreadystatechange = () => {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                const data = JSON.parse(xhr.responseText);
                if (callback) callback(null, data);
            } else {
                if (callback) callback(new Error('Failed to upload.'));
            }
        }
    };

    // Monitor upload progress
    xhr.upload.onprogress = function(event) {
        if (event.lengthComputable && onProgress) {
            const percentComplete = (event.loaded / event.total) * 100;
            onProgress(percentComplete);
        }
    };

    xhr.open('POST', `${app.config.apiBaseUrl}/upload`, true);
    xhr.send(formData);
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

// Function to update UI with upload progress
app.updateProgress = function(percentage) {
    // Assuming you have a progress element in your HTML with id 'progressBar'
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = `${percentage}%`;
    progressBar.textContent = `${Math.round(percentage)}%`;
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
        }, app.updateProgress);
    } else {
        alert('Please select a file to upload');
    }
});