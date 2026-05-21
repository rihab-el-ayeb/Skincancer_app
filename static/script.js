// Image preview for predict page
const imageInput = document.getElementById('imageInput');
if (imageInput) {
    imageInput.addEventListener('change', function(e) {
        const preview = document.getElementById('imagePreview');
        if (e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = function(event) {
                preview.src = event.target.result;
                preview.classList.remove('d-none');
            };
            reader.readAsDataURL(e.target.files[0]);
        } else {
            preview.classList.add('d-none');
        }
    });
}

// Show loading spinner on form submit (predict form)
const predictForm = document.querySelector('form[action="/predict"]');
if (predictForm) {
    predictForm.addEventListener('submit', function() {
        const btn = this.querySelector('button[type="submit"]');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<span class="loader"></span> Analyzing...';
        }
    });
}

// Search/filter in patients table
const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('keyup', function() {
        const filter = this.value.toLowerCase();
        const rows = document.querySelectorAll('#patientsTable tbody tr');
        rows.forEach(row => {
            const text = row.innerText.toLowerCase();
            row.style.display = text.includes(filter) ? '' : 'none';
        });
    });
}

// Image modal function (for patients page)
function showImageModal(imgSrc) {
    const modalImg = document.getElementById('modalImage');
    if (modalImg) {
        modalImg.src = imgSrc;
        const modal = new bootstrap.Modal(document.getElementById('imageModal'));
        modal.show();
    }
}

// Auto-hide flash messages after 3 seconds
setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.style.transition = 'opacity 0.5s';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500);
    });
}, 3000);
