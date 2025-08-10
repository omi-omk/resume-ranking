// Global state
let currentPage = 'dashboard';
let currentJob = '';

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupNavigation();
    loadDashboard();
}

function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.getAttribute('data-page');
            navigateTo(page);
        });
    });
}

function navigateTo(page) {
    // Update active nav
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`[data-page="${page}"]`).classList.add('active');
    
    currentPage = page;
    
    // Load page content
    switch(page) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'candidates':
            loadCandidates();
            break;
        case 'jobs':
            loadJobs();
            break;
        case 'matching':
            loadMatching();
            break;
    }
}

// Dashboard
function loadDashboard() {
    const content = document.getElementById('main-content');
    content.innerHTML = `
        <div class="card">
            <h2>Dashboard</h2>
            <p>Welcome to the Resume Ranking System</p>
            <div class="d-flex gap-2 mt-2">
                <div class="card" style="flex: 1;">
                    <h3 id="total-candidates">-</h3>
                    <p>Total Candidates</p>
                </div>
                <div class="card" style="flex: 1;">
                    <h3 id="total-jobs">-</h3>
                    <p>Total Jobs</p>
                </div>
                <div class="card" style="flex: 1;">
                    <h3 id="total-matches">-</h3>
                    <p>Total Matches</p>
                </div>
            </div>
        </div>
    `;
    
    loadDashboardStats();
}

async function loadDashboardStats() {
    try {
        const [candidates, jobs] = await Promise.all([
            fetch('/api/candidates/').then(r => r.json()),
            fetch('/api/jobs/').then(r => r.json())
        ]);
        
        document.getElementById('total-candidates').textContent = candidates.total_file || 0;
        document.getElementById('total-jobs').textContent = jobs.total_job || 0;
        document.getElementById('total-matches').textContent = '-'; // TODO: Add matching count
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
    }
}

// Candidates
function loadCandidates() {
    const content = document.getElementById('main-content');
    content.innerHTML = `
        <div class="card">
            <div class="d-flex justify-between align-center mb-2">
                <h2>Candidates</h2>
                <button class="btn btn-primary" onclick="showUploadModal()">
                    Upload CVs
                </button>
            </div>
            <div id="candidates-table">
                <div class="loading">
                    <div class="spinner"></div>
                </div>
            </div>
        </div>
    `;
    
    loadCandidatesTable();
}

async function loadCandidatesTable() {
    try {
        const response = await fetch('/api/candidates/');
        const data = await response.json();
        
        const tableHtml = `
            <table class="table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>CV File</th>
                        <th>Upload Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.results.map(candidate => `
                        <tr>
                            <td>${candidate.candidate_name || 'Unknown'}</td>
                            <td>${candidate.email || '-'}</td>
                            <td>${candidate.cv_name || '-'}</td>
                            <td>${new Date(candidate.created_at).toLocaleDateString()}</td>
                            <td>
                                <button class="btn btn-sm btn-secondary" onclick="viewCandidate('${candidate._id}')">
                                    View
                                </button>
                                <button class="btn btn-sm btn-danger" onclick="deleteCandidate('${candidate._id}')">
                                    Delete
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
        document.getElementById('candidates-table').innerHTML = tableHtml;
    } catch (error) {
        console.error('Error loading candidates:', error);
        document.getElementById('candidates-table').innerHTML = '<p>Error loading candidates</p>';
    }
}

function showUploadModal() {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>Upload CV Files</h3>
                <button class="btn btn-sm" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body">
                <div class="upload-area" id="upload-area">
                    <div class="upload-icon">📄</div>
                    <p>Drag & drop CV files here or click to browse</p>
                    <p class="text-sm">Supports PDF and DOCX files</p>
                    <input type="file" id="file-input" multiple accept=".pdf,.docx" style="display: none;">
                </div>
                <div id="upload-progress" style="display: none;">
                    <div class="loading">
                        <div class="spinner"></div>
                        <span>Uploading and analyzing files...</span>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    setupFileUpload();
}

function setupFileUpload() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });
    
    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });
}

async function handleFiles(files) {
    const formData = new FormData();
    for (let file of files) {
        formData.append('files', file);
    }
    
    document.getElementById('upload-progress').style.display = 'block';
    document.getElementById('upload-area').style.display = 'none';
    
    try {
        const response = await fetch('/api/candidates/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        closeModal();
        loadCandidatesTable();
        
        // Show results
        alert(`Upload completed!\nProcessed: ${result.results.filter(r => r.status === 'success').length}\nSkipped: ${result.results.filter(r => r.status === 'skipped').length}\nErrors: ${result.results.filter(r => r.status === 'error').length}`);
        
    } catch (error) {
        console.error('Error uploading files:', error);
        alert('Error uploading files');
        closeModal();
    }
}

// Jobs
function loadJobs() {
    const content = document.getElementById('main-content');
    content.innerHTML = `
        <div class="card">
            <div class="d-flex justify-between align-center mb-2">
                <h2>Jobs</h2>
                <button class="btn btn-primary" onclick="showCreateJobModal()">
                    Create Job
                </button>
            </div>
            <div id="jobs-table">
                <div class="loading">
                    <div class="spinner"></div>
                </div>
            </div>
        </div>
    `;
    
    loadJobsTable();
}

async function loadJobsTable() {
    try {
        const response = await fetch('/api/jobs/');
        const data = await response.json();
        
        const tableHtml = `
            <table class="table">
                <thead>
                    <tr>
                        <th>Job Title</th>
                        <th>Created Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.results.map(job => `
                        <tr>
                            <td>${job.job_name}</td>
                            <td>${new Date(job.created_at).toLocaleDateString()}</td>
                            <td>
                                <button class="btn btn-sm btn-secondary" onclick="viewJob('${job._id}')">
                                    View
                                </button>
                                <button class="btn btn-sm btn-danger" onclick="deleteJob('${job._id}')">
                                    Delete
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
        document.getElementById('jobs-table').innerHTML = tableHtml;
    } catch (error) {
        console.error('Error loading jobs:', error);
        document.getElementById('jobs-table').innerHTML = '<p>Error loading jobs</p>';
    }
}

function showCreateJobModal() {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3>Create New Job</h3>
                <button class="btn btn-sm" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body">
                <form id="job-form">
                    <div class="form-group">
                        <label>Job Title</label>
                        <input type="text" class="form-control" name="job_name" required>
                    </div>
                    <div class="form-group">
                        <label>Job Description</label>
                        <textarea class="form-control" name="job_description" rows="8" required></textarea>
                    </div>
                    <div class="d-flex gap-2">
                        <button type="submit" class="btn btn-primary">Create Job</button>
                        <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    document.getElementById('job-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const jobData = {
            job_name: formData.get('job_name'),
            job_description: formData.get('job_description')
        };
        
        try {
            const response = await fetch('/api/jobs/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(jobData)
            });
            
            if (response.ok) {
                closeModal();
                loadJobsTable();
                alert('Job created successfully!');
            } else {
                alert('Error creating job');
            }
        } catch (error) {
            console.error('Error creating job:', error);
            alert('Error creating job');
        }
    });
}

// Matching
function loadMatching() {
    const content = document.getElementById('main-content');
    content.innerHTML = `
        <div class="card">
            <h2>Matching</h2>
            <div class="d-flex gap-2 align-center mb-2">
                <select id="job-selector" class="form-control" style="max-width: 300px;">
                    <option value="">Select a job...</option>
                </select>
                <button class="btn btn-primary" onclick="processMatching()">
                    Start Matching
                </button>
            </div>
            <div id="matching-results">
                <p>Select a job to view matching results</p>
            </div>
        </div>
    `;
    
    loadJobSelector();
}

async function loadJobSelector() {
    try {
        const response = await fetch('/api/jobs/all');
        const jobs = await response.json();
        
        const selector = document.getElementById('job-selector');
        selector.innerHTML = '<option value="">Select a job...</option>' +
            jobs.map(job => `<option value="${job.job_name}">${job.job_name}</option>`).join('');
        
        selector.addEventListener('change', (e) => {
            if (e.target.value) {
                loadMatchingResults(e.target.value);
            }
        });
    } catch (error) {
        console.error('Error loading jobs:', error);
    }
}

async function processMatching() {
    const jobName = document.getElementById('job-selector').value;
    if (!jobName) {
        alert('Please select a job first');
        return;
    }
    
    try {
        const response = await fetch('/api/matching/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ job_name: jobName })
        });
        
        const result = await response.json();
        alert(`Matching completed!\nProcessed: ${result.processed}\nSkipped: ${result.skipped}`);
        
        loadMatchingResults(jobName);
    } catch (error) {
        console.error('Error processing matching:', error);
        alert('Error processing matching');
    }
}

async function loadMatchingResults(jobName) {
    document.getElementById('matching-results').innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
        </div>
    `;
    
    try {
        const response = await fetch(`/api/matching/results?job_name=${encodeURIComponent(jobName)}`);
        const data = await response.json();
        
        const tableHtml = `
            <table class="table">
                <thead>
                    <tr>
                        <th>Candidate</th>
                        <th>Email</th>
                        <th>Score</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.results.map(result => `
                        <tr>
                            <td>${result.candidate_name}</td>
                            <td>${result.candidate_email}</td>
                            <td>
                                <span class="badge ${getScoreBadgeClass(result.score)}">
                                    ${result.score.toFixed(1)}%
                                </span>
                            </td>
                            <td>
                                <span class="badge ${result.matching_status ? 'badge-success' : 'badge-warning'}">
                                    ${result.matching_status ? 'Matched' : 'Pending'}
                                </span>
                            </td>
                            <td>
                                <button class="btn btn-sm btn-secondary" onclick="viewMatchingDetail('${result.id}', '${jobName}')">
                                    View Details
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
        document.getElementById('matching-results').innerHTML = tableHtml;
    } catch (error) {
        console.error('Error loading matching results:', error);
        document.getElementById('matching-results').innerHTML = '<p>Error loading matching results</p>';
    }
}

function getScoreBadgeClass(score) {
    if (score >= 80) return 'badge-success';
    if (score >= 60) return 'badge-info';
    if (score >= 40) return 'badge-warning';
    return 'badge-danger';
}

// Utility functions
function closeModal() {
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.remove();
    }
}

async function deleteCandidate(id) {
    if (confirm('Are you sure you want to delete this candidate?')) {
        try {
            const response = await fetch(`/api/candidates/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                loadCandidatesTable();
                alert('Candidate deleted successfully');
            } else {
                alert('Error deleting candidate');
            }
        } catch (error) {
            console.error('Error deleting candidate:', error);
            alert('Error deleting candidate');
        }
    }
}

async function deleteJob(id) {
    if (confirm('Are you sure you want to delete this job?')) {
        try {
            const response = await fetch(`/api/jobs/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                loadJobsTable();
                alert('Job deleted successfully');
            } else {
                alert('Error deleting job');
            }
        } catch (error) {
            console.error('Error deleting job:', error);
            alert('Error deleting job');
        }
    }
}

// Modal styles
const modalStyles = `
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    border-radius: 8px;
    max-width: 600px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
}

.modal-header {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #e5e7eb;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-body {
    padding: 1.5rem;
}
`;

// Add modal styles to head
const styleSheet = document.createElement('style');
styleSheet.textContent = modalStyles;
document.head.appendChild(styleSheet);