function loginModal() {
  const modal = document.getElementById("modal");
  fetch('/login')
    .then(response => response.text())
    .then(html => {
      modal.innerHTML = html;
      const form = document.getElementById('login-form');

      form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the form from submitting normally

        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/login');
        xhr.setRequestHeader('X-CSRFToken', form.querySelector('[name="csrf_token"]').value);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function () {
          const response = JSON.parse(xhr.response)
          if (xhr.status != 200) {
            document.getElementById('email-error').innerText = response.email ? response.email : ""
            document.getElementById('password-error').innerText = response.password ? response.password : ""
          }
          if (response.redirect){
            window.location.href = response.redirect;
          }
        };
        const d = {
          email:document.getElementById('email').value,
          password:document.getElementById('password').value,
          remember:document.getElementById('remember').checked
        }
        xhr.send(JSON.stringify(d));
      });
    })
  ocModal()
}
function signupModal() {
  const modal = document.getElementById("modal");
  fetch('/register')
    .then(response => response.text())
    .then(html => {
      modal.innerHTML = html;
      const form = document.getElementById('login-form');

      form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the form from submitting normally

        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/register');
        xhr.setRequestHeader('X-CSRFToken', form.querySelector('[name="csrf_token"]').value);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function () {
          const response = JSON.parse(xhr.response)
          if (xhr.status != 200) {
            document.getElementById('email-error').innerText = response.email ? response.email : ""
            document.getElementById('password-error').innerText = response.password ? response.password : ""
          }
          if (response.redirect){
            window.location.href = response.redirect;
          }
        };
        const d = {
          email:document.getElementById('email').value,
          password:document.getElementById('password').value,
          confirm_password:document.getElementById('confirm_password').value
        }
        xhr.send(JSON.stringify(d));
      });
    })
  ocModal()
}
// Open Close Modal
function ocModal(){
  if (modal.classList.contains("hidden")) {
    modal.classList.replace("hidden","flex");
  } else {
    modal.classList.replace("flex","hidden");
  }
}
if (window.location.search.indexOf('login=') !== -1) {
  loginModal()
}

// User profile dropdown
function showProfile(){
  document.getElementById("profileDropdown").classList.toggle("hidden");
  document.getElementById("profileDropdown").classList.toggle("block");
}