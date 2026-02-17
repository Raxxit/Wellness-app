<template>
  <div class="manage-resources">
    <div class="header">
      <h1>Manage Resources</h1>
      <div class="header-actions">
        <router-link to="/AdminResource" class="btn btn-primary">
          + Add New Resource
        </router-link>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading">
      Loading resources...
    </div>

    <!-- Error Message -->
    <div v-if="error" class="error">
      {{ error }}
    </div>

    <!-- Resources Table -->
    <div v-if="!loading && !error" class="table-container">
      <!-- Filter by type -->
      <div class="filter-bar">
        <select v-model="typeFilter" class="filter-select">
          <option value="">All Types</option>
          <option value="video">Video</option>
          <option value="article">Article</option>
          <option value="podcast">Podcast</option>
          <option value="app">App</option>
          <option value="website">Website</option>
          <option value="game">Game</option>
        </select>
      </div>

      <table class="resources-table">
        <thead>
          <tr>
            <th>Type</th>
            <th>Title</th>
            <th>URL</th>
            <th>Verified</th>
            <th>Created</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="resource in filteredResources" :key="resource.resource_id">
            <td>
              <span class="type-badge" :class="resource.type">
                {{ resource.type }}
              </span>
            </td>
            <td>{{ resource.title }}</td>
            <td>
              <a :href="resource.url" target="_blank" class="url-link">
                {{ truncateUrl(resource.url) }}
              </a>
            </td>
            <td>
              <span class="verified-badge" :class="{ verified: resource.is_verified }">
                {{ resource.is_verified ? '✓' : '✗' }}
              </span>
            </td>
            <td>{{ formatDate(resource.created_at) }}</td>
            <td class="actions">
              <button @click="editResource(resource)" class="btn-edit">
                Edit
              </button>
              <button @click="confirmDelete(resource)" class="btn-delete">
                Delete
              </button>
            </td>
          </tr>
          <tr v-if="filteredResources.length === 0">
            <td colspan="7" class="no-data">No resources found</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <h2>Edit Resource</h2>
        <form @submit.prevent="updateResource">
          <div class="form-group">
            <label>Title:</label>
            <input type="text" v-model="editForm.title" required>
          </div>
          
          <div class="form-group">
            <label>URL:</label>
            <input type="url" v-model="editForm.url" required>
          </div>
          
          <div class="form-group">
            <label>Type:</label>
            <select v-model="editForm.type" required>
              <option value="video">Video</option>
              <option value="article">Article</option>
              <option value="podcast">Podcast</option>
              <option value="app">App</option>
              <option value="website">Website</option>
              <option value="game">Game</option>
            </select>
          </div>
          
          <div class="form-group checkbox">
            <label>
              <input type="checkbox" v-model="editForm.is_verified">
              Verified
            </label>
          </div>
          
          <div class="modal-actions">
            <button type="submit" class="btn-save" :disabled="saving">
              {{ saving ? 'Saving...' : 'Save Changes' }}
            </button>
            <button type="button" class="btn-cancel" @click="closeModal">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal">
      <div class="modal-content small">
        <h3>Delete Resource</h3>
        <p>Are you sure you want to delete "{{ deleteItem?.title }}"?</p>
        <div class="modal-actions">
          <button @click="deleteResource" class="btn-delete" :disabled="deleting">
            {{ deleting ? 'Deleting...' : 'Yes, Delete' }}
          </button>
          <button @click="closeDeleteModal" class="btn-cancel">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ManageResources',
  data() {
    return {
      loading: true,
      saving: false,
      deleting: false,
      error: '',
      resources: [],
      typeFilter: '',
      showEditModal: false,
      showDeleteModal: false,
      editForm: {
        resource_id: null,
        title: '',
        url: '',
        type: '',
        is_verified: false
      },
      deleteItem: null
    }
  },
  computed: {
    filteredResources() {
      if (!this.typeFilter) return this.resources
      return this.resources.filter(r => r.type === this.typeFilter)
    }
  },
  mounted() {
    this.fetchResources()
  },
  methods: {
    async fetchResources() {
      this.loading = true
      try {
        const response = await fetch('http://127.0.0.1:5000/api/admin/resources')
        const data = await response.json()
        this.resources = data
      } catch (error) {
        this.error = 'Failed to load resources'
        console.error(error)
      } finally {
        this.loading = false
      }
    },

    editResource(resource) {
      this.editForm = {
        resource_id: resource.resource_id,
        title: resource.title,
        url: resource.url,
        type: resource.type,
        is_verified: resource.is_verified == 1
      }
      this.showEditModal = true
    },

    async updateResource() {
  this.saving = true
  try {
    const url = `http://127.0.0.1:5000/api/admin/resources/${this.editForm.resource_id}`
    const payload = {
      title: this.editForm.title,
      url: this.editForm.url,
      type: this.editForm.type,
      is_verified: this.editForm.is_verified ? 1 : 0
    }
    
    console.log('Updating resource at:', url)
    console.log('With payload:', payload)
    
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    console.log('Response status:', response.status)
    
    const data = await response.json()
    console.log('Response data:', data)

    if (response.ok) {
      await this.fetchResources()
      this.closeModal()
      alert('Resource updated successfully!')
    } else {
      alert('Failed to update resource: ' + (data.message || 'Unknown error'))
    }
  } catch (error) {
    console.error('Full error:', error)
    alert('Error updating resource: ' + error.message)
  } finally {
    this.saving = false
  }
},

    confirmDelete(resource) {
      this.deleteItem = resource
      this.showDeleteModal = true
    },

    async deleteResource() {
  this.deleting = true
  try {
    const url = `http://127.0.0.1:5000/api/admin/resources/${this.deleteItem.resource_id}`
    console.log('Deleting resource at:', url)
    console.log('Resource to delete:', this.deleteItem)
    
    const response = await fetch(url, {
      method: 'DELETE'
    })

    console.log('Response status:', response.status)
    
    // Try to get response text first
    const text = await response.text()
    console.log('Response text:', text)
    
    // Try to parse as JSON if possible
    let data
    try {
      data = JSON.parse(text)
      console.log('Response data:', data)
    } catch (e) {
      console.log('Response is not JSON:', text)
    }

    if (response.ok) {
      await this.fetchResources()
      this.closeDeleteModal()
      alert('Resource deleted successfully!')
    } else {
      alert('Failed to delete resource. Status: ' + response.status)
    }
  } catch (error) {
    console.error('Delete error:', error)
    alert('Error deleting resource: ' + error.message)
  } finally {
    this.deleting = false
  }
},

    closeModal() {
      this.showEditModal = false
      this.editForm = {
        resource_id: null,
        title: '',
        url: '',
        type: '',
        is_verified: false
      }
    },

    closeDeleteModal() {
      this.showDeleteModal = false
      this.deleteItem = null
    },

    truncateUrl(url) {
      if (url.length > 30) {
        return url.substring(0, 30) + '...'
      }
      return url
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.manage-resources {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  color: #1e293b;
  margin: 0;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  text-decoration: none;
  font-size: 14px;
}

.btn-primary {
  background: #6366f1;
  color: white;
}

.btn-primary:hover {
  background: #4f46e5;
}

.filter-bar {
  margin-bottom: 20px;
}

.filter-select {
  padding: 8px 12px;
  border: 2px solid #e2e8f0;
  border-radius: 6px;
  width: 200px;
}

.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow-x: auto;
}

.resources-table {
  width: 100%;
  border-collapse: collapse;
}

.resources-table th {
  background: #f8fafc;
  padding: 15px;
  text-align: left;
  font-weight: 600;
  color: #475569;
  border-bottom: 2px solid #e2e8f0;
}

.resources-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #e2e8f0;
}

.type-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  text-transform: capitalize;
}

.type-badge.video { background: #e0e7ff; color: #3730a3; }
.type-badge.article { background: #fef3c7; color: #92400e; }
.type-badge.podcast { background: #fae8ff; color: #86198f; }
.type-badge.app { background: #dcfce7; color: #166534; }
.type-badge.website { background: #cffafe; color: #155e75; }
.type-badge.game { background: #ffe4e6; color: #991b1b; }

.url-link {
  color: #6366f1;
  text-decoration: none;
}

.url-link:hover {
  text-decoration: underline;
}

.verified-badge {
  display: inline-block;
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  border-radius: 50%;
  background: #f1f5f9;
}

.verified-badge.verified {
  background: #dcfce7;
  color: #166534;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-edit, .btn-delete {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.btn-edit {
  background: #e0e7ff;
  color: #3730a3;
}

.btn-edit:hover {
  background: #c7d2fe;
}

.btn-delete {
  background: #fee2e2;
  color: #991b1b;
}

.btn-delete:hover {
  background: #fecaca;
}

.no-data {
  text-align: center;
  color: #94a3b8;
  padding: 40px;
}

.loading, .error {
  text-align: center;
  padding: 40px;
  color: #64748b;
}

.error {
  color: #ef4444;
}

/* Modal Styles */
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
  padding: 30px;
  border-radius: 12px;
  width: 500px;
  max-width: 90%;
}

.modal-content.small {
  width: 400px;
}

.modal-content h2, .modal-content h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #1e293b;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #475569;
  font-weight: 500;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 2px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
}

.form-group.checkbox label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.form-group.checkbox input {
  width: auto;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

.btn-save, .btn-cancel {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.btn-save {
  background: #6366f1;
  color: white;
}

.btn-save:hover:not(:disabled) {
  background: #4f46e5;
}

.btn-save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-cancel {
  background: #e2e8f0;
  color: #475569;
}

.btn-cancel:hover {
  background: #cbd5e1;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 15px;
  }
  
  .resources-table {
    font-size: 14px;
  }
  
  .actions {
    flex-direction: column;
  }
}
</style>