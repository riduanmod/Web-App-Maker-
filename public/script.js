document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('pwa-form');
    
    // Inputs
    const appNameInput = document.getElementById('appName');
    const appUrlInput = document.getElementById('appUrl');
    const appIconInput = document.getElementById('appIcon');
    const appThemeInput = document.getElementById('appTheme');
    
    // Preview Elements
    const previewName = document.getElementById('preview-name');
    const previewIframe = document.getElementById('preview-iframe');
    const previewIcon = document.getElementById('preview-icon');
    const previewHeader = document.getElementById('preview-header');
    const previewPlaceholder = document.getElementById('preview-placeholder');

    // Live Preview Sync Functions
    appNameInput.addEventListener('input', (e) => {
        previewName.textContent = e.target.value || 'App Name';
    });

    appIconInput.addEventListener('input', (e) => {
        previewIcon.src = e.target.value || 'https://via.placeholder.com/150?text=Icon';
    });

    // Update iframe only on blur/change
    appUrlInput.addEventListener('change', (e) => {
        const url = e.target.value;
        if (url) {
            previewIframe.src = url;
            previewIframe.style.display = 'block';
            previewPlaceholder.style.display = 'none';
        } else {
            previewIframe.src = 'about:blank';
            previewIframe.style.display = 'none';
            previewPlaceholder.style.display = 'flex';
        }
    });

    // --- Iro.js Color Wheel Integration (Fixed Overlay) ---
    const themeHexInput = document.getElementById('themeHex');
    const colorPreview = document.getElementById('colorPreview');
    const colorWheelOverlay = document.getElementById('colorWheelOverlay');
    const colorWheelModal = document.getElementById('colorWheelModal');

    // Initialize Color Picker
    var colorPicker = new iro.ColorPicker("#colorWheel", {
        width: 220,
        color: "#3B82F6",
        borderWidth: 2,
        borderColor: "#1f2937",
        layoutDirection: "vertical",
        layout: [
            { component: iro.ui.Wheel },
            { component: iro.ui.Slider, options: { sliderType: 'value' } }
        ]
    });

    // Update colors smoothly
    colorPicker.on('color:change', function(color) {
        const hex = color.hexString;
        themeHexInput.value = hex.toUpperCase();
        colorPreview.style.backgroundColor = hex;
        previewHeader.style.backgroundColor = hex;
        appThemeInput.value = hex;
    });

    // Manual HEX Update
    themeHexInput.addEventListener('input', (e) => {
        let val = e.target.value;
        if (!val.startsWith('#')) val = '#' + val;
        if (/^#[0-9A-Fa-f]{6}$/i.test(val)) {
            colorPicker.color.hexString = val;
            colorPreview.style.backgroundColor = val;
            previewHeader.style.backgroundColor = val;
            appThemeInput.value = val;
        }
    });

    // Toggle Fixed Modal Overlay
    window.toggleColorWheel = function() {
        const isHidden = colorWheelOverlay.classList.contains('hidden');
        if (isHidden) {
            colorWheelOverlay.classList.remove('hidden');
            colorWheelOverlay.classList.add('flex');
            setTimeout(() => {
                colorWheelOverlay.classList.remove('opacity-0');
                colorWheelModal.classList.remove('scale-95');
                colorWheelModal.classList.add('scale-100');
            }, 10);
        } else {
            colorWheelOverlay.classList.add('opacity-0');
            colorWheelModal.classList.remove('scale-100');
            colorWheelModal.classList.add('scale-95');
            setTimeout(() => {
                colorWheelOverlay.classList.add('hidden');
                colorWheelOverlay.classList.remove('flex');
            }, 300);
        }
    };

    // Close on clicking outside the modal box
    colorWheelOverlay.addEventListener('click', (e) => {
        if (e.target === colorWheelOverlay) {
            toggleColorWheel();
        }
    });

    // --- Form Submit ---
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const generatedUrl = `/app?name=${encodeURIComponent(appNameInput.value)}&url=${encodeURIComponent(appUrlInput.value)}&icon=${encodeURIComponent(appIconInput.value)}&theme=${encodeURIComponent(appThemeInput.value)}`;
        window.location.href = generatedUrl;
    });
});
