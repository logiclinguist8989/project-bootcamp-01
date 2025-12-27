// Minimal form validation and demo behavior
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('loginForm');
  const email = document.getElementById('email');
  const password = document.getElementById('password');
  const emailError = document.getElementById('emailError');
  const passwordError = document.getElementById('passwordError');

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    let valid = true;
    emailError.textContent = '';
    passwordError.textContent = '';

    if (!email.value || !/^\S+@\S+\.\S+$/.test(email.value)) {
      emailError.textContent = 'Please enter a valid email address.';
      valid = false;
    }
    if (!password.value || password.value.length < 6) {
      passwordError.textContent = 'Password must be at least 6 characters.';
      valid = false;
    }

    if (!valid) return;

    // Demo success behavior (replace with real auth call)
    const btn = form.querySelector('.btn--primary');
    btn.disabled = true;
    btn.textContent = 'Signing in...';
    setTimeout(() => {
      btn.disabled = false;
      btn.textContent = 'Log In';
      alert(`Welcome back, ${email.value}! (demo)`);
      form.reset();
    }, 900);
  });
});