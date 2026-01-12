import { reactive } from 'vue';

export const authState = reactive({
  user: JSON.parse(localStorage.getItem('user')) || null,
  
  login(userData, token) {
    // userData should be the object that contains the 'name' field
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('token', token);
    this.user = userData; 
  },
  
  logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    this.user = null;
  }
});