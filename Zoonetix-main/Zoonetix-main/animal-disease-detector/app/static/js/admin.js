// Store all users for search functionality
let allUsers = [];

// Load users on page load
document.addEventListener('DOMContentLoaded', () => {
    loadUsers();
});

// Load all users
async function loadUsers() {
    try {
        const response = await fetch('/api/admin/users', {
            method: 'GET',
            credentials: 'include'
        });

        if (response.status === 401) {
            // Unauthorized, redirect to admin login
            window.location.href = '/admin';
            return;
        }

        if (!response.ok) {
            throw new Error('Failed to load users');
        }

        allUsers = await response.json();
        displayUsers(allUsers);
        updateStats();
    } catch (error) {
        console.error('Error loading users:', error);
        document.getElementById('usersTableBody').innerHTML = `
            <tr class="empty-table">
                <td colspan="5">Error loading users. Please try again.</td>
            </tr>
        `;
    }
}

// Display users in table
function displayUsers(users) {
    const tableBody = document.getElementById('usersTableBody');
    
    if (users.length === 0) {
        tableBody.innerHTML = `
            <tr class="empty-table">
                <td colspan="5">No users found</td>
            </tr>
        `;
        return;
    }

    tableBody.innerHTML = users.map(user => `
        <tr>
            <td>
                ${user.username}
                ${user.is_admin ? '<span class="admin-badge-inline">ADMIN</span>' : ''}
            </td>
            <td class="user-email">${user.email}</td>
            <td class="user-date">${formatDate(user.created_at)}</td>
            <td>${user.predictions_count}</td>
            <td>
                <div class="action-buttons">
                    <button class="btn-view" onclick="viewUserDetails(${user.id})">View</button>
                    ${!user.is_admin ? `<button class="btn-delete" onclick="deleteUser(${user.id}, '${user.username}')">Delete</button>` : '<span style="color: #666; font-size: 12px;">-</span>'}
                </div>
            </td>
        </tr>
    `).join('');
}

// Filter users based on search
function filterUsers() {
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    
    const filteredUsers = allUsers.filter(user => 
        user.username.toLowerCase().includes(searchInput) ||
        user.email.toLowerCase().includes(searchInput)
    );
    
    displayUsers(filteredUsers);
}

// View user details
async function viewUserDetails(userId) {
    try {
        const response = await fetch(`/api/admin/users/${userId}`, {
            method: 'GET',
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error('Failed to load user details');
        }

        const user = await response.json();
        displayUserDetails(user);
        document.getElementById('userModal').classList.add('active');
    } catch (error) {
        console.error('Error loading user details:', error);
        alert('Error loading user details');
    }
}

// Display user details in modal
function displayUserDetails(user) {
    const detailsDiv = document.getElementById('userDetailsContent');
    
    const detailsHTML = `
        <div class="user-detail-item">
            <span class="user-detail-label">User ID:</span>
            <span class="user-detail-value">#${user.id}</span>
        </div>
        <div class="user-detail-item">
            <span class="user-detail-label">Username:</span>
            <span class="user-detail-value">${user.username}</span>
        </div>
        <div class="user-detail-item">
            <span class="user-detail-label">Email:</span>
            <span class="user-detail-value">${user.email}</span>
        </div>
        <div class="user-detail-item">
            <span class="user-detail-label">Joined:</span>
            <span class="user-detail-value">${formatDate(user.created_at)}</span>
        </div>
        <div class="user-detail-item">
            <span class="user-detail-label">Role:</span>
            <span class="user-detail-value">${user.is_admin ? 'Admin' : 'User'}</span>
        </div>
        <div class="user-detail-item">
            <span class="user-detail-label">Total Predictions:</span>
            <span class="user-detail-value">${user.predictions_count}</span>
        </div>
        
        ${user.predictions_count > 0 ? `
            <div class="predictions-list">
                <h3 style="color: #00d4ff; margin-top: 20px; margin-bottom: 15px;">
                    Recent Predictions
                </h3>
                ${user.predictions.slice(0, 10).map(pred => `
                    <div class="prediction-item">
                        <div class="prediction-disease">🔬 ${pred.disease}</div>
                        <div class="prediction-confidence">
                            Confidence: ${(pred.confidence * 100).toFixed(2)}%
                        </div>
                        <div class="prediction-confidence">
                            📸 ${pred.image_name || 'Unknown'}
                        </div>
                        <div class="prediction-confidence">
                            📅 ${formatDate(pred.created_at)}
                        </div>
                    </div>
                `).join('')}
            </div>
        ` : `
            <div class="no-predictions">
                No predictions yet
            </div>
        `}
        
        ${!user.is_admin ? `
            <button class="btn-delete" onclick="deleteUserFromModal(${user.id}, '${user.username}')" 
                    style="width: 100%; margin-top: 20px; padding: 10px;">
                Delete User Account
            </button>
        ` : ''}
    `;
    
    detailsDiv.innerHTML = detailsHTML;
}

// Close user details modal
function closeUserModal() {
    document.getElementById('userModal').classList.remove('active');
}

// Delete user
async function deleteUser(userId, username) {
    if (!confirm(`Are you sure you want to delete user "${username}" and all their predictions?`)) {
        return;
    }

    try {
        const response = await fetch(`/api/admin/users/${userId}`, {
            method: 'DELETE',
            credentials: 'include'
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to delete user');
        }

        alert('User deleted successfully');
        loadUsers();
    } catch (error) {
        console.error('Error deleting user:', error);
        alert(`Error: ${error.message}`);
    }
}

// Delete user from modal
function deleteUserFromModal(userId, username) {
    closeUserModal();
    deleteUser(userId, username);
}

// Update statistics
function updateStats() {
    const totalUsers = allUsers.length;
    const totalPredictions = allUsers.reduce((sum, user) => sum + user.predictions_count, 0);

    document.getElementById('totalUsers').textContent = totalUsers;
    document.getElementById('totalPredictions').textContent = totalPredictions;
}

// Format date
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Admin logout
async function adminLogout() {
    try {
        await fetch('/api/admin/logout', {
            method: 'POST',
            credentials: 'include'
        });
        
        document.cookie = 'admin_token=; path=/; max-age=0';
        window.location.href = '/admin';
    } catch (error) {
        console.error('Error logging out:', error);
    }
}

// Close modal when clicking outside
document.getElementById('userModal')?.addEventListener('click', (e) => {
    if (e.target.id === 'userModal') {
        closeUserModal();
    }
});
